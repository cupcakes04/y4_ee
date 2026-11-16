# 00. The Sensor-to-Motion Pipeline: How Robots See, Represent Space, and Steer

> **Purpose of this document:**  
> A fundamental, intuitive guide to the complete chain connecting raw sensor measurements to robot steering. It explains what sensors physically measure, how computers represent physical space, how path planners generate motion, why moving obstacles break traditional planners, and how predictive trajectory control bridges the gap.

---

## 1. The Big Picture: From Sensor Signals to Motor Voltages

At its simplest, mobile robot navigation is an information-processing pipeline that transforms raw physical energy (photons, laser reflections, wheel ticks) into physical motor actions (turning wheels):

```
┌──────────────────┐      ┌────────────────────────┐      ┌───────────────────────┐      ┌─────────────────┐
│   RAW SENSORS    │ ──►  │ SPATIAL REPRESENTATION │ ──►  │     PATH PLANNING     │ ──►  │ MOTOR ACTUATION │
│ Photons, Laser   │      │ Costmaps, Points,      │      │ Global Route + Local  │      │ Wheel Speeds:   │
│ Pulses, Encoders │      │ Dynamic State Vectors  │      │ Trajectory Rollouts   │      │ cmd_vel (v, w)  │
└──────────────────┘      └────────────────────────┘      └───────────────────────┘      └─────────────────┘
```

Every design choice, trade-off, and debate in autonomous navigation comes down to how information moves through these four stages.

---

## 2. Step 1: What Sensors Physically Measure (The Raw Inputs)

Computers cannot "see" rooms or "know" what an obstacle is; they only receive arrays of numbers from physical transducers.

```
       2D PLANAR LiDAR                          MONOCULAR RGB CAMERA                     STEREO / DEPTH CAMERA
 (Range Array at fixed height)               (2D Grid of Color Pixels)                (Disparity & 3D Point Cloud)

      \       |       /                        ┌───────────────────────┐                    ┌───────────────┐
       \      |      /                         │ [R, G, B]   [R, G, B] │                    │  [X, Y, Z]    │
   ─────●─────●─────●─────                     │ [R, G, B]   [R, G, B] │                    │  Point Cloud  │
         Laser Plane                           └───────────────────────┘                    └───────────────┘
  Measures: (distance, angle)                 Measures: (u, v) pixel colors                Measures: Disparity -> Depth
  Exact distance, zero semantics              Rich semantics, zero metric depth            Direct 3D, high noise at range
```

### 2.1 2D Planar LiDAR
- **Physical Mechanism:** A laser diode fires rapid pulses of infrared light while spinning on a motor. It measures Time-of-Flight (ToF)—the round-trip travel time of photons reflected back from surfaces.
- **Data Output:** A 1D array of ranges $(r_i, \theta_i)$ at a single horizontal elevation ($10\text{--}20\text{ cm}$ above the ground).
- **What it does well:** Millimeter-accurate distance ($<1\text{ cm}$ error), wide field of view ($270^\circ\text{--}360^\circ$), completely unaffected by room lighting, shadows, or textureless walls. Trivial compute load ($<1\text{ ms}$ processing).
- **The Blind Spot:** **Zero semantics and single-plane blindness.** It cannot tell if a return is a concrete column, a human ankle, or a cardboard box. If an obstacle hangs $30\text{ cm}$ above the floor (e.g. forklift tines), the laser passes underneath completely undetected.

### 2.2 Monocular RGB Camera
- **Physical Mechanism:** A 2D grid of photodiodes focused through a glass lens capturing ambient photons across Red, Green, and Blue wavelengths.
- **Data Output:** A 2D pixel array ($H \times W \times 3$, e.g., $1920 \times 1080 \times 3$).
- **What it does well:** Rich semantic context. AI object detectors (like YOLO) can inspect patterns of pixels and immediately classify: `"Person"`, `"Forklift"`, or `"Box"`, bounding them in pixel boxes $[u_{\min}, v_{\min}, u_{\max}, v_{\max}]$.
- **The Blind Spot:** **Scale ambiguity (no metric depth).** In projective geometry, an object half the size at $2\text{ meters}$ casts the exact same pixel image as a full-sized object at $4\text{ meters}$. A single camera cannot calculate physical distance without making assumptions about object size or floor flatness.

