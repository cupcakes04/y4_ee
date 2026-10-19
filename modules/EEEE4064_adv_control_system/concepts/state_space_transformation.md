# State-Space Canonical Forms: Structural Comparison & Notes

---

## 1. Dual Pair: Controllable Canonical Form (CCF) vs. Observable Canonical Form (OCF)

CCF and OCF represent the exact same transfer function $G(s) = \frac{Y(s)}{U(s)}$ and share an exact **matrix transpose (duality)** relationship.

### Mathematical Realization

Given the transfer function:


$$\frac{Y(s)}{U(s)} = \frac{b_0 s^n + b_1 s^{n-1} + \dots + b_{n-1} s + b_n}{s^n + a_1 s^{n-1} + \dots + a_{n-1} s + a_n} = b_0 + \frac{(b_1 - a_1 b_0) s^{n-1} + \dots + (b_n - a_n b_0)}{s^n + a_1 s^{n-1} + \dots + a_n}$$

* Controllable Canonical Form (CCF):



$$\dot{x} = \begin{bmatrix} 0 & 1 & 0 & \cdots & 0 \\  0 & 0 & 1 & \cdots & 0 \\  \vdots & \vdots & \vdots & \ddots & \vdots \\  0 & 0 & 0 & \cdots & 1 \\  -a_n & -a_{n-1} & -a_{n-2} & \cdots & -a_1 \end{bmatrix} x + \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 0 \\ 1 \end{bmatrix} u$$



$$y = \begin{bmatrix} b_n - a_n b_0 & b_{n-1} - a_{n-1} b_0 & \cdots & b_1 - a_1 b_0 \end{bmatrix} x + b_0 u$$



* Observable Canonical Form (OCF):



$$\dot{x} = \begin{bmatrix} 0 & 0 & \cdots & 0 & -a_n \\  1 & 0 & \cdots & 0 & -a_{n-1} \\  \vdots & \vdots & \ddots & \vdots & \vdots \\  0 & 0 & \cdots & 1 & -a_1 \end{bmatrix} x + \begin{bmatrix} b_n - a_n b_0 \\ b_{n-1} - a_{n-1} b_0 \\ \vdots \\ b_1 - a_1 b_0 \end{bmatrix} u$$



$$y = \begin{bmatrix} 0 & 0 & \cdots & 0 & 1 \end{bmatrix} x + b_0 u$$




### Transpose / Duality Mapping

$$\mathbf{A_o = A_c^T}, \quad \mathbf{B_o = C_c^T}, \quad \mathbf{C_o = B_c^T}, \quad \mathbf{D_o = D_c = b_0}$$

* **$A$ Matrix:** The bottom row containing polynomial coefficients $\begin{bmatrix} -a_n & \cdots & -a_1 \end{bmatrix}$ in CCF becomes the **final column** in OCF. The superdiagonal of $1$s transposes into a subdiagonal of $1$s.


* **$B$ and $C$ Matrices:** The trivial vector $\begin{bmatrix} 0 & \cdots & 1 \end{bmatrix}^T$ swaps roles from input distribution ($B_c$) to state extraction ($C_o$). The numerator dynamics vector moves from output weighting ($C_c$) directly into input distribution ($B_o$).



### Core Philosophy & Intuitive Usage

* **CCF (Actuation-First / Phase-Variable):**
* **Philosophy:** Constructs a downstream integration chain driven from the top ($x_n$) by control input $u$. The states represent pure derivatives/integrals, while output $y$ is simply a weighted combination read out from this chain.


* **Core Usage:** **State-Feedback Controller Synthesis ($u = -Kx$)**. Because feedback changes only the bottom row of $A_c$ ($A_c - B_c K$), pole placement gains map directly to desired characteristic polynomial coefficients without requiring matrix inversion.


* **OCF (Measurement-First / Observer Form):**
* **Philosophy:** Constructs an upstream accumulation pipeline terminating at the single measured output $y \approx x_n$. The internal states are structured so that observing the single output backward reveals the full internal state vector.


* **Core Usage:** **State Estimator / Luenberger Observer Design**. The observer gain vector $L$ in $(A_o - L C_o)$ directly alters the last column of $A_o$, making observer pole placement structurally identical to controller synthesis in CCF.



---

## 2. Modal Pair: Diagonal Canonical Form (DCF) vs. Jordan Canonical Form (JCF)

DCF and JCF represent **modal state decompositions** derived directly from the **partial fraction expansion (PFE)** of the transfer function.

### Mathematical Realization

Given the factored denominator:


$$\frac{Y(s)}{U(s)} = b_0 + \sum \text{PFE terms}$$

* Diagonal Canonical Form (DCF — Distinct Roots $-p_1, \dots, -p_n$):



