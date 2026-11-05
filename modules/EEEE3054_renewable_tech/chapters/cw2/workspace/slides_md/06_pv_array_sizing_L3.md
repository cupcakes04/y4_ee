# Slide 6: Sizing the Solar PV Array & Inverter

---

## 1. PV Array Sizing Equations & Reference Worked Method

| PV Array Sizing Equations | Reference Calculation Method |
| :---: | :---: |
| ![PV Sizing Formulas](../assets/lectures/lec3_pv_sizing_formulas.png) | ![Worked Example 3](../assets/lectures/lec3_worked_example3.png) |

*Figure 8: Energy-constraint PV array sizing equations and reference calculation steps.*

---

## 2. Selected Equipment Datasheets

| SANYO `HIP-210NKHE1` Module ($210\text{ Wp}$) | Fronius `IG 40` Inverter ($3,500\text{ W}$ AC / $4,410\text{ W}$ DC) |
| :---: | :---: |
| ![Sanyo HIP 210 Datasheet](../assets/lectures/datasheet_sanyo_hip210.png) | ![Fronius IG Datasheet](../assets/lectures/datasheet_fronius_ig.png) |

*Figure 9: Electrical specifications for the selected SANYO `HIP-210NKHE1` PV panel and Fronius `IG 40` inverter.*

---

## 3. Step-by-Step Sizing Calculation Using Global Solar Atlas Data

1. **Annual Energy Required ($E_{\text{req}}$):**
   $$E_{\text{req}} = 21.6\text{ kWh/day} \times 365\text{ days} = \mathbf{7,884\text{ kWh/year}} \quad (\varepsilon = 100\%\text{ off-grid})$$
2. **Temperature De-Rating Factor ($k_{\text{tem\_p\_ave}}$):**
   - From SANYO datasheet: $\beta_{\text{power}} = -0.30\%/^\circ\text{C}$. From Global Solar Atlas (Slide 3): $T_{\text{amb}} = 28.8^\circ\text{C}$:
   $$k_{\text{tem\_p\_ave}} = 1 + \left[ \left(\frac{-0.30}{100}\right) \times 28.8 \right] = 1 - 0.0864 = \mathbf{0.9136}$$
3. **Minimum PV Array Power at STC ($P_{\text{arr\_stc}}$):**
   - Using Global Solar Atlas tilted irradiation $\text{PSH} = 2,474.7\text{ h/year}$ ($6.78\text{ h/day}$ at $22^\circ$ tilt), Fronius IG 40 max efficiency $\eta_{\text{inv}} = 0.943$, cable efficiency $\eta_{\text{cab}} = 0.95$, dirt factor $k_{\text{dir}} = 0.97$, and mismatch $k_{\text{mm}} = 0.95$:
   $$P_{\text{arr\_stc}} = \frac{7,884}{2,474.7 \times 0.943 \times 0.95 \times 0.97 \times 0.95 \times 0.9136} = \frac{7,884}{1,865.9} = \mathbf{4.225\text{ kWp}} \quad (\mathbf{4,225\text{ Wp}})$$
4. **Number of SANYO `HIP-210NKHE1` ($210\text{ Wp}$) Panels & Inverter Match:**
   $$N_{\text{min\_mod}} = \left\lceil \frac{4,225\text{ Wp}}{210\text{ Wp}} \right\rceil = \left\lceil 20.12 \right\rceil = \mathbf{21\text{ modules}} \quad (3\text{ parallel strings} \times 7\text{ series modules})$$
   - **Total Array Power:** $21 \times 210\text{ Wp} = \mathbf{4,410\text{ Wp}}$ ($4.41\text{ kWp}$) $\rightarrow$ **Matches the `Fronius IG 40` max DC power ($4,410\text{ W}$) and $3,500\text{ W}$ AC output!**

---

### What to Say (Speaker Notes)
- **Annual Energy Target:** $E_{\text{req}} = 21.6\text{ kWh/day} \times 365\text{ days} = \mathbf{7,884\text{ kWh/year}}$.
- **Temperature Derate:** $k_{\text{tem\_p\_ave}} = 1 + (-0.003 \times 28.8^\circ\text{C}) = \mathbf{0.9136}$ (based on $-0.30\%/^\circ\text{C}$ SANYO coeff).
- **Minimum Array Sizing:** $P_{\text{arr\_stc}} = \frac{7,884}{2,474.7 \times 0.943 \times 0.95 \times 0.97 \times 0.95 \times 0.9136} = \mathbf{4,225\text{ Wp}}$.
- **Module Configuration:** $\lceil 4,225 / 210 \rceil = \mathbf{21\text{ panels}}$ (3 parallel strings × 7 series modules = **4,410 Wp**).
- **Inverter Match:** Fronius IG 40 rated DC input (4,410 W) matches array exactly; 3,500 W AC easily handles 2.0 kW peak load.