### 2.3 Stereo RGB-D Cameras
- **Physical Mechanism:** Two parallel camera lenses separated by a baseline distance $b$, mimicking human binocular vision. By finding corresponding visual features in both images, it calculates pixel shift (**disparity** $d = u_{\text{left}} - u_{\text{right}}$) to triangulate depth:
  $$Z = \frac{f \cdot b}{d}$$
- **What it does well:** Directly produces a full 3D point cloud $(X, Y, Z)$ covering both height and depth.
- **The Blind Spot:** **Quadratic noise degradation and optical failure.** 
  1. Depth error grows quadratically with distance ($\Delta Z \propto Z^2$). At $8\text{ meters}$, disparity jitter creates noise of $\pm 0.8\text{--}1.2\text{ meters}$, making smooth velocity estimation nearly impossible.
  2. Active IR projectors get blinded by warehouse skylights and fail on featureless white walls or shiny polished concrete floors (specular glare).

---

## 3. Step 2: How Robots Represent Space (From Signals to Internal Maps)

A path planner cannot consume raw laser pulses or camera pixels directly. It needs an internal mathematical representation of space:

```
              SPATIAL REPRESENTATION PARADIGMS
                             │
       ┌─────────────────────┴─────────────────────┐
       ▼                                           ▼
GRID-BASED (Occupancy Grid / Costmap)     OBJECT-BASED (Tracked States)
• Represents EVERY cell in space          • Represents only DISCRETE objects
• Cell = Free, Occupied, or Unknown       • Vector: [x, y, vx, vy, radius]
• Time-invariant (t = 0 snapshot)         • Explicitly models velocity over time
```

### 3.1 The Traditional Grid: The 2D Costmap (`nav2_costmap_2d`)
The standard spatial model in ROS / Nav2 is a **2D Costmap**—an overhead raster grid representing the floor broken into small square cells (typically $5\text{ cm} \times 5\text{ cm}$):
- **Cell Values:** Each cell holds a cost value from `0` (completely free floor) to `254` (lethal obstacle / collision).
- **The Three Layer Stack:**
  1. **Static Layer:** Pre-built 2D map from SLAM showing permanent walls and building architecture.
  2. **Obstacle Layer:** Live LiDAR hit points are marked as occupied cells (`254`), while clear laser rays clear out old hits (raycasting).
  3. **Inflation Layer:** Adds a mathematical "cushion" around every obstacle that decays exponentially. This prevents the robot from driving so close to a wall that its chassis scrapes it.

### 3.2 The Object-Based State Model (Dynamic State Vectors)
Instead of rasterizing everything into a grid, object-based representations isolate dynamic targets into discrete parametric states:
$$\mathbf{x}_i = \begin{bmatrix} x_i \\ y_i \\ v_{x, i} \\ v_{y, i} \\ R_i \end{bmatrix}$$
- Maintained by a state estimator (e.g. an **Extended Kalman Filter**).
- **Advantage:** Space is not quantized into millions of grid cells, and crucially, **velocity is explicitly tracked**.

---

## 4. Step 3: The Path Planning Hierarchy (Macro Route vs. Micro Maneuvers)

Planning is divided into two distinct hierarchical layers operating at completely different speeds and scales:

```
┌────────────────────────────────────────────────────────────────────────┐
│ GLOBAL PATH PLANNER (The "Highway GPS")                                │
│ • Runs once (or every few seconds)                                     │
│ • Reads the entire static warehouse map (Static Costmap)               │
│ • Finds the shortest obstacle-free route from Point A to Point B       │
│ • Output: A static path of waypoints [(x0, y0), (x1, y1), ... (xN, yN)]│
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Global Path
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LOCAL CONTROLLER / TRAJECTORY PLANNER (The "Steering Wheel")           │
│ • Runs continuously at HIGH FREQUENCY (20 to 50 Hz, every 20-50 ms)    │
│ • Reads live sensor inputs and the local environment (Local Costmap)   │
│ • Tracks the global path while dynamically swerving around obstacles   │
│ • Output: Real-time velocity commands: cmd_vel = [v, omega]            │
└────────────────────────────────────────────────────────────────────────┘
```

### 4.1 The Global Planner
- **Algorithms:** $A^*$, Dijkstra, or Nav2's `SmacPlanner2D`.
- **Function:** Solves a graph search problem across the static map. It does not care about dynamic obstacles moving around right now; its job is to find the overall corridor sequence to reach the destination room.

