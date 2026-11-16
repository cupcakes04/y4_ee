# 3_4: The Kalman Filter as a Modern State-Space Observer

> **Context**: Theoretical bridge connecting `chapters/research/03_perception_and_tracking.md` (§3.4 Stage 3) to Modern / Advanced State-Space Control Systems. Explains the structural duality between state observers, Kalman filtering, and optimal control.

---

## 1. Classical Control vs. Modern State-Space Control

| Dimension | Classical Control (Frequency Domain) | Modern Control (State-Space Domain) |
|---|---|---|
| **Mathematical Core** | Laplace domain Transfer Functions: $G(s) = \frac{Y(s)}{U(s)}$ | First-order vector differential / difference equations: $\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}$ |
| **System View** | Input-Output "Black Box" (SISO) | Internal Internal State Dynamics (MIMO): $\mathbf{x} = [x_1, x_2, \dots, x_n]^T$ |
| **Key Tools** | Bode plots, Nyquist criterion, Root Locus, PID controllers | State feedback ($-\mathbf{K}\mathbf{x}$), Pole placement, LQR, Observers |

---

## 2. The Fundamental Problem: Unmeasured Internal States

In state-space control, we often cannot directly measure all state variables of interest.
- In our obstacle tracking pipeline, the sensor **only measures 2D position** ($z_x, z_y$).
- However, the predictive trajectory planner requires **obstacle velocities** ($v_x, v_y$) to project collision trajectories into the future ($\tau \in [0, 2.0]\text{ s}$).
- Calculating raw numerical derivatives ($\frac{\Delta x}{\Delta t}$) fails because high-frequency sensor noise ($\pm 3\text{ cm}$) causes velocity estimates to explode.

### The Solution: State Observers
A **State Observer** runs a mathematical model of the physical system in parallel with the real world, comparing predicted sensor outputs with real sensor outputs to reconstruct unmeasured states:

1. **Luenberger Observer (Deterministic):** Designed for noise-free systems. Observer feedback gain $\mathbf{L}$ is chosen via manual pole placement.
2. **Kalman Filter (Stochastic):** The mathematically **optimal observer** when the plant suffers from random disturbances (process noise $\mathbf{Q}$) and the sensors suffer from noise (measurement noise $\mathbf{R}$).

---

## 3. Matrix Mapping: Control Theory $\longleftrightarrow$ Kalman Filter

Robotics and control theory use slightly different notation for identical mathematical structures:

| Concept | Control Theory Notation | Kalman Filter Notation (Our Code) | Physical Meaning in AMR Tracking |
|---|---|---|---|
| **State Vector** | $\mathbf{x}(t)$ or $\mathbf{x}_k$ | $\mathbf{x}_k = [x, y, v_x, v_y]^T$ | Position and velocity on the warehouse floor |
| **State Matrix** | $\mathbf{A}$ (continuous) | $\mathbf{F} = \begin{bmatrix} 1 & 0 & \Delta t & 0 \\ 0 & 1 & 0 & \Delta t \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$ | Constant Velocity (CV) physics: $\text{pos} \leftarrow \text{pos} + \text{vel} \cdot \Delta t$ |
| **Input Matrix** | $\mathbf{B}\mathbf{u}$ | $\mathbf{0}$ (or unmodeled) | Obstacles are unactuated by our robot (passive agents) |
| **Output / Sensor Matrix** | $\mathbf{C}$ | $\mathbf{H} = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \end{bmatrix}$ | Extraction mask: sensor reads position, not velocity |
| **Process Disturbance** | Disturbance $w(t)$ | Covariance $\mathbf{Q} \in \mathbb{R}^{4 \times 4}$ | Pedestrian acceleration, dodging, or turning maneuvers |
| **Measurement Noise** | Sensor noise $v(t)$ | Covariance $\mathbf{R} \in \mathbb{R}^{2 \times 2}$ | LiDAR beam variance ($\sigma_{\text{lidar}} \approx 0.03\text{ m}$) |
| **Observer Gain** | Observer Gain $\mathbf{L}$ | Kalman Gain $\mathbf{K}_k$ | Dynamic weighting: balances model trust vs sensor trust |

---

## 4. The Two-Step Cycle in State-Space Terms

```
                 ┌────────────────────────────────────────────────────────┐
                 │ 1. TIME UPDATE (Open-Loop Physics Predict)             │
                 │    x̂_{k|k-1} = F · x̂_{k-1|k-1}                         │
                 │    P_{k|k-1} = F · P_{k-1|k-1} · F^T + Q               │
                 └───────────────────────────┬────────────────────────────┘
                                             │
                                             ▼
                 ┌────────────────────────────────────────────────────────┐
                 │ 2. MEASUREMENT UPDATE (Closed-Loop Error Feedback)     │
                 │    Innovation:  y_k = z_k - H · x̂_{k|k-1}              │
                 │    Kalman Gain: K_k = P_{k|k-1} · H^T · (H P H^T + R)^-1│
                 │    State:       x̂_{k|k} = x̂_{k|k-1} + K_k · y_k        │
                 └────────────────────────────────────────────────────────┘
```

- **Open-Loop Step (Predict):** Multiplies the prior state by system dynamics $\mathbf{F}$. If the camera/laser temporarily drops out, this step continues predicting where the obstacle moves based on its existing velocity.
- **Closed-Loop Step (Correct):** Computes the error (Innovation $\mathbf{y}_k$) between where the sensor saw the target versus where the model predicted it. The **Kalman Gain $\mathbf{K}_k$** injects this error back into the state vector, smoothly refining both position and velocity.

---

## 5. The Grand Unified Architecture: LQG and Separation Principle

Why does this matter for the final year project?

In advanced control systems, the **Separation Principle** states that:
> The design of an optimal state estimator (the Kalman Filter) and the design of an optimal feedback controller (such as LQR or MPPI) can be partitioned and solved completely independently without loss of optimality.

In our project:
1. **Observer (Perception Layer):** The Kalman Filter ingests noisy, discrete 2D LiDAR observations and yields clean state estimates $\hat{\mathbf{x}} = [x, y, v_x, v_y]^T$.
2. **Controller (Planning Layer):** The MPPI controller (`nav2_mppi_controller`) consumes $\hat{\mathbf{x}}$ to optimize trajectory rollouts $\mathbf{u}_k = [v, \omega]^T$.
3. **Combined Architecture:** Together, they form a modern **stochastic predictive control pipeline**, turning raw, blind sensor measurements into smooth, proactive collision avoidance.

