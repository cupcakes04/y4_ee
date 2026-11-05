# Reference 08: Diesel Generator Emissions & CAPEX

---

## 1. What is this? (Metrics & Checked Values)
- **Specific Fuel Consumption (SFC):** **$0.30\text{–}0.33\text{ L/kWh}$** (Depco operational range: $0.20\text{–}0.40\text{ L/kWh}$ depending on load factor)
- **Diesel Emission Factor:** **$2.687\text{ kg CO}_2/\text{L}$** (National Environment Agency Singapore / IPCC Standard)
- **Grid Carbon Intensity:** **$0.80\text{–}0.90\text{ kg CO}_2/\text{kWh}$**
- **$3.5\text{ kW}$ Standalone Diesel Generator CAPEX:** **$\$800\text{–}\$1,200\text{ USD}$** (Commercial benchmark: ATO $3.5\text{ kW}$ silent generator $\approx \$1,050$)

---

## 2. The Proof (Screenshots & Technical Excerpts)

| Domain | Screenshot Proof |
| :--- | :--- |
| **Fuel Consumption & Efficiency** | ![Depco Generator Fuel Consumption Guide](sources/08_diesel_emissions_capex/depco_generator_fuel_consumption.png) |
| **Carbon Intensity Factor** | ![Diesel Carbon Intensity Benchmark](sources/08_diesel_emissions_capex/nea_singapore_diesel_emissions_factor.png) |
| **3.5 kW Generator CAPEX** | ![3.5 kW Diesel Generator CAPEX Overview](sources/08_diesel_emissions_capex/diesel_generator_3_5kw_market_capex.png) |

> **Depco Power Systems Fuel Consumption Guide:**
> Typical small diesel generators running at moderate loading ($50\%\text{–}75\%$ load) consume **$0.25\text{–}0.35\text{ litres of diesel per kWh}$**. At light loads ($<25\%$, typical during night clinic hours), efficiency drops further towards $0.40\text{ L/kWh}$.

> **Singapore NEA / UncleESG Carbon Reporting Standard:**
> Direct greenhouse gas combustion emission factor for stationary and automotive diesel fuel:
> $$\mathbf{2.687\text{ kg CO}_2\text{e per litre of diesel}}$$

> **Commercial Equipment Price (ATO / Generic 3.5 kW Genset):**
> Market price for a standalone single-phase $3.5\text{ kW}$ ($4.4\text{ kVA}$) soundproof diesel genset ranges between **$\$800$ and $\$1,200\text{ USD}$**.

---

## 3. How was it calculated?
- **Annual Fuel Consumption for $5,840\text{ kWh/year}$:**
  $$\text{Fuel} = 5,840\text{ kWh} \times 0.32\text{ L/kWh} \approx \mathbf{1,868.8\text{ Litres/year}}$$
- **Gross Diesel Emissions:**
  $$\text{CO}_2 = 1,868.8\text{ L} \times 2.687\text{ kg CO}_2/\text{L} \approx \mathbf{5,021\text{ kg CO}_2/\text{yr}} = \mathbf{5.02\text{ tonnes CO}_2/\text{year}}$$
- **Net Avoided Carbon Emissions (Slide 9):**
  $$\text{Net Avoided CO}_2 = 5.02\text{ t (diesel)} - 0.27\text{ t (solar)} = \mathbf{4.75\text{ tonnes CO}_2/\text{year}}$$
  $$\text{20-Year Lifetime Avoided} = 20 \times 4.75\text{ t} = \mathbf{95.0\text{ tonnes CO}_2}$$
- **Comparison to Generative AI Guess:**
  - AI guessed $\sim 0.85\text{ kg CO}_2/\text{kWh}$ and $\sim 4.96\text{ tonnes/yr}$ ($99.2\text{ tonnes}$ over 20 years).
  - Grounded calculation ($4.75\text{ t/yr}$) proves the AI's emission reduction estimate was accurate within $4.2\%$.

---

## 4. Source Link
- **Depco Fuel Consumption Guide:** [Depco Diesel Generator Fuel Consumption Chart](https://www.depco.com/diesel-fuel-consumption/)
- **NEA / Singapore ESG Factors:** [UncleESG - CO2 Emissions per Litre of Diesel](https://uncleesg.com/co2-per-litre-of-diesel-and-petrol/)
- **ATO Generator Catalog:** [ATO 3.5 kW Diesel Generator Catalog](https://www.ato.com/diesel-generator)
