# Paper Card: L14 - Helbing & Molnar (1995)

- **Key:** L14
- **Citation:** D. Helbing and P. Molnar, "Social force model for pedestrian dynamics," *Physical Review E*, vol. 51, no. 5, pp. 4282–4286, May 1995. doi:10.1103/PhysRevE.51.4282.
- **Status:** Verified (Canonical physics and pedestrian dynamics paper)

---

## 1. Core Summary & Contribution
Introduces the foundational *Social Force Model* (SFM) describing pedestrian motion through continuous physical and psychological forces:
- Pedestrians accelerate toward a destination with a characteristic desired velocity $\mathbf{v}_0$ (empirically $1.2\text{--}1.4\text{ m/s}$).
- Repulsive forces model avoidance of static boundaries and other moving individuals.
- Establishes the standard mathematical framework for simulating and predicting human motion in crowded spaces.

---

## 2. Relevance to FYP (SD-MEng-26-01)
- **Pedestrian Simulation Grounding:** Provides theoretical justification for simulated pedestrian velocities ($0.8\text{--}1.4\text{ m/s}$) and deceleration dynamics in Gazebo Harmonic test scenarios (Scenarios A, B, and D).
- **Constant Velocity Approximation Validity:** Demonstrates that over short lookahead horizons ($T \le 2.0\text{ s}$), pedestrian motion is predominantly unaccelerated along the desired velocity vector $\mathbf{v}_0$, justifying the linear Constant Velocity (CV) Kalman filter and MPPI forward projection model.
- **Evaluation Criteria:** Grounds the Minimum Time-to-Collision ($\text{TTC}_{\min}$) and dynamic clearance buffers used in the 3-way ablation benchmark.

