# UAV Airframe Architectures

**Subject:** AERO3012 — Autonomous Aerial Systems & Flight Dynamics

**Date:** September 30, 2026

## What it is

UAV airframe architectures define how an unmanned aircraft generates lift, maneuvers, and expends energy. The four core types—Fixed-Wing, Single-Rotor Helicopter, Multirotor, and Hybrid VTOL—represent distinct mechanical trade-offs between static hover precision and aerodynamic cruising efficiency.

| Airframe Type | Lift Mechanism | Hover Capability | Energy Efficiency (Cruise) | Mechanical Complexity |
| --- | --- | --- | --- | --- |
| **Fixed-Wing** | Airflow over static airfoils | None | Maximum ($L/D \approx 15\text{--}20$) | Low |
| **Single-Rotor** | Dynamic blade pitch variation | High (large disc area) | Moderate | High (swashplate + linkages) |
| **Multirotor** | Direct thrust from multiple props | Moderate (high disc loading) | Lowest ($T \ge W$ continuously) | Low (direct-drive BLDC) |
| **Hybrid VTOL** | Blended (rotors hover $\rightarrow$ wing cruise) | High (takeoff/landing only) | High | High (tilt actuators or dead mass) |

## Key Points

* **Fixed-Wing:** Thrust only needs to overcome total drag ($T = D$), allowing extended range and flight endurance measured in hours.
* **Fixed-Wing:** Requires forward airspeed ($v > v_{\text{stall}}$) to maintain lift; cannot hover, turn in place, or operate in tight vertical corridors.
* **Single-Rotor Helicopter:** A large rotor diameter reduces induced velocity, giving it higher hover efficiency per unit mass than multirotors.
* **Single-Rotor Helicopter:** High mechanical vulnerability; failure in swashplate linkages, drive belts, or gearboxes causes catastrophic loss of control.
* **Multirotor:** Generates pitch, roll, and yaw moments purely through differential motor RPM, eliminating control surfaces and mechanical linkages.
* **Multirotor:** Suffers extreme endurance penalties because small propeller disc areas demand constant high current draw to counter gravity ($T \ge W$).
* **Hybrid VTOL:** Combines zero-infrastructure runway-free operation with fixed-wing aerodynamic transit speeds.
* **Hybrid VTOL:** Lift-and-cruise architectures carry inactive hover motors as dead weight during cruise, whereas tilt-rotor designs introduce critical mechanical pivot failure points.

## Key Equations (if any)

$$L = \frac{1}{2} \rho v^2 S C_L$$

* $L$ $\rightarrow$ Aerodynamic lift force (N)
* $\rho$ $\rightarrow$ Air density ($\text{kg/m}^3$)
* $v$ $\rightarrow$ True airspeed ($\text{m/s}$)
* $S$ $\rightarrow$ Wing planform area ($\text{m}^2$)
* $C_L$ $\rightarrow$ Lift coefficient (dimensionless)

$$P_{\text{induced}} = \frac{T^{3/2}}{\sqrt{2 \rho A}}$$

* $P_{\text{induced}}$ $\rightarrow$ Induced power required to hover (W)
* $T$ $\rightarrow$ Total thrust generated, equal to weight $W$ in steady hover (N)
* $\rho$ $\rightarrow$ Air density ($\text{kg/m}^3$)
* $A$ $\rightarrow$ Total rotor disc actuator area, $\pi R^2$ ($\text{m}^2$)

## Watch Out For

* Assuming higher propeller count equals higher hover efficiency: multirotors have significantly smaller disc area ($A$) than a single-rotor helicopter of equal mass, which drastically increases induced power demand ($P_{\text{induced}} \propto 1/\sqrt{A}$).
* Treating Hybrid VTOL transition as purely binary: the transition corridor requires managing a dangerous envelope where airspeed is below wing stall speed while rotor tilt reduces pure vertical thrust support.
* Confusing thrust with lift on fixed-wing platforms: the motor does not lift the aircraft against gravity; it overcomes aerodynamic drag to maintain the forward airspeed needed for the wing to generate lift.