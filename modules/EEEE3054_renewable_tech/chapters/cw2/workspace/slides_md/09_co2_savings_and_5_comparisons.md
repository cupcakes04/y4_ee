# Slide 9: $\text{CO}_2$ Emissions Savings & 5 System Comparisons

---

## 1. Simple 20-Year $\text{CO}_2$ Emissions Calculation (Solar PV vs. Diesel Generator)

- **Total Energy Used by Clinic in 20 Years:**
  $$E_{20\text{yr}} = 7,884\text{ kWh/year} \times 20\text{ years} = \mathbf{157,680\text{ kWh}}$$

| System | How $\text{CO}_2$ is Produced | Emission Factor (IPCC / NREL) | Total 20-Year $\text{CO}_2$ Emissions |
| :--- | :--- | :---: | :---: |
| **1. Our Solar PV + Li-Ion Battery System** | **$0\text{ kg}$ during operation** (no fuel burned). Only factory manufacturing emissions for panels & batteries. | $\approx \mathbf{0.05\text{ kg CO}_2\text{/kWh}}$<br>($50\text{ g/kWh}$ lifecycle) | $157,680 \times 0.05 = \mathbf{7,884\text{ kg}}$<br>(**$7.9\text{ tonnes CO}_2$**) |
| **2. Fossil-Fuel System (Diesel Generator)** | Burns $\approx 0.35\text{ Litres}$ of diesel per kWh ($55,188\text{ L}$ total over 20 yrs $\times 2.68\text{ kg CO}_2\text{/L}$). | $\approx \mathbf{0.95\text{ kg CO}_2\text{/kWh}}$<br>($950\text{ g/kWh}$) | $157,680 \times 0.95 = \mathbf{149,796\text{ kg}}$<br>(**$149.8\text{ tonnes CO}_2$**) |
| **Net $\text{CO}_2$ Saved by Using Solar PV** | — | — | **$149.8 - 7.9 = \mathbf{141.9\text{ tonnes CO}_2\text{ saved}}$ ($94.7\%$ reduction!)** |

*Table 6: Calculation of 20-year lifecycle $\text{CO}_2$ emissions and total carbon savings.*

---

## 2. Five Comparisons: Proposed Solar PV + Battery vs. Diesel Generator
*(CW2 Brief requires **more than 4** numerical comparisons and stating clearly which system performs better).*

| # | Comparison Criterion | **Proposed Solar PV + Li-Ion System** | **Diesel Generator System** | Which System Performs Better? |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Initial Start-Up Cost (CAPEX)** | **$\$8,500$** (higher upfront cost to buy panels & batteries). | **$\$1,800$** (cheap to buy a small $3.5\text{ kW}$ diesel generator). | **Diesel performs better** on initial start-up cost ($79\%$ cheaper upfront). |
| **2** | **Annual Running & Fuel Cost** | **$\$200\text{/year}$** ($0\text{ L}$ fuel; just wiping dust off panels). | **$\$3,150\text{/year}$** ($\sim 2,760\text{ L/yr}$ diesel fuel + oil & filter changes). | **Solar PV performs better** ($94\%$ cheaper to run every year). |
| **3** | **20-Year Total Cost** | **$\$17,700$** total over 20 years ($\approx \mathbf{\$0.11/\text{kWh}}$). | **$\$68,400$** total over 20 years ($\$1.8\text{k}$ + $\$63\text{k}$ fuel + $\$3.6\text{k}$ replacements $\approx \mathbf{\$0.43/\text{kWh}}$). | **Solar PV performs better** (saves **$\$50,700$** over 20 years!). |
| **4** | **20-Year $\text{CO}_2$ Emissions** | **$7.9\text{ tonnes CO}_2$** (factory manufacturing only; zero smoke). | **$149.8\text{ tonnes CO}_2$** (from burning $55,188\text{ L}$ of diesel fuel). | **Solar PV performs better** (cuts carbon emissions by **$94.7\%$**). |
| **5** | **Noise & Fuel Supply Security** | **$0\text{ dB}$ completely silent**; uses free daily Sudan sunshine. | **$75\text{–}85\text{ dB}$ loud engine noise** 24/7 next to patients; blacks out if fuel trucks get stuck. | **Solar PV performs better** for hospital quietness and reliable supply. |

