# Reference 02: Battery Energy Storage Costs

---

## 1. What is this? (Component & Checked Cost)
- **Component:** $15.5\text{ kWh}$ Lithium-Ion (LFP) Battery Energy Storage System (BESS)
- **Checked Cost:** **$\$3,800\text{ USD}$** ($\sim \$245\text{–}\$247/\text{kWh}$)
- **Expected Lifetime:** **$10\text{–}15\text{ years}$** ($\sim 4,000\text{–}6,000\text{ cycles}$ at $80\%\text{ DoD}$)

---

## 2. The Proof (Screenshot & Verbatim Excerpt)

![NREL/NLR Battery Storage Cost Projections Abstract](sources/02_battery_storage/nrel_2025_bess_cost_abstract.png)
*Figure 2: Verbatim abstract from NREL/NLR 2025 Utility-Scale Battery Storage Cost Projections.*

> **Verbatim Abstract Excerpt:**
> "Under the moderate scenario: 4-hour battery system costs decline from **$247/kWh** in 2024 to **$190/kWh** in 2030, a **23% decrease**."

---

## 3. How was it calculated?
- **Our Usable Storage Sized:** $12.4\text{ kWh}$ (matches night-time medical load profile)
- **Total Nameplate Sizing at $80\%\text{ DoD}$:**
  $$\text{Capacity} = \frac{12.4\text{ kWh}}{0.80} = 15.5\text{ kWh}$$
- **Capital Cost Calculation:**
  $$\text{BESS Cost} = 15.5\text{ kWh} \times \$247/\text{kWh} = \$3,828.50 \approx \mathbf{\$3,800\text{ USD}}$$
- **Comparison to Generative AI Guess:**
  - AI estimated $\$300/\text{kWh}$ ($\$3,720$ for $12.4\text{ kWh}$).
  - Verified NREL moderate benchmark reflects recent 2024/2025 cost deflation to $\$247/\text{kWh}$.

---

## 4. Source Link
- **National Laboratory Research Hub (NLR / NREL):** [Cost Projections for Utility-Scale Battery Storage: 2025 Update (PDF)](https://www.nlr.gov/docs/fy25osti/93281.pdf)
- **Research Hub Portal:** [NLR Battery Cost Projections Hub](https://research-hub.nlr.gov/en/publications/cost-projections-for-utility-scale-battery-storage-2025-update)
