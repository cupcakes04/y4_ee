# 4_3: Custom Dynamic Obstacle Critic Plugin Architecture

> **Context**: Personal concept understanding note for `chapters/research/04_predictive_mppi_control.md` (§4.3). Explains how the custom C++ critic plugin projects obstacle velocities through time, expands dynamic safety margins, and resolves the classic "Freezing Robot" failure mode without modifying core Nav2 libraries.

---

## The 30-Second Mental Model (TL;DR)

```
[Standard Nav2 Problem]
Costmap is a static photo (t = 0). 
Pedestrian walking across hallway -> Map marks entire corridor red -> Robot panics and freezes (v = 0).

[Our Custom Critic Solution]
Costmap is a video with time (t = 0 ... 2.0s).
Pedestrian walking at 1.2 m/s -> Critic projects where they will be at each second.
Paths trying to cross ahead get penalized; paths smoothly following behind get zero penalty.
Result: Robot naturally yields and glides through without stopping.
```

---

## 1. The Root Problem: Why Standard Nav2 Fails (§4.2)

Default Nav2 architectures decouple path planning from sensor perception using a **2D Costmap** (`nav2_costmap_2d`). 
While great for static walls and shelves, this creates two major failure modes when humans walk around:

| Failure Mode | What Actually Happens | Real-World Consequence |
|---|---|---|
| **1. The Freezing Robot** *(False Path Invalidation)* | A pedestrian crosses an aisle $3\text{ m}$ ahead at $1.2\text{ m/s}$. Standard Nav2 paints that aisle blocked **right now**. In 2 seconds, the human will already be gone, but the static costmap registers a lethal wall. | MPPI sees every forward path blocked, scores them with infinite cost, drops velocity to zero ($\mathbf{u}^* = [0, 0]^T$), and starts spinning in place. |
| **2. Blind Interception** *(Collision Danger)* | A human is walking into an open intersection that the robot plans to cross. Because the human isn't in that intersection *right now*, the static costmap marks it as completely free ($0\text{ cost}$). | The robot accelerates directly into the human's crossing path, forcing an emergency E-stop when the human suddenly enters the safety bubble. |

---

## 2. How the Custom Critic Plugin Solves It (§4.3)

Instead of relying on a time-blind costmap grid, we write a **custom C++ Critic Plugin** (`DynamicObstaclesCriticPlugin`) dynamically loaded into MPPI via ROS 2 `pluginlib`.

It injects a new spatio-temporal loss term directly into **Phase 3** of MPPI:

```
           /tracked_obstacles (ROS 2 Topic from Kalman Filter)
                           │
                           ▼
 ┌──────────────────────────────────────────────────────────────────┐
 │ DynamicObstaclesCriticPlugin (Evaluates M = 2000 rollouts)       │
 │                                                                  │
 │   For each simulated future time step τ_k (0.0s to 2.0s):        │
 │     1. Project pedestrian forward: p_obs(τ_k) = p_0 + v_obs * τ_k│
 │     2. Compare against robot rollout position: p_robot(τ_k)      │
 │     3. Calculate distance: dist = || p_robot - p_obs ||          │
 │     4. If dist < Lethal Radius -> Disqualify trajectory (Cost 10⁵)│
 │     5. If dist in safety zone  -> Apply Gaussian repulsion cost   │
 └──────────────────────────────────────────────────────────────────┘
```

---

## 3. Mathematical Breakdown Demystified

### A. Forward Motion Projection (High School Physics)
$$\mathbf{p}_{\text{obs}, i}(\tau_k) = \mathbf{p}_{\text{obs}, i}(0) + \mathbf{v}_{\text{obs}, i} \cdot \tau_k$$

* $\tau_k = k \cdot \Delta t$ is the lookahead preview time (e.g., $0.1\text{ s}, 0.5\text{ s}, 1.0\text{ s}, 2.0\text{ s}$).
* The Kalman filter already provides estimated pedestrian velocity $\mathbf{v}_{\text{obs}} = [v_x, v_y]^T$.
* We simply project their position forward along that vector: $\text{Distance} = \text{Speed} \times \text{Time}$.

