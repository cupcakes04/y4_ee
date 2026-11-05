# EEEE3054 CW2 — Simple Plan & Summary

> **IMPORTANT PRESENTATION REMINDER:**
> - **Do NOT say "Lecture 2 / Lecture 3 / Lecture 5" during your oral presentation!** Present the formulas, diagrams, and tables naturally as standard engineering design methods (all "Lecture N" text has already been removed from the slide titles, captions, and speaker notes inside `slides_md/`).

---

## 1. Folder Structure Inside `slides_md/`
- **`slides_md/01_...` to `10_...md`:** The 10 individual slide Markdown files.
- **`slides_md/data/`:** All site/climate/resource data and scripts:
  - `fetch_climate_data.py` *(Python script that queries the NASA POWER API, crops `GSA_Report_Dongola.pdf`, and plots the `gwa-plot-data` CSVs)*
  - `GSA_Report_Dongola.pdf` $\rightarrow$ cropped to `gsa_site_info_map.png` & `gsa_monthly_hourly_solar.png`
  - `gwa-plot-data_.../` $\rightarrow$ plotted to `gwa_wind_chart.png`
  - `nasa_power_dongola.csv` $\rightarrow$ plotted to `nasa_temp_rain.png`, `nasa_solar_psh.png`, `nasa_wind_speed.png`
  - `desert.png`, `village.png`, `net_power_profile.png`
- **`slides_md/assets/`:** Cropped reference equations, worked examples, and equipment datasheets:
  - `cw2_fig1_load.png`
  - `lec3_single_phase_diagram.png`, `lec3_pv_sizing_formulas.png`, `lec3_num_modules_formula.png`, `lec3_worked_example3.png`
  - `lec5_bess_block_diagram.png`, `lec5_bess_types_table.png`, `lec5_store_drain_example.png`, `lec5_buyback_example.png`
  - `datasheet_sanyo_hip210.png` (`SANYO HIP-210NKHE1`, $210\text{ Wp}$)
  - `datasheet_fronius_ig.png` (`Fronius IG 40`, $4,410\text{ W}$ DC / $3,500\text{ W}$ AC)

---

## 2. Quick Summary of the Numbers Across the 10 Slides

1. **Daily & Annual Load (Slide 1):**
   - Daily energy $= (0.2 + 1.0 + 2.0 + 1.5 + 0.5 + 0.2) \times 4\text{ h} = \mathbf{21.6\text{ kWh/day}}$ ($\mathbf{7,884\text{ kWh/year}}$).
   - Daytime (`8 to 16`) $= \mathbf{14.0\text{ kWh}}$ ($65\%$); Night/Morning/Evening $= \mathbf{7.6\text{ kWh}}$ ($35\%$).
2. **Site & Resource Data (Slides 2–4, from `GSA_Report_Dongola.pdf` & `gwa-plot-data`):**
   - **Site:** Dongola / Argo Island, Sudan ($19.16^\circ\text{ N}, 30.48^\circ\text{ E}$).
   - **Solar:** $\text{GHI} = 2,335.6\text{ kWh/m}^2\text{/yr}$ ($6.40\text{ PSH/day}$); Tilted $\text{GTI}_{\text{opta}} = \mathbf{2,474.7\text{ kWh/m}^2\text{/yr}}$ ($\mathbf{6.78\text{ PSH/day}}$ at $22^\circ$ tilt); Air Temp $= \mathbf{28.8^\circ\text{C}}$.
   - **Wind:** GWA 100m median wind speed $= \mathbf{8.69\text{ m/s}}$ ($514\text{ W/m}^2$); NASA 10m wind speed $= \mathbf{5.11\text{ m/s}}$.
   - **Hydro, Geothermal, Wave/Tidal:** Self-explanatory unsuitable ($<4\text{ mm/yr}$ rain, flat river, $>600\text{ km}$ from volcano/sea).
3. **PV Array & Inverter Sizing (Slide 6):**
   - $k_{\text{tem\_p\_ave}} = 1 + \left(\frac{-0.30}{100} \times 28.8\right) = \mathbf{0.9136}$
   - $P_{\text{arr\_stc}} = \frac{7,884}{2,474.7 \times 0.943 \times 0.95 \times 0.97 \times 0.95 \times 0.9136} = \mathbf{4,225\text{ Wp}}$
   - $N = \left\lceil \frac{4,225}{210} \right\rceil = \mathbf{21\text{ panels}}$ ($3\text{ parallel} \times 7\text{ series} = \mathbf{4,410\text{ Wp}}$, matching `Fronius IG 40` max DC input of $4,410\text{ W}$).
4. **Battery Sizing (Slide 7):**
   - Night drain $= 0.8 + 4.0 + 2.0 + 0.8 = \mathbf{7.6\text{ kWh}}$.
   - Using $2\text{ kWh}$ Lithium-Ion units: $4\text{ units}$ ($8\text{ kWh}$) minimum for 1 night $\rightarrow$ **$\mathbf{8\text{ units} = 16\text{ kWh}}$** for $2\times$ hospital safety margin.
5. **Costs, Payback, $\text{CO}_2$ & AI Critique (Slides 8–10):**
   - Initial CAPEX $= \mathbf{\$8,500}$; 20-Year Total Cost $= \mathbf{\$17,700}$ (including $\$5,200$ Year 11 replacement + $\$200/\text{yr}$ O&M).
   - Buyback Time $= \frac{\$8,500}{\$2,954/\text{yr}} = \mathbf{2.9\text{ years}}$.
   - 20-Year $\text{CO}_2$ $= \mathbf{7.9\text{ tonnes}}$ (Solar) vs. **$\mathbf{149.8\text{ tonnes}}$** (Diesel) $\rightarrow \mathbf{141.9\text{ tonnes saved}}$ ($94.7\%$).