*Table 7: Five numerical comparisons between the proposed Solar PV + Battery system and a Diesel Generator.*

### References & Verification Proofs for Slide 9 (Decoupled in `data/`)

1. **Clinic 20-Year Electricity Demand:**
   - Source: Slide 1 daily clinic load profile ($21.6\text{ kWh/day}$).
   - Calculation: $21.6\text{ kWh/day} \times 365\text{ days/year} \times 20\text{ years} = \mathbf{157,680\text{ kWh}}$.
2. **Solar Lifecycle Emissions Factor ($50\text{ g CO}_2/\text{kWh} \rightarrow 7.9\text{ t CO}_2$):**
   - Source: NREL / NLR Lifecycle Assessment Report (*Life Cycle Greenhouse Gas Emissions from Solar Photovoltaics*).
   - Median harmonized lifecycle intensity is $\approx 46\text{ g CO}_2\text{e/kWh}$, supporting our conservative $0.05\text{ kg CO}_2/\text{kWh}$ ($7.9\text{ tonnes CO}_2$). See detailed proof & chart in [`data/07_solar_co2_lifecycle_nrel.md`](../data/07_solar_co2_lifecycle_nrel.md).
3. **Diesel Generator Fuel Burn ($0.35\text{ L/kWh}$) & Fuel $\text{CO}_2$ Factor ($2.687\text{ kg CO}_2/\text{L} \rightarrow 149.8\text{ t CO}_2$):**
   - Sources: Depco Power Systems ($0.2\text{–}0.4\text{ L/kWh}$ SFC) & Singapore NEA Carbon Guidelines ($2.687\text{ kg CO}_2/\text{L}$).
   - Produces $\approx 0.95\text{ kg CO}_2/\text{kWh}$ ($149.8\text{ tonnes CO}_2$). See detailed proof & screenshots in [`data/08_diesel_generator_emissions_and_capex.md`](../data/08_diesel_generator_emissions_and_capex.md).
4. **Economic Baseline & 5 Numerical Comparisons:**
   - Generator CAPEX ($\$1,800$), fuel operating cost ($\$0.40/\text{kWh} \rightarrow \$3,150/\text{yr}$), and remote African diesel LCOE benchmark ($\$0.35\text{–}0.70/\text{kWh}$) documented in [`data/06_diesel_baseline_cost_esmap_undp.md`](../data/06_diesel_baseline_cost_esmap_undp.md) & [`data/08_diesel_generator_emissions_and_capex.md`](../data/08_diesel_generator_emissions_and_capex.md).

---

### What to Say (Speaker Notes)
- **Lifecycle $\text{CO}_2$ Balance:** Solar lifecycle **7.9 tonnes $\text{CO}_2$** (50 g/kWh) vs. Diesel **149.8 tonnes $\text{CO}_2$** (55,188 L fuel) $\rightarrow$ **141.9 tonnes $\text{CO}_2$ saved (94.7% cut)**.
- **1. Initial CAPEX:** Diesel performs better ($1,800 vs $8,500; 79% cheaper upfront).
- **2. Annual OPEX:** Solar performs better ($200/yr vs $3,150/yr; 94% cheaper to operate).
- **3. 20-Year Total Cost:** Solar performs better ($17,700 vs $68,400; saves $50,700).
- **4. $\text{CO}_2$ Footprint:** Solar performs better (7.9 t vs 149.8 t).
- **5. Clinic Quiet & Reliability:** Solar performs better (0 dB silent vs 80 dB engine noise; no fuel convoy risk).

