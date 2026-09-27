To maximize throughput and retention in final-year Electrical Engineering using software engineering principles, the study workflow should be treated as an **ETL (Extract, Transform, Load) and Verification pipeline**.

A frequent anti-pattern in engineering study workflows is **tightly coupled ingestion and memorization**: reading raw slide decks linearly, attempting to retain un-normalized slide layouts, or copying formulas without parsing the underlying hardware dynamics.

---

### System Architecture: The EE Knowledge Pipeline

```
[Raw Ingestion Layer]  -->  [Parsing & Normalization]  -->  [Domain Model / Core MD]  -->  [Verification / Test Harness]
(PDFs, Schematics,          (Gemini Multimodal: OCR,       (Decoupled Hardware Logic,      (State-Space Checks, Edge Cases,
 Waveforms, Tables)          Math Extraction, Pinouts)      Derivations, First Principles)  Simulink/SPICE/Code Prototyping)

```

---

### 1. Ingestion Layer: Multimodal Extraction to Markdown

Slides with sparse text, dense tables, circuit schematics, and simulation plots break typical text parsers. Decouple raw assets from your core markdown repository.

* **Ingestion Rule:** Treat raw lecture PDFs strictly as immutable source blobs. Do not annotate directly inside the PDF viewer.
* **Prompting Gemini for Extraction:** Do not ask for high-level summaries. Require explicit, mechanical extraction:
* *Circuit Schematics:* Convert topology into component nodes, operating regions (e.g., saturation, triode, cutoff), and state variables (inductor currents $i_L$, capacitor voltages $v_C$).
* *Math & State Models:* Render full LaTeX equations with all domain assumptions, boundary conditions, and parameter definitions explicit.
* *Waveforms / Timing Diagrams:* Convert visual plots into state tables (clock edge, switch states, conduction paths, output voltage steps).



---

### 2. Domain Model: Markdown Architecture

Structure each topic as a standalone, modular document. Enforce strict **acyclic dependencies**—if Chapter 4 (e.g., Inverters) relies on Chapter 2 (e.g., MOSFET Switching Dynamics), Chapter 4 must reference the interface contract (input/output boundaries, state constraints), not re-derive switching transients from scratch.

Each topic markdown file follows a standardized schema:

#### Standard Topic Document Schema

1. **State Variables & Physical Quantities:** Explicit definition of every variable, units, and physical manifestation.
2. **Governing Equations & Conservation Laws:** KVL, KCL, Maxwell-Ampère laws, or state-space representations ($\dot{x} = Ax + Bu$). Verbose derivations showing every step rather than collapsed academic jumps.
3. **Mechanical Intuition & Dynamic Trajectory:** Trace the physical chain of causality.
* *Example:* Gate voltage rises $\rightarrow$ channel forms $\rightarrow$ drain current rises $\rightarrow$ parasitic capacitance charges $\rightarrow$ switching losses occur.


4. **Failure Modes & Anti-Patterns (Edge Cases):**
* What saturates the core?
* Where does shoot-through occur?
* What causes pole migration across the imaginary axis?


5. **Interface Constraints:** Voltage limits, maximum slew rate ($dv/dt$), thermal dissipation thresholds, bandwidth/sampling limits.

---

### 3. Mechanical Intuition over Academic Abstraction

Final-year EE units (power electronics, state-space control, embedded systems, high-speed RF) frequently obscure simple physics behind heavy linear algebra or Laplace transforms.

* **Energy and Charge Accounting:** Replace abstract complex-frequency transfer functions with physical state flow:
* Where is the energy stored between switching cycles?
* What happens to inductor energy when the low-side switch opens?
* Why does adding a phase-lead compensator physically advance time response (i.e., anticipating the error slope)?


* **Decouple Math from Mechanism:** Derive the mathematical proof *after* tracing the physical circuit or signal trajectory. If the physical trajectory is not clear, the mathematical proof is just symbol manipulation without diagnostic utility.

---

### 4. Verification Layer: The "Test Harness"

Never rely on passive re-reading to verify comprehension. Treat exam problems and design specifications as automated tests verifying the validity of your mental model.

* **Boundary Value Injection:** Test equations by setting variables to $0$, $\infty$, or steady-state ($t \to \infty, s \to 0$). If a transfer function does not collapse to the DC circuit intuition when $s = 0$, the mathematical model is broken.
* **Executable Prototyping:**
* For control loops or signal processing: Implement the difference equations directly in Python or MATLAB/Simulink scripts using your extracted markdown formulas.
* For hardware/power stages: Run simplified SPICE models to verify current flow paths against your documented state tables.


* **Failure-First Socratic Queries:** Use Gemini as a test harness, not an author. Feed your normalized markdown back into Gemini with prompts such as:
> *"Here is my architectural breakdown of a buck-boost converter in discontinuous conduction mode. Identify any missing transient states, unstated parasitic assumptions, or physical boundary violations in this derivation."*