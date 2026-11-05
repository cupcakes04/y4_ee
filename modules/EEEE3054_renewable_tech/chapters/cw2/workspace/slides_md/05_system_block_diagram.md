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
- "Slide 5 shows how our off-grid system is connected, combining a standard single-phase PV protection layout with a Battery Energy Storage System (BESS)."
- "In Figure 7, sunlight hits our **21 SANYO 210W solar panels (4.41 kWp total)**."
- "During the daytime (8 AM to 4 PM), **14.0 kWh** goes straight through our **Fronius IG 40 inverter** to run the health centre."
- "At the same time, the extra **7.6 kWh** generated during the day is stored inside our **Lithium-Ion battery bank**, and then drained at night (4 PM to 8 AM) so the clinic has 24-hour power totaling **21.6 kWh/day**."
