# Slide 10: Critique of Generative AI & References

---

## 1. Critical Evaluation of AI Results (4 Required Points from CW2 Brief)

| Critique Question (from CW2 Brief) | What We Found When Fact-Checking the AI | How We Fixed It in Our Final Slides |
| :--- | :--- | :--- |
| **1. What did the AI get RIGHT (Reliable)?** | • AI gave realistic solar panel prices ($\sim \$0.30/\text{Wp}$, matching **IRENA 2023**).<br>• AI correctly showed that batteries are the most expensive part of an off-grid solar system, and that solar $\text{CO}_2$ comes only from factory manufacturing. | Kept the solar panel price and the lifecycle $\text{CO}_2$ emission factor ($0.05\text{ kg CO}_2\text{/kWh}$). |
| **2. What did the AI get WRONG or Misleading?** | • **Too-cheap battery price ($\$150/\text{kWh}$):** AI quoted mass-produced electric car battery prices instead of off-grid home/clinic rack batteries (**$\$250/\text{kWh}$**).<br>• **Forgot battery replacement:** AI assumed one battery lasts all 20 years, even though Li-Ion batteries only last **10–15 years**. | Increased battery cost from $\$2,400$ to **$\$4,000$** ($\$250/\text{kWh}$) and added **$\$5,200$ at Year 11** to replace the battery and inverter once. |
| **3. What Hidden Assumptions did the AI make?** | • **Ignored remote Sudan shipping:** AI assumed standard US/Europe free delivery, forgetting it costs extra to transport heavy batteries to rural Northern Sudan.<br>• **Ignored low night-time generator efficiency:** AI assumed a diesel generator runs at peak efficiency 24/7, even when our clinic only needs **$0.2\text{ kW}$ at night**. | Added **$\$1,000$** for remote Sudan transport/installation, and used a realistic **$0.35\text{ L/kWh}$** fuel burn for the diesel generator. |
| **4. Summary of Total Cost Correction** | • **AI Raw 20-Year Cost:** $\$7,420$ *(Unrealistic)* | • **Our Corrected 20-Year Cost:** **$\$17,700$** *(Realistic & verified)* |

*Table 8: Critical evaluation of the Generative AI cost, $\text{CO}_2$, and comparison outputs.*

---

## 2. References & Data Sources

1. **Solar & Climate Data:**
   - **Global Solar Atlas Report:** World Bank / Solargis (2026), Dongola ($19.16^\circ\text{ N}, 30.48^\circ\text{ E}$), report file: [`GSA_Report_Dongola.pdf`](../assets/api/GSA_Report_Dongola.pdf) | [Online Map](https://globalsolaratlas.info).
   - **NASA POWER Agroclimatology / RE Database:** Local climate csv: [`nasa_power_dongola.csv`](../assets/api/nasa_power_dongola.csv) | [Portal](https://power.larc.nasa.gov).
2. **Wind Data:**
   - **Global Wind Atlas Data:** DTU / World Bank (2026), Northern State, Sudan, data folder: [`gwa-plot-data`](../assets/api/gwa-plot-data_2026-11-04179380525039303_14_10_UTC) | [Online Atlas](https://globalwindatlas.info).
3. **Equipment Datasheets:**
   - SANYO `HIP-210NKHE1` HIT Photovoltaic Module Datasheet ($210\text{ Wp}$): [`datasheet_sanyo_hip210.png`](../assets/lectures/datasheet_sanyo_hip210.png).
   - Fronius `IG 15–60` Transformer Inverter Datasheet (`Fronius IG 40`, $4,410\text{ W}$ DC / $3,500\text{ W}$ AC): [`datasheet_fronius_ig.png`](../assets/lectures/datasheet_fronius_ig.png).
4. **Cost, O&M & Economic Benchmarks (Decoupled in `data/`):**
   - **Solar PV Capital Costs:** IRENA (2024), *Renewable Power Generation Costs in 2023* $\rightarrow$ [[Details & Proof: 01_solar_panels_irena.md]](../data/01_solar_panels_irena.md).
   - **Li-Ion Battery Storage Projections:** NREL / NLR (2025), *Cost Projections for Utility-Scale Battery Storage: 2025 Update* $\rightarrow$ [[Details & Proof: 02_battery_storage_nrel.md]](../data/02_battery_storage_nrel.md).
   - **Inverter & BOS Hardware Benchmarks:** NREL Q1 2023 Benchmark & SolarTopStore quote $\rightarrow$ [[Details & Proof: 03_inverter_controller_fronius_nrel.md]](../data/03_inverter_controller_fronius_nrel.md).
   - **Sudan Supply Chain & Remote Logistics:** UNDP Sudan (May 2024), *Solar Energy Value Chains in Sudan* $\rightarrow$ [[Details & Proof: 04_bos_cables_sudan_delivery_undp.md]](../data/04_bos_cables_sudan_delivery_undp.md).
   - **PV Maintenance & Desert Soiling:** PV-Maps O&M Benchmarks & QEERI Qatar Desert Soiling Study $\rightarrow$ [[Details & Proof: 05_opex_maintenance_desert_soiling.md]](../data/05_opex_maintenance_desert_soiling.md).
   - **Diesel Generation Economics & Crisis Baseline:** World Bank / ESMAP Mini-Grids & Power for All Fact Sheet $\rightarrow$ [[Details & Proof: 06_diesel_baseline_cost_esmap_undp.md]](../data/06_diesel_baseline_cost_esmap_undp.md).
   - **Battery Life & Cycle Standards:** Korea Battery Industry Association (2017), *Energy Storage System Technology and Business Model*.
5. **$\text{CO}_2$ Lifecycle & Generator Engineering Benchmarks (Decoupled in `data/`):**
   - **Solar PV Lifecycle Carbon Intensity:** NREL / NLR (2013), *Life Cycle Greenhouse Gas Emissions from Solar Photovoltaics* $\rightarrow$ [[Details & Proof: 07_solar_co2_lifecycle_nrel.md]](../data/07_solar_co2_lifecycle_nrel.md).
   - **Diesel Fuel $\text{CO}_2$ Factor & Specific Fuel Burn:** Singapore NEA Carbon Guidelines ($2.687\text{ kg CO}_2/\text{L}$) & Depco Generator Efficiency ($0.35\text{ L/kWh}$) $\rightarrow$ [[Details & Proof: 08_diesel_generator_emissions_and_capex.md]](../data/08_diesel_generator_emissions_and_capex.md).

---

### What to Say (Speaker Notes)
- **Reliable AI Output:** Accurately predicted solar panel costs (~$0.30/Wp) and identified zero operating emissions.
- **Unreliable AI Output:** Quoted EV battery pricing ($150/kWh vs $250/kWh rack units) and assumed zero mid-life replacements.
- **Hidden Assumptions:** Omitted Sudan remote transport ($1,800) and assumed 100% generator efficiency during 0.2 kW night load.
- **Cost Correction:** Adjusted AI's raw 20-year estimate of $7,420 to verified turnkey cost of **$17,700**.
- **Key References:** Global Solar Atlas, NASA POWER, IRENA (2024), NREL BESS (2025), UNDP Sudan (2024).