### 4.2 The Local Controller
- **Algorithms:** DWA (Dynamic Window Approach), TEB (Timed Elastic Band), or MPPI (Model Predictive Path Integral).
- **Function:** Calculates the immediate next motor command (`cmd_vel`: forward speed $v$ in $\text{m/s}$ and rotational speed $\omega$ in $\text{rad/s}$) to move along the global path without colliding with local obstacles over the next $1\text{--}3\text{ seconds}$.

---

## 5. Step 4: How Local Planners Actually Steer (The Common Paradigms)

How does a local controller choose what steering command to send to the motors? There are three main approaches:

```
   PARADIGM 1: DWA                       PARADIGM 2: TEB                       PARADIGM 3: MPPI
 (Dynamic Window Approach)             (Timed Elastic Band)             (Model Predictive Path Integral)

      Sample velocity pairs               Deform global path               Sample 2000 random futures
        (v, w) -> Arcs                    like a rubber band                     on GPU / SIMD
           ┌───┐                                 ──●──                          ╭─────╮
           │   │                                ╱     ╲                        ╭───────╮
           └───┘                               ●       ●                      ─────────►
       Simple, reactive                    Elastic optimization            Stochastic optimal control
```

### 5.1 Dynamic Window Approach (DWA)
- **How it works:** Discrete velocity pairs $(v, \omega)$ within the robot's acceleration limits are sampled. For each pair, it projects a circular arc forward for $1\text{--}2\text{ seconds}$ on the 2D costmap. It scores each arc based on path progress, goal distance, and clearance, picking the best score.
- **Pros:** Fast, simple, reliable in wide open spaces.
- **Cons:** Very short-sighted. Often gets stuck in local minima (e.g. U-shaped obstacles) or oscillates in narrow aisles.

### 5.2 Timed Elastic Band (TEB)
- **How it works:** Treats the planned trajectory like an elastic band connecting start and goal. It uses non-linear numerical optimization (g2o) to deform the band away from costmap obstacles while optimizing transit time.
- **Pros:** Smooth, time-optimal trajectories that respect kinematic acceleration limits.
- **Cons:** Computationally heavy. In dynamic environments, the optimizer can flip between topologically distinct paths (e.g., trying to pass left, then suddenly right), causing visible robot stuttering.

### 5.3 Model Predictive Path Integral (MPPI) Controller
- **How it works (The Modern Standard in Nav2):**
  1. Instead of solving mathematical gradients, it generates **$1,000\text{--}2,000$ perturbed candidate control sequences** in parallel across a lookahead horizon ($T = 2.0\text{ s}$).
  2. It kinematically rolls out every candidate path forward through time.
  3. Each trajectory rollout is scored by a modular chain of **"Critics"** (e.g., `GoalCritic`, `PathAlignCritic`, `ObstaclesCritic`).
  4. It computes a softmax-weighted average across all candidate paths to synthesize the mathematically optimal control action $\mathbf{u}^*$.
- **Pros:** Extremely robust, handles complex vehicle kinematics, runs at $30\text{--}50\text{ Hz}$ on multi-core CPUs/GPUs, never gets stuck in local numerical derivative traps.

---

## 6. Step 5: The Fundamental Collision (Why Moving Obstacles Break Traditional Planners)

Now we reach the core problem in autonomous robotics that motivates this entire project: **The Static Assumption Conflict**.

```
WHAT TRADITIONAL PLANNERS ASSUME               WHAT ACTUALLY HAPPENS IN REALITY
────────────────────────────────────           ─────────────────────────────────────────
The Costmap is a snapshot at t = 0             Obstacles MOVE across time (t > 0)

      [Obstacle at t = 0]                             [t = 0]       [t = 1s]      [t = 2s]
              ●                                          ● ────────────► ● ────────────► ●
        (Treated as an                               (Pedestrian crosses and CLEARS the aisle)
      unmoving brick wall)

Planner evaluates t = 2s rollout against       Planner evaluates t = 2s rollout against
the t = 0 obstacle location!                   where the obstacle will ACTUALLY be!
──► FAILS: Robot freezes or swerves.           ──► SUCCEEDS: Robot smoothly yields.
```

