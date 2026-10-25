# Exploratory Track 02: Planar Inverse Perspective Mapping (IPM) & Nav2 Costmap Filters

> **Archive Status**: EXPLORATORY MATHEMATICAL FORMULATION / PARKED OUTSIDE ASSESSED SCOPE.  
> **Associated Literature**: Zhang & Pless (2004), Nav2 Costmap Filters Documentation.

---

## 1. Planar Homography Formulation

To translate 2D visual segmentation masks of floor phenomena into metric spatial boundaries without requiring a dense depth camera, this exploratory module formulated an analytical planar **Inverse Perspective Mapping (IPM)** under the flat-ground assumption ($Z_w = 0$).

Given a calibrated monocular camera with intrinsic matrix $\mathbf{K}$ and camera pose $[\mathbf{R} \mid \mathbf{t}]$ relative to the robot base footprint frame:

$$\mathbf{p}_{\text{pixel}} = \lambda \mathbf{K} \left( \mathbf{r}_1 X_w + \mathbf{r}_2 Y_w + \mathbf{t} \right) = \mathbf{H} \begin{bmatrix} X_w \\ Y_w \\ 1 \end{bmatrix}$$

Because the ground plane is locally flat ($Z_w = 0$), the transformation reduces to a non-singular $3 \times 3$ planar homography matrix $\mathbf{H} = \mathbf{K} [\mathbf{r}_1, \mathbf{r}_2, \mathbf{t}]$. Inverting $\mathbf{H}$ yields the exact ground coordinates $(X_w, Y_w)$ deterministically in $<0.2\text{ ms}$:

$$\begin{bmatrix} X_w \\ Y_w \\ 1 \end{bmatrix} \sim \mathbf{H}^{-1} \begin{bmatrix} u \\ v \\ 1 \end{bmatrix}$$

---

## 2. Polygon Simplification & Nav2 Costmap Filter Injection

1. **Contour Extraction & Simplification:**
   - Pixel boundaries extracted from the student segmentation model are projected via $\mathbf{H}^{-1}$ into metric ground polygons.
   - To avoid streaming excessive vertex data over ROS 2 topics, the Douglas-Peucker polyline simplification algorithm reduces the polygon to its minimal convex hull or piecewise-linear representation with tolerance $\epsilon = 0.05\text{ m}$.
2. **Dynamic Costmap Filter Injection:**
   - Polygons are published to ROS 2 `nav2_costmap_2d::CostmapFilterInfo` topics.
   - **Keepout Zones:** Injected into Nav2 costmap filter layers to dynamically assign lethal cost ($C = 254$) over fluid hazard polygons, forcing local planners to detour around the spill.
   - **Speed Limits:** Injected to dynamically restrict AMR linear velocities within slippery surface zones.

---

## 3. Why This Track Was Parked

1. **Susceptibility to Ground Pitch Variations:**  
   Analytical IPM strictly assumes an invariant ground plane ($Z=0$). Small angular pitch variations ($>1.5^\circ$) caused by robot acceleration, deceleration, or minor floor unevenness cause significant spatial projection distortion at distances beyond $4\text{ m}$.
2. **Outside Supervisor Specification:**  
   The core research specification (`SD-MEng-26-01`) concentrates on dynamic obstacle interactions (pedestrians, carts) crossing the robot's route, which are tracked via planar LiDAR ray gating rather than ground-plane homography.

