# Slide 5: Proposed Off-Grid Solar + Battery System Diagram

---

## 1. Reference Single-Phase PV & Battery Storage Architecture

| Single-Phase PV Connection Layout | Battery Energy Storage System (BESS) Layout |
| :---: | :---: |
| ![Single Phase PV System](../assets/lectures/lec3_single_phase_diagram.png) | ![BESS Block Diagram](../assets/lectures/lec5_bess_block_diagram.png) |

*Figure 6: Standard single-phase PV protection/switching layout (left) and BESS control block diagram (right).*

---

## 2. Custom Off-Grid Health Centre System Diagram & Energy Flow

```mermaid
flowchart LR
    SUN["Sunlight at Dongola<br/>GTI = 6.78 PSH/day<br/>(2,474.7 kWh/m²/yr)"] -->|"21 × 210 Wp Panels<br/>(SANYO HIP-210NKHE1)<br/>Total = 4.41 kWp"| PV["PV Array Output<br/>(After Temp, Dirt,<br/>Cable & Mismatch Losses)"]
    
    PV -->|"DC Cable (η = 95%)<br/>& Charge Controller"| BUS["DC Bus / Split<br/>Total Usable:<br/>~21.6 kWh/day"]
    
    BUS -->|"Daytime (8am–4pm)<br/>Supplies 14.0 kWh"| INV["Fronius IG 40 Inverter<br/>(DC to 230V AC, 50Hz)<br/>Max η = 94.3%"]
    
    BUS <-->|"Day: Stores 7.6 kWh<br/>Night: Drains 7.6 kWh<br/>(Li-Ion η = 95%)"| BATT["Li-Ion Battery Bank<br/>8 × 2 kWh = 16 kWh<br/>(Covers 7.6 kWh Night<br/>+ Extra Backup)"]
    
    INV -->|"Total Delivered:<br/>21.6 kWh/day AC<br/>(Peak = 2.0 kW)"| LOAD["Health Centre Load<br/>Lights, Fridges,<br/>Medical Tools"]
```
*Figure 7: Custom off-grid system diagram showing main components, efficiencies, and daily energy flow.*

---

### What to Say (Speaker Notes)
- **Architecture:** DC-coupled hybrid PV + battery feeding a single-phase 230V AC, 50 Hz inverter.
- **Solar Generation:** 21 × SANYO 210W modules (**4.41 kWp STC**) mounted at 22° South tilt.
- **Daytime Power Flow:** 14.0 kWh routed directly to clinic loads via Fronius IG 40 inverter (94.3% eff).
- **Storage Power Flow:** 7.6 kWh excess solar charges Li-Ion battery (95% round-trip eff) to sustain 7.6 kWh night load.
