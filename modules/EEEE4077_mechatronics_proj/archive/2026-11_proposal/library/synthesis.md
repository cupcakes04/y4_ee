# Thematic Literature Review Synthesis

This document synthesizes the academic literature and industrial state of the art supporting the dissertation, organized into four primary technical pillars and an exploratory context note.

---

## Pillar 1: Multi-Modal Sensor Fusion & Metric Dynamic Tracking

Autonomous mobile robots operating in brownfield logistics environments face severe perceptual constraints when relying solely on 2D safety LiDARs. While single-plane laser scanners provide high-precision distance measurements ($<1\text{ cm}$ accuracy) over wide operational sweeps ($360^\circ$ at $20\text{--}40\text{ Hz}$), they collapse three-dimensional physical structures into sparse, disconnected planar point clusters. When human pedestrians cross the scan plane, the sensor records isolated reflections (cross-sections of lower limbs) without photometric features or volumetric boundaries.

To overcome point fragmentation and semantic blindness without escalating hardware costs to multi-channel 3D LiDAR arrays, late-fusion architectures combining planar LiDAR with monocular RGB cameras represent an optimal trade-off:
1. **Geometric Transformation:** The spatial relationship between planar laser scanners and cameras is grounded in the checkerboard extrinsic calibration technique developed by Zhang and Pless [L5]:
   $$\lambda \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = \mathbf{K} \left( \mathbf{R} \begin{bmatrix} X_{\text{lidar}} \\ Y_{\text{lidar}} \\ 0 \end{bmatrix} + \mathbf{t} \right)$$
   Projecting laser scan points into calibrated image coordinates establishes an associative bridge between visual detections and metric ranges.
2. **Visual Association in Image Space:** Modern multi-object tracking architectures such as ByteTrack (Zhang et al. [L13]) associate both high-score and low-score bounding boxes across frames using 2D motion and IoU overlap. By maintaining persistent identities (`track_id`) directly in image space, the system bridges transient visual occlusions and avoids fragile combinatorial clustering on raw laser point clouds.
3. **Metric State Filtering:** Gating planar laser returns through visual bounding frustums isolates target depth from background wall reflections. Filtering these gated metric returns through a linear discrete Kalman filter with a Constant Velocity (CV) model (Thrun et al. [L12]) produces smooth, continuous state vectors $[x, y, v_x, v_y]^T$ and uncertainty covariances at low computational cost.

---

## Pillar 2: The Freezing Robot Problem & Predictive MPPI Control

In conventional mobile navigation stacks—including standard configurations of the ROS 2 Navigation stack (Nav2 [L2, L3])—sensor returns are registered directly into a 2D occupancy grid (`nav2_costmap_2d`). In dynamic environments, this design creates the classic **"Freezing Robot Problem"** formalized by Trautman and Krause [L1]: the robot treats moving agents as immovable barriers, triggering abrupt decelerations, repeated recovery rotations, and mission aborts.

While Model Predictive Path Integral (MPPI) control (Williams et al. [L4], Macenski et al. [L11]) has emerged as the premier local trajectory planner in Nav2, an architectural analysis reveals a fundamental limitation:
- All 11 default trajectory critics shipped with `nav2_mppi_controller` evaluate obstacles strictly against the static 2D costmap.
- Because the costmap is time-invariant ($t = 0$), the optimizer cannot evaluate where a dynamic obstacle will be at lookahead horizon $\tau \in [0.5, 2.0]\text{ s}$.
- Consequently, standard MPPI either halts prematurely because an obstacle currently blocks the corridor (false positive), or accelerates into the future crossing path of an oncoming vehicle (blind interception).

To resolve this limitation without discarding Nav2's robust infrastructure, dynamic obstacle states must be incorporated directly into the trajectory rollout evaluation. Formulating a custom **dynamic obstacle critic plugin** that forward-projects dynamic obstacle positions across each sampled rollout ($\mathbf{p}_{\text{obs}}(\tau) = \mathbf{p}_0 + \mathbf{v}_{\text{obs}} \tau$) enables the MPPI optimizer to proactively yield, slow down, or execute smooth evasive deflections.

### 2.1 Advanced MPPI Variants and the Modern Landscape