---

### B. Spatio-Temporal Dynamic Cost (The Two-Tier Penalty)

For every candidate robot trajectory point at time $\tau_k$, the critic computes Euclidean clearance:
$$\text{dist} = \|\mathbf{p}_{\text{robot}}(\tau_k) - \mathbf{p}_{\text{obs}, i}(\tau_k)\|$$

It then applies two distinct penalties:

#### 1. Lethal Boundary Check (Instant Kill)
$$\text{If } \text{dist} < R_{\text{robot}} + R_{\text{obs}} \implies \text{Cost} = 10^5$$
* If the robot's physical body touches the pedestrian at that future time step, the candidate path receives a lethal cost ($10^5$).
* When passed into MPPI's Softmax in Phase 4 ($\exp(-10^5/\lambda) = 0$), this trajectory gets **zero voting weight**.

#### 2. Gaussian Repulsion Cushion (Smooth Yielding)
$$\mathcal{L}_{\text{dyn}} = w_{\text{dyn}} \cdot \exp\left( -\frac{\text{dist}^2}{2 \, \sigma_i^2(\tau_k)} \right)$$
* Acts like a smooth magnetic repulsion field around moving people.
* If the robot gives the pedestrian comfortable clearance ($> 1.5\text{ m}$), the penalty drops to nearly $0$.
* If the robot cuts it close, the penalty increases exponentially, encouraging the controller to choose a wider swerve or ease off the throttle.

---

### C. Why Does the Safety Bubble Expand Over Time?
$$\sigma_i(\tau_k) = R_{\text{robot}} + R_{\text{obs}} + \alpha \cdot \tau_k$$

Notice the expansion rate term **$\alpha \cdot \tau_k$**:
* **At $\tau = 0.1\text{ s}$:** We know with high certainty where the person is walking. The safety cushion $\sigma$ stays compact.
* **At $\tau = 2.0\text{ s}$:** Humans are non-linear; the person might slow down, turn, or take unexpected steps. Velocity estimation covariance naturally grows over time.
* **The engineering fix:** By letting the buffer expand linearly with time ($\alpha \ge 0$), the robot gives moving agents a wider berth the further into the future it looks, preventing risky close-quarter cuts.

---

## 4. Software Architecture & Implementation Footprint (§4.3.3)

| Architectural Choice | Why It Matters Industrially |
|---|---|
| **Nav2 `pluginlib` Interface** | Zero modification to Nav2 core. The critic compiles as an independent shared library (`.so`) loaded dynamically via YAML configuration at runtime. |
| **SIMD Batch Evaluation** | Evaluating $2000 \text{ rollouts} \times 40 \text{ steps} = 80,000$ points sounds heavy, but because it is simple vector math, CPU vectorization (AVX2/NEON) and OpenMP parallel loops process the entire batch in **$< 0.3\text{ ms}$**. |
| **Minimal Code Footprint** | Complete implementation requires **fewer than 150 lines of modern C++ (C++17)** with zero external dependencies beyond standard ROS 2 and Nav2. |

---

## 5. Summary: Before vs. After Custom Critic

| Scenario | Standard Nav2 MPPI | Nav2 MPPI + Custom Dynamic Critic |
|---|---|---|
| **Human crosses aisle ahead** | Paints corridor blocked $\to$ **Freezes / spins ($v = 0$)**. | Calculates human clears corridor in $1.2\text{ s}$ $\to$ **Slows down smoothly, then glides through behind them**. |
| **Human walking towards robot** | Relies on circular static inflation $\to$ **Late emergency braking**. | Detects closing velocity $\to$ **Proactively swerves away well in advance**. |
| **CPU Load** | Negligible. | Adds $< 0.3\text{ ms}$ CPU time (well within the $50\text{ ms}$ budget). |