$$\frac{Y(s)}{U(s)} = b_0 + \frac{c_1}{s + p_1} + \frac{c_2}{s + p_2} + \dots + \frac{c_n}{s + p_n}$$



$$\dot{x} = \begin{bmatrix} -p_1 & 0 & \cdots & 0 \\  0 & -p_2 & \cdots & 0 \\  \vdots & \vdots & \ddots & \vdots \\  0 & 0 & \cdots & -p_n \end{bmatrix} x + \begin{bmatrix} 1 \\ 1 \\ \vdots \\ 1 \end{bmatrix} u, \quad y = \begin{bmatrix} c_1 & c_2 & \cdots & c_n \end{bmatrix} x + b_0 u$$



* Jordan Canonical Form (JCF — Repeated Root $-p_1$ with multiplicity 3, plus distinct roots):



$$\frac{Y(s)}{U(s)} = b_0 + \frac{c_1}{(s + p_1)^3} + \frac{c_2}{(s + p_1)^2} + \frac{c_3}{s + p_1} + \frac{c_4}{s + p_4} + \dots + \frac{c_n}{s + p_n}$$



$$\dot{x} = \left[ \begin{array}{ccc|ccc} -p_1 & 1 & 0 & 0 & \cdots & 0 \\ 0 & -p_1 & 1 & \vdots & & \vdots \\ 0 & 0 & -p_1 & 0 & \cdots & 0 \\ \hline 0 & \cdots & 0 & -p_4 & & 0 \\ \vdots & & \vdots & & \ddots & \vdots \\ 0 & \cdots & 0 & 0 & \cdots & -p_n \end{array} \right] x + \left[ \begin{array}{c} 0 \\ 0 \\ 1 \\ \hline 1 \\ \vdots \\ 1 \end{array} \right] u, \quad y = \begin{bmatrix} c_1 & c_2 & c_3 & c_4 & \cdots & c_n \end{bmatrix} x + b_0 u$$




### Structural Partition Relationship

JCF directly embeds DCF as a submatrix alongside partitioned blocks:

```
                     Repeated Roots Block              Distinct Roots Block
                 ┌───────────────────────────┬──────────────────────────────────────┐
                 │  -p₁    1     0           │   0        0       ..        0       │  ◄── Off-Diagonal: ZERO Coupling
                 │    0  -p₁     1           │   :        :                 :       │
State Matrix A:  │    0    0   -p₁           │   0        0       ..        0       │
                 ├───────────────────────────┼──────────────────────────────────────┤
                 │    0   ..     0           │ -p₄        0       ..        0       │
                 │    :          :           │   0      -p₅       ..        0       │  ◄── Subsystem: Pure DCF
                 │    0   ..     0           │   0        0       ..      -pₙ       │
                 └───────────────────────────┴──────────────────────────────────────┘
                  ▲                           ▲
                  Jordan Block (Chained)      Off-Diagonal: ZERO Coupling

```

* **Bottom-Right Subsystem (Pure DCF):** The distinct roots maintain completely decoupled scalar modes ($\dot{x}_k = -p_k x_k + u$).


* **Top-Left Subsystem (Jordan Block):** Accommodates the cascading powers $\frac{1}{(s+p_1)^k}$. The superdiagonal $1$s provide the necessary feedforward links between repeated states.


* **Off-Diagonal Blocks ($\mathbf{0}$):** Strictly zero. Independent modal frequencies never interact or cross-bleed.


* **Input Vector ($B$) Partition:** In the distinct partition, every state receives $u$ directly ($1$s). In the Jordan partition, $u$ is injected **only into the base state** ($x_3$). The signal then ripples upward into $x_2$ and $x_1$ via the superdiagonal $1$s.



### Core Philosophy & Intuitive Usage

* **DCF (Decoupled Parallel Modes):**
    * **Philosophy:** Complete dynamic decoupling. Converts high-order systems into independent scalar 1D problems operating in parallel.


    * **Core Usage:** **Modal Analysis & Analytical Solutions**. The matrix exponential is diagonal ($e^{At} = \text{diag}(e^{-p_i t})$), and controllability/observability can be inspected directly without computing rank criteria: a zero in $B$ indicates an uncontrollable mode, while a zero in $C$ ($c_i = 0$) indicates an unobservable mode.




* **JCF (Generalized Modal Form for Defective Systems):**
    * **Philosophy:** Handles repeated eigenvalues where full diagonal decoupling is mathematically impossible. Represents the nearest achievable approximation to a diagonal form using chained leaky integrators.


    * **Core Usage:** **Secular Response Analysis & Structural Degeneracy**. Illustrates how repeated poles generate polynomial-exponential time responses ($t^k e^{-p t}$) via state chaining, while isolating the exact minimum path required to control the repeated subsystem.