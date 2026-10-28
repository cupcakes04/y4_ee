# 4_1: MPPI Sampling and Control Optimization Explained

> **Context**: Personal concept understanding note for `chapters/research/04_predictive_mppi_control.md` (§4.1.1). Provides an intuitive, no-fluff breakdown of how Model Predictive Path Integral (MPPI) control samples candidate actions, simulates kinematics, evaluates costs, and synthesizes optimal velocity commands without computing analytical gradients.

---

## The 30-Second Mental Model (TL;DR)

If the formal math in §4.1.1 looks like academic jargon, think of MPPI like **training a Machine Learning model in real-time**:

```
[Phase 1: Sampling]   Randomly wiggle the gas & steering commands 2000 times (v, ω).
         │
[Phase 2: Physics]    Predict where the wheels go on the floor (x, y, θ). (Robot cannot slide sideways).
         │
[Phase 3: Loss]       THE MAP ENTERS HERE: Penalize walls, wandering off track, and jerky driving.
         │
[Phase 4: Softmax]    Give lowest-loss paths the highest vote, blend them, and send to the motors.
```

---

## 1. Controls vs. Poses vs. The Map (Untangling the Core Confusion)

A major source of confusion in §4.1.1 is mixing up **motor inputs**, **robot positions**, and **where the map actually is**.

### A. Controls $\mathbf{u} = [v, \omega]^T$ (Phase 1: The Pedals & Steering Wheel)
* $\mathbf{U} = [\mathbf{u}_0, \mathbf{u}_1, \dots, \mathbf{u}_{N-1}]$ is **NOT a list of positions**.
* It is a sequence of **motor velocity commands** over time:
  * $v_k$: Linear forward speed ($\text{m/s}$) $\to$ gas / brake pedal.
  * $\omega_k$: Angular turning rate ($\text{rad/s}$) $\to$ steering wheel rate.
* In Phase 1, MPPI simply takes a baseline plan and adds random Gaussian noise ($\boldsymbol{\epsilon}$) to test $M = 2000$ slightly different combinations of gas and steering.

### B. Poses $\mathbf{p} = [x, y, \theta]^T$ (Phase 2: The Resulting Floor Coordinates)
* $[x, y]$: Bird's Eye View (BEV) coordinates on the floor plane (in meters).
* $\theta$ (theta): The heading angle (which direction the robot's front is pointing).
* **Can it go sideways? NO!**
  * A standard warehouse AMR uses **differential drive kinematics** (non-holonomic).
  * It has **no sideways velocity** ($v_y = 0$). It cannot slide like a crab.
  * To move left, it **must rotate while driving forward**. That is why Phase 2 uses trigonometry:
    $$\begin{cases}
    x_{k+1} = x_k + v_k \cos(\theta_k) \Delta t \\
    y_{k+1} = y_k + v_k \sin(\theta_k) \Delta t \\
    \theta_{k+1} = \theta_k + \omega_k \Delta t
    \end{cases}$$
  * If $\theta = 0\text{ rad}$ (facing East), $v$ pushes purely into $+x$.
  * If $\theta = \frac{\pi}{2}\text{ rad}$ (facing North), $v$ pushes purely into $+y$.

### C. Where is the Map?
* **The map does NOT exist in Phase 1 or Phase 2!**
  * Phase 1 just invents 2,000 steering sequences in the abstract.
  * Phase 2 just simulates where those steering sequences would roll the chassis in empty space.
* **The MAP only enters in Phase 3:** The controller takes the simulated coordinates $(x_k, y_k)$ and overlays them onto the **Costmap** grid to see if they collide with walls or people.

---

## 2. Phase 3 Demystified: Can I Skip the Math?

**Yes.** You do not need to derive the summation or matrix inversion algebra. 

The equation in §4.1.1:
$$S(\mathbf{V}_m) = \phi(\mathbf{p}_{N, m}) + \sum_{k=0}^{N-1} \left( \sum_{j \in \text{Critics}} w_j \mathcal{L}_j(\mathbf{p}_{k, m}, \mathbf{v}_{k, m}) + \lambda \mathbf{u}_k^T \boldsymbol{\Sigma}^{-1} \mathbf{v}_{k, m} \right)$$

is literally just an ML-style **Loss Function**:

$$\text{Total Loss } S = \sum (\text{Critic Penalties}) + \text{Smoothness Regularizer} + \text{Terminal Goal Penalty}$$

### What are the Penalties? (What you actually tune in Nav2)

In practice, you configure these penalties in Nav2 using **Critic Plugins** and their weights ($w_j$):

| Penalty (Nav2 Critic) | What It Penalizes | Practical Intuition |
|---|---|---|
| **Obstacle Penalty** (`ObstaclesCritic`, `DynamicObstaclesCritic`) | Trajectory footprint touching a static wall or walking pedestrian on the costmap. | **Lethal penalty ($10^5$)**: Instantly ruins the trajectory's score so it receives zero vote. |
| **Path-Following Penalty** (`PathAlignCritic`, `PathAngleCritic`) | Distance between the simulated candidate path and the global reference plan. | Keeps the robot centered in the hallway rather than drifting erratically. |
| **Progress Penalty** (`PathFollowCritic` / Terminal Cost $\phi$) | Being far from the goal at the end of the 2-second horizon. | Prevents the robot from stopping still to "avoid risk"; pushes it to make forward progress. |
| **Effort / Smoothness Penalty** ($\lambda \mathbf{u}^T \boldsymbol{\Sigma}^{-1} \mathbf{v}$) | Rapid, violent fluctuations in motor speed (e.g., slamming from $+1\text{ m/s}$ to $-1\text{ m/s}$). | Acts as an energy regularizer; keeps motion smooth and protects motors and gearboxes. |

---

## 3. Phase 4 Demystified: Can I Skip the Optimization Math?

**Yes.** Control theory papers call this the *"Feynman-Kac Path Integral formula"*, but in computer science it is literally just a standard **Softmax with Temperature**:

$$\text{Weight } w_m = \text{Softmax}\left(-\frac{\text{Loss } S_m}{\text{Temperature } \lambda}\right)$$

$$\text{Final Command } \mathbf{u}^* = \sum_{m=1}^M w_m \mathbf{v}_m$$

### The 3 Rules You Need to Know:
1. **Lower Loss = Exponentially Higher Voting Power:**
   * Because of the negative sign ($-\frac{S}{\lambda}$), paths with tiny penalties get the majority of the weight.
   * Any trajectory that hits an obstacle has $S \to \infty \implies \exp(-\infty) = 0$, so crashing paths get **0% vote**.
2. **The Output is a Consensus (Weighted Average):**
   * Instead of betting everything on a single randomly sampled path (which might be a lucky outlier or razor-thin near a wall), MPPI averages across the safest cluster of paths:
     $$\mathbf{u}^* = 0.85 \times (\text{Safe Path A}) + 0.15 \times (\text{Safe Path B}) + 0.0 \times (\text{Crashing Paths})$$
3. **The Only Parameter You Care About is Temperature $\lambda$:**
   * Works identically to temperature in LLMs:
     * **Small $\lambda$ (e.g. $0.05$):** "Winner takes all" (greedy). The single lowest-loss trajectory gets almost $100\%$ of the weight.
     * **Large $\lambda$ (e.g. $1.0$):** Soft blend across many candidates. Smoother, but can blur distinct options together.
   * *Note on the term $-\min S$:* It's just a numerical programming trick to prevent $\exp(-\text{huge})$ from underflowing to `NaN` in C++.

---

## 4. Receding Horizon & Warm-Starting (The Execution Loop)

Once the optimal 2-second sequence $\mathbf{U}^* = [\mathbf{u}_0^*, \mathbf{u}_1^*, \dots, \mathbf{u}_{N-1}^*]$ is calculated:

```
  Synthesized Plan: [ u_0*,  u_1*,  u_2*,  ...,  u_{N-1}* ]
                      │
                      ▼
               Sent to Robot Hardware (/cmd_vel)
```

1. **Dispatch:** Only the very first command $\mathbf{u}_0^*$ is sent to the motor controller (`/cmd_vel`).
2. **Warm Start:** The remaining sequence is shifted forward by one time step: $[\mathbf{u}_1^*, \mathbf{u}_2^*, \dots, \mathbf{u}_{N-1}^*]$ becomes the baseline $\mathbf{U}$ for the next cycle.
3. **Repeat:** 20 to 50 milliseconds later, fresh sensor data arrives, and the cycle repeats.

---

## 5. Summary Cheat Sheet

| Step | What the Math Says | What is Actually Happening |
|---|---|---|
| **Phase 1** | $\mathbf{v}_{k,m} = \mathbf{u}_k + \boldsymbol{\epsilon}_{k,m}$ | Randomly perturb throttle $v$ and steering $\omega$ 2000 times. |
| **Phase 2** | $\mathbf{p}_{k+1} = f(\mathbf{p}_k, \mathbf{v}_k)$ | Simulate wheel rollout on the floor ($x, y, \theta$). Robot cannot slide sideways. |
| **Phase 3** | $S(\mathbf{V}_m) = \phi + \sum (w_j \mathcal{L}_j + \text{reg})$ | **Map lookup (Loss function)**: Score each rollout for collisions, path alignment, and jerkiness. |
| **Phase 4** | $w_m = \frac{\exp(-S_m/\lambda)}{\sum \exp(-S/\lambda)}$ | **Softmax**: Give lowest-loss paths high voting weights; calculate the weighted average command $\mathbf{u}^*$. |
| **Execution** | Send $\mathbf{u}_0^*$, warm start $\mathbf{U}$ | Send the first motor command to `/cmd_vel`, shift the buffer, and re-solve 50 ms later. |