Recent literature explores several advanced avenues to address standard MPPI pathologies:
1. **Analytical Safety Filters via Control Barrier Functions (SE-MPPI [L15]):** Kang introduces a Nav2-native controller combining online local-minima escape with a QP-based Control Barrier Function (CBF) filter. Rather than modifying rollout costs, SE-MPPI leaves MPPI's stochastic sampling unchanged and projects the synthesized command $\mathbf{u}_0^*$ onto a safe control set via quadratic programming. While mathematically guaranteeing forward invariance for known stationary or moving boundaries, QP safety filters require exact barrier constraints and do not proactively reshape rollouts over the multi-second preview horizon.
2. **Continuous Geometric Representation via JAX GPU Rollouts (EXACT-MPPI [L16]):** Peng et al. bypass discrete occupancy grids entirely, calculating exact Signed Distance Functions (SDF) between arbitrary non-convex robot footprints and raw point clouds in parallel via JAX CUDA kernels. While EXACT-MPPI demonstrates high geometric fidelity for irregular chassis, it shifts the runtime execution to Python/JAX on an edge GPU, abandoning standard Nav2 plugin modularity and assuming unsegmented metric point clouds rather than semantic dynamic tracking.
3. **Multi-Modal Trajectory Clustering (CSC-MPPI [L17]):** RCILab (IROS 2025) identifies the classic MPPI *mode-averaging collapse*—where symmetrical obstacle encounters cause left- and right-swerving rollouts to be averaged into a fatal centerline collision. CSC-MPPI mitigates this by running DBSCAN clustering on GPU memory (cuML) to isolate distinct topological modes and solving primal-dual constrained sampling.

**Synthesis with Our Approach:** These works represent high-performance methodological counterparts, but target different failure axes. EXACT-MPPI addresses complex geometric footprints, CSC-MPPI addresses symmetrical mode averaging, and SE-MPPI enforces reactive hard boundaries. In contrast, our project targets the **brownfield perception-planning gap**: retrofitting widely deployed, CPU-constrained 2D LiDAR AMRs with monocular vision tracking, and guiding the standard Nav2 C++ controller via spatio-temporal cost shaping where dynamic velocity vectors naturally break trajectory symmetry without requiring heavy GPU clustering or external QP solvers.

---

## Pillar 3: Pedestrian Dynamics & 3-Way Comparative Ablation

Accurate motion prediction over short planning horizons is grounded in pedestrian dynamics literature. The foundational Social Force Model introduced by Helbing and Molnar [L14] demonstrates that:
- Normal human walking speed centers around $1.2\text{--}1.4\text{ m/s}$ along a characteristic desired velocity vector $\mathbf{v}_0$.
- Over short preview horizons ($T \le 2.0\text{ s}$), pedestrian motion exhibits high directional inertia and is predominantly unaccelerated. This mathematically justifies using a linear Constant Velocity (CV) model for both state filtering [L12] and MPPI rollout evaluation, avoiding the latency and memory overhead of deep neural trajectory transformers on edge hardware.

To rigorously substantiate performance claims, the supervisor specification (`SD-MEng-26-01`) mandates an **ablation study** that isolates the contribution of visual object detection from motion prediction:
- **C0 (Baseline):** 2D LiDAR only with default static MPPI critics.
- **C1 (Vision Detection Only):** 2D LiDAR + Camera detection, evaluating obstacles as static clearance circles at $t = 0$ without temporal forward projection.
- **C2 (Full Predictive MPPI):** 2D LiDAR + Camera tracking with Kalman filtering and forward temporal motion extrapolation.

This 3-way comparative design provides defensible empirical evidence detailing whether visual bounding alone mitigates freezing, or whether predictive motion modeling is necessary to achieve smooth, proactive yielding in dynamic cross-traffic.

---

## Pillar 4: Commercial Scale & Brownfield Retrofit Imperative

The practical necessity of retrofitting existing brownfield AMRs is substantiated by commercial robotics market data. According to the International Federation of Robotics (IFR) [L9], professional service robot deployments are dominated by the transportation and logistics sector, which registered over 102,900 commercial units in 2024 (a 14% year-on-year increase). 

The vast majority of these logistics AMRs are deployed in cost-sensitive mid-tier warehousing and manufacturing facilities where replacing 2D LiDAR fleets with high-end 3D perception arrays is financially prohibitive. A retrofit framework combining low-cost monocular vision with existing planar LiDAR and predictive MPPI control addresses this exact commercial demand.

---

## Contextual Note: Archived Exploratory Track (chapters/explore/)

In parallel exploratory investigations formally archived in `chapters/explore/` (`01_vlm_hazard_distillation.md` and `02_planar_ipm_homography.md`), the use of vision-language foundation models (Florence-2 [L6], Grounded-SAM [L7], and ViLAM [L8]) was studied for detecting transient non-geometric surface hazards ($Z \approx 0$, e.g. fluid spills) and projecting keepout zones via planar homography to Nav2 Costmap Filters [L10]. This work was decoupled from the assessed engineering scope to ensure 100% focus on the core dynamic tracking and predictive MPPI control pipeline.