### The Breakdown:
1. **The Costmap has no clock:** Standard costmaps (`nav2_costmap_2d`) are 2D arrays $(X, Y)$. There is no time coordinate $T$.
2. **Dynamic obstacles are painted as static barriers:** When a walking pedestrian intersects the 2D LiDAR plane, their legs are marked on the costmap as occupied cells.
3. **The Resulting Pathologies:**
   - **Pathology A: The Freezing Robot (False Positive Collision):**  
     A pedestrian crosses an aisle $3\text{ meters}$ ahead at $1.2\text{ m/s}$. The costmap marks the aisle as blocked. When MPPI rolls out candidate trajectories for lookahead time $\tau = 1.5\text{ s}$, it evaluates them against the pedestrian's *current* position ($t = 0$). Every trajectory down the aisle receives a maximum collision penalty. The robot slams on its brakes and stops dead in its tracks—even though by $t = 1.5\text{ s}$ the human would have completely cleared the aisle!
   - **Pathology B: Blind Interception (False Negative Collision):**  
     A vehicle is driving toward an open intersection that the robot is approaching. The intersection currently has no obstacle ($0\text{ cost}$). The robot accelerates forward, only to arrive at the exact same moment as the vehicle, forcing a panic emergency halt.

---

## 7. Step 6: The Solution (Spatio-Temporal Predictive Planning)

To solve this problem without abandoning the proven, reliable Nav2 planning architecture, we decouple **static infrastructure** from **dynamic traffic**:

```
                       THE DUAL-REPRESENTATION ARCHITECTURE
                                         │
        ┌────────────────────────────────┴────────────────────────────────┐
        ▼                                                                 ▼
STATIC INFRASTRUCTURE                                             DYNAMIC OBSTACLES
(Walls, Racks, Machinery)                                         (Walking Humans, Moving Carts)
        │                                                                 │
        ▼                                                                 ▼
Standard 2D Costmap (t = 0)                                       Tracked State Vectors [x, y, vx, vy]
        │                                                                 │
        ▼                                                                 ▼
Standard Static Critics                                           Custom Predictive Dynamic Critic
(Evaluates spatial clearance to walls)                            (Projects positions forward: p0 + v*tau)
        │                                                                 │
        └────────────────────────────────┬────────────────────────────────┘
                                         ▼
                             MPPI Rollout Evaluator
                    (Evaluates candidate trajectories across
                     BOTH space and future time horizon tau)
                                         │
                                         ▼
                            Smooth Proactive Motion
                         (Yields, swerves, ZERO freezes)
```

### How the Predictive Critic Works Mathematically:
When MPPI simulates candidate trajectory $m$ at preview horizon step $k$ (corresponding to future lookahead time $\tau_k = k \cdot \Delta t$):
1. It queries the tracked obstacle's state: position $\mathbf{p}_0$ and velocity $\mathbf{v}_{\text{obs}}$.
2. It extrapolates where the obstacle will be at that exact future moment:
   $$\mathbf{p}_{\text{obs}}(\tau_k) = \mathbf{p}_0 + \mathbf{v}_{\text{obs}} \cdot \tau_k$$
3. It evaluates the distance between the simulated robot pose $\mathbf{p}_{\text{robot}}(\tau_k)$ and the forward-projected obstacle pose $\mathbf{p}_{\text{obs}}(\tau_k)$.
4. If a candidate trajectory would intersect the obstacle's future position, it receives a penalizing cost. If a candidate trajectory slightly decelerates (yielding) so the obstacle crosses before the robot arrives, it receives a low cost.

**The outcome:** The robot transitions from a blind, reactive "freeze-and-wait" machine to a proactive, fluid autonomous vehicle that naturally yields to crossing traffic.

---

## 8. Summary: The Mental Model at a Glance

| Pipeline Stage | What Exists in Reality | What This Project Uses / Designs |
|---|---|---|
| **Raw Sensing** | 2D LiDAR (distances) + Camera (pixels) | 2D LiDAR + Monocular RGB Camera |
| **Spatial Fusion** | Separate data streams | Camera detects & tracks (ByteTrack); LiDAR gates depth |
| **State Estimation** | None (raw points dumped to costmap) | Per-track linear Kalman filter estimating $[x, y, v_x, v_y]^T$ |
| **Spatial Model** | Time-invariant 2D Costmap ($t=0$) | Dual model: Static Costmap for walls + State Vectors for agents |
| **Local Planning** | Default MPPI querying static costmap | Custom C++ `DynamicObstaclesCriticPlugin` forward-projecting motion |
| **Robot Behavior** | Freezes in front of crossing traffic | Proactively yields or deflects smoothly around moving traffic |
