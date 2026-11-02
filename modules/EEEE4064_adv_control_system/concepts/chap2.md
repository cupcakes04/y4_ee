# Lecture 2: State-Space Representation

**Subject:** EEEE4064 — Advanced Control System Design

**Source:** EEEE4064 - L02 - State Space Representation.pdf

**Date captured:** 2026-09-29

---

## Overview

This chapter establishes the continuous-time state-space representation as an alternative to classical transfer function analysis for modeling linear time-invariant (LTI) systems. It formulates physical differential equations into canonical first-order matrix vector differential equations ($\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}$, $\mathbf{y} = \mathbf{C}\mathbf{x} + \mathbf{D}\mathbf{u}$) to directly accommodate multi-input multi-output (MIMO) systems and internal energy-storing state dynamics. It details the construction of phase-variable companion forms for $n^{\text{th}}$-order systems, providing an algebraic transformation ($\beta$-coefficients) to isolate and eliminate input time derivatives from the state vector derivatives.

---

## Lecture Outline

The lecture covers five main sections:

* **01 | State-Space Equations of LTI Systems**

* **02 | State-Space of a Second-Order System**

* **03 | State-Space of a Third-Order System**

* **04 | State-Space of nth-Order Systems - Case 1**

* **05 | State-Space of nth-Order Systems - Case 2**


---

## State-Space Equations of LTI Systems

### Fundamental Definitions

* **State Variables:** The state variables of a dynamic system are defined as the variables making up the smallest set of variables that determine the state of the dynamic system.


* **State-Space Representation:** A mathematical model of a physical system formulated as a set of input, output, and state variables related by first-order differential equations (continuous-time) or difference equations (discrete-time).


* ⚠️ DEPENDS ON: Ordinary Differential Equations (ODEs) and Matrix Algebra.



### General Multi-Input Multi-Output (MIMO) Model

A general system can possess $m$ inputs, $p$ outputs, and $n$ state variables:

* Inputs: $u_1, u_2, \dots, u_m$

* Outputs: $y_1, y_2, \dots, y_p$

* State variables: $x_1, x_2, \dots, x_n$


> **Diagram Reconstruction: MIMO System Black Box (Slide 3)**
> A central blue rectangle labeled **MIMO** represents the system. On the left side, horizontal incoming arrows denote the inputs vector, labeled from top to bottom as $u_1$, $u_2$, an ellipsis vertical column, and $u_m$, collectively labeled "Inputs". On the bottom edge, vertical upward-pointing arrows enter the block representing the system state variables, labeled from left to right as $x_1$, $x_2$, an ellipsis horizontal row, and $x_n$, collectively labeled "State variables". On the right side, horizontal outgoing arrows emerge from the block representing the outputs, labeled from top to bottom as $y_1$, $y_2$, a vertical ellipsis, and $y_p$, collectively labeled "Outputs".
> 
> 

---

### EXAMPLE 1

Consider a continuous-time linear time-invariant system described by the following second-order differential equation:


$$\ddot{y}(t) + a_1 \dot{y}(t) + a_2 y(t) = u(t)$$


where $a_1$ and $a_2$ are constant system parameters, $u(t)$ is the system input, $y(t)$ is the system output, $\dot{y}(t) = \frac{dy(t)}{dt}$, and $\ddot{y}(t) = \frac{d^2 y(t)}{dt^2}$.

**Step 1: Selection of state variables**

Define the state variables as:


$$x_1(t) = y(t)$$

$$x_2(t) = \dot{y}(t)$$

**Step 2: Time differentiation**

Differentiating $x_1(t)$ and $x_2(t)$ with respect to time $t$:


$$\dot{x}_1(t) = \dot{y}(t) = x_2(t) \quad \text{--- (1)}$$

$$\dot{x}_2(t) = \ddot{y}(t) = -a_2 x_1(t) - a_1 x_2(t) + u(t) \quad \text{--- (2)}$$

**Step 3: Define output equation**

$$y(t) = x_1(t) \quad \text{--- (3)}$$

**Step 4: Algebraic expansion including zero coefficients**

Equations (1)–(3) are rewritten explicitly to display every state variable and input coefficient:


$$\dot{x}_1(t) = 0 \cdot x_1(t) + 1 \cdot x_2(t) + 0 \cdot u(t) \quad \text{--- (4)}$$

$$\dot{x}_2(t) = -a_2 x_1(t) - a_1 x_2(t) + 1 \cdot u(t) \quad \text{--- (5)}$$

$$y(t) = 1 \cdot x_1(t) + 0 \cdot x_2(t) + 0 \cdot u(t) \quad \text{--- (6)}$$

**Step 5: Vector-Matrix Assembly**

Grouping Equations (4) and (5) yields the **State equation** ($\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}$):


$$\begin{bmatrix} \dot{x}_1(t) \\ \dot{x}_2(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ -a_2 & -a_1 \end{bmatrix} \begin{bmatrix} x_1(t) \\ x_2(t) \end{bmatrix} + \begin{bmatrix} 0 \\ 1 \end{bmatrix} u(t)$$

Grouping Equation (6) yields the **Output equation** ($\mathbf{y} = \mathbf{C}\mathbf{x} + \mathbf{D}\mathbf{u}$):


$$y(t) = \begin{bmatrix} 1 & 0 \end{bmatrix} \begin{bmatrix} x_1(t) \\ x_2(t) \end{bmatrix}$$


Here, $\mathbf{D} = [0]$.

* $x_1(t)$ and $x_2(t)$ are the **state variables**.


* $\dot{x}_1(t)$, $\dot{x}_2(t)$, and $y(t)$ are called the **state-space equations**.


* Matrix and vector variables are represented using bold font.



---

### General Matrix Form and Vector Block Diagram

The generalized continuous-time linear state-space representation is defined as:


$$\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}$$

$$\mathbf{y} = \mathbf{C}\mathbf{x} + \mathbf{D}\mathbf{u}$$


where:

* $\mathbf{x}$ = State vector ($n \times 1$)


* $\dot{\mathbf{x}}$ = Derivative of the state vector with respect to time ($n \times 1$)


* $\mathbf{u}$ = Input or control vector ($m \times 1$)


* $\mathbf{y}$ = Output vector ($p \times 1$)


* $\mathbf{A}$ = System matrix ($n \times n$)


* $\mathbf{B}$ = Input matrix ($n \times m$)


* $\mathbf{C}$ = Output matrix ($p \times n$)


* $\mathbf{D}$ = Feedforward (direct transmission) matrix ($p \times m$)



> **Diagram Reconstruction: General State-Space Vector Block Diagram (Slide 6)**
> * Signal flow begins on the left with the vector input $\mathbf{u}(t)$.
> 
> 
> * The signal splits into two paths:
> 1. The lower forward branch passes through block $\mathbf{B}(t)$, producing $\mathbf{B}(t)\mathbf{u}(t)$, which feeds into the positive terminal of a summing junction.
> 
> 
> 2. The upper feedforward branch bypasses the state dynamics entirely, entering block $\mathbf{D}(t)$, yielding $\mathbf{D}(t)\mathbf{u}(t)$, which routes to the top positive input of the output summing junction.
> 
> 
> 
> 
> * The output of the first summing junction produces $\dot{\mathbf{x}}(t)$.
> 
> 
> * $\dot{\mathbf{x}}(t)$ passes through an integrator block labeled $\int dt$, yielding the state vector $\mathbf{x}(t)$.
> 
> 
> * The state vector $\mathbf{x}(t)$ branches into two paths:
> 1. It routes downward through feedback matrix block $\mathbf{A}(t)$, feeding back into the positive terminal of the first summing junction as $\mathbf{A}(t)\mathbf{x}(t)$.
> 
> 
> 2. It proceeds forward through matrix block $\mathbf{C}(t)$, producing $\mathbf{C}(t)\mathbf{x}(t)$, which enters the left positive input of the output summing junction.
> 
> 
> 
> 
> * The output summing junction computes $\mathbf{y}(t) = \mathbf{C}(t)\mathbf{x}(t) + \mathbf{D}(t)\mathbf{u}(t)$, directed outward to the right.
> 
> 
> 
> 

---

## Notes on the State-Space Representation

1. **Physical Observability:** State variables do not need to be physically measurable or observable quantities.


2. **Practical Selection:** Practically, it is convenient to choose easily measurable quantities for state variables if possible, because optimal control laws will require the feedback of all state variables with suitable weighting.


3. **Notation:** For simplicity, it is possible to eliminate the explicit time argument "($t$)" when writing state-space equations since operation within the time domain is assumed.


4. **System Order:** The state equation consists of $n$ first-order differential equations, where $n$ is equal to the order of the system.



---

## State-Space of a Second-Order System

### EXAMPLE 2: Mass-Spring-Damper System

Consider a linear mechanical translational system comprising a mass $m$, a linear spring with stiffness constant $k$, and a viscous damper with damping coefficient $b$.

* **System Input:** External force $u(t)$.


* **System Output:** Displacement $y(t)$ of mass $m$, measured from the equilibrium position in the absence of external force.


* **System Type:** Single-Input Single-Output (SISO) linear system.


* ⚠️ DEPENDS ON: Newton’s Second Law of Motion ($F_{\text{net}} = m\ddot{y}$) and mechanical impedance modeling.



> **Diagram Reconstruction: Mass-Spring-Damper Schematic (Slide 8)**
> A fixed rigid ceiling is shown at the top with hatching lines. Suspended from the ceiling is a helical spring labeled $k$. The lower end of the spring connects to a rigid block of mass labeled $m$. A downward vertical arrow represents external input force $u(t)$ applied directly to mass $m$. From the right side of the mass, a horizontal line terminates in an arrow pointing downward, indicating the output displacement $y(t)$. Attached below the mass is a vertical rod entering a dashpot/damper body labeled $b$. The lower rod of the damper is anchored to a fixed rigid bottom floor with hatching lines.
> 
> 

#### Derivation

1. **Second-Order Differential Equation of Motion:**
Summing forces using Newton's second law:

$$m \ddot{y} + b \dot{y} + k y = u$$



2. **Formulate First-Order State Equations:**
Choose physical state variables (position and velocity):

$$x_1 = y$$



$$x_2 = \dot{y}$$



Differentiating both states:

$$\dot{x}_1 = x_2$$



$$\dot{x}_2 = \ddot{y} = \frac{1}{m}(-k y - b \dot{y}) + \frac{1}{m}u$$



Substituting $x_1$ and $x_2$:

$$\dot{x}_2 = -\frac{k}{m} x_1 - \frac{b}{m} x_2 + \frac{1}{m} u$$



$$y = x_1$$



3. **Matrix Form:**
$$\begin{bmatrix} \dot{x}_1 \\ \dot{x}_2 \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ -\frac{k}{m} & -\frac{b}{m} \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} + \begin{bmatrix} 0 \\ \frac{1}{m} \end{bmatrix} u$$



$$y = \begin{bmatrix} 1 & 0 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$$



$$\mathbf{A} = \begin{bmatrix} 0 & 1 \\ -\frac{k}{m} & -\frac{b}{m} \end{bmatrix}, \quad \mathbf{B} = \begin{bmatrix} 0 \\ \frac{1}{m} \end{bmatrix}, \quad \mathbf{C} = \begin{bmatrix} 1 & 0 \end{bmatrix}, \quad D = 0$$




> **Diagram Reconstruction: Scalar Simulation Diagram for Mass-Spring-Damper (Slide 9)**
> * Signal flow starts on the left with input $u$, passing through scaling block $\frac{1}{m}$.
> 
> 
> * It enters a summing junction with a positive sign.
> 
> 
> * The output of the summing junction is acceleration $\dot{x}_2$.
> 
> 
> * $\dot{x}_2$ enters an integrator block labeled $\int$, producing velocity $x_2$.
> 
> 
> * $x_2$ branches: one path continues rightward to a second integrator block $\int$, while the other feedback path loops downward through gain block $\frac{b}{m}$.
> 
> 
> * The output of the second integrator is displacement $x_1 = y$, which continues rightward as the final system output.
> 
> 
> * The line for $x_1$ loops down and leftward through gain block $\frac{k}{m}$.
> 
> 
> * The outputs of gain blocks $\frac{b}{m}$ and $\frac{k}{m}$ enter an intermediate summer with positive signs, whose combined feedback signal enters the negative terminal of the main summing junction.
> 
> 
> 
> 

---

## State-Space of a Third-Order System

### EXAMPLE 3

Given the continuous-time third-order differential equation:


$$\dddot{y}(t) + 6\ddot{y}(t) + 11\dot{y}(t) + 6y(t) = 6u(t)$$

**Step 1: Rearrange for the highest-order derivative**

$$\dddot{y} = -6\ddot{y} - 11\dot{y} - 6y + 6u$$

**Step 2: Assign state variables**

*(Note: As defined in slide 10, states are ordered starting from the highest derivative down to the zeroth derivative)*:


$$x_1 = \ddot{y}$$

$$x_2 = \dot{y}$$

$$x_3 = y$$

**Step 3: Differentiate state variables**

$$\dot{x}_1 = \dddot{y} = -6x_1 - 11x_2 - 6x_3 + 6u$$

$$\dot{x}_2 = \ddot{y} = x_1$$

$$\dot{x}_3 = \dot{y} = x_2$$

$$y = x_3$$

**Step 4: Formulate State and Output Equations**

$$\begin{bmatrix} \dot{x}_1 \\ \dot{x}_2 \\ \dot{x}_3 \end{bmatrix} = \begin{bmatrix} -6 & -11 & -6 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} + \begin{bmatrix} 6 \\ 0 \\ 0 \end{bmatrix} u$$

$$y = \begin{bmatrix} 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}$$


Here, $\mathbf{A} = \begin{bmatrix} -6 & -11 & -6 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}$, $\mathbf{B} = \begin{bmatrix} 6 \\ 0 \\ 0 \end{bmatrix}$, $\mathbf{C} = \begin{bmatrix} 0 & 0 & 1 \end{bmatrix}$, and $D = 0$.

> **Diagram Reconstruction: Third-Order Companion Form Block Diagram (Slide 11)**
> * Signal flow begins at input node $u$, passing through gain block $6$ into a summing junction labeled $\Sigma$.
> 
> 
> * The output of $\Sigma$ is $\dddot{y}$.
> 
> 
> * $\dddot{y}$ enters the first integrator block labeled $\frac{1}{s}$, producing node $\ddot{y}$ ($= x_1$).
> 
> 
> * A feedback branch from $\ddot{y}$ passes down through gain block $-6$ and enters a positive terminal on $\Sigma$.
> 
> 
> * The main path enters the second integrator block labeled $\frac{1}{s}$, producing node $\dot{y}$ ($= x_2$).
> 
> 
> * A feedback branch from $\dot{y}$ passes down through gain block $-11$ and enters a positive terminal on $\Sigma$.
> 
> 
> * The main path enters the third integrator block labeled $\frac{1}{s}$, producing node $y$ ($= x_3$), which feeds to output terminal $y$.
> 
> 
> * A feedback branch from $y$ passes down through gain block $-6$ and enters a positive terminal on $\Sigma$.
> 
> 
> * ⚠️ DEPENDS ON: Laplace transform notation where integration in the time domain is denoted by the transfer operator $\frac{1}{s}$.
> 
> 
> 
> 

---

### EXERCISE 1

Consider a system with the following differential equation:


$$\dddot{c} + 9\ddot{c} + 26\dot{c} + 24c = 24r$$


Find the state-space representation for the system then draw its block diagram.
*(Refer to Open / Unresolved section)*.

---

## State-Space of nth-Order Systems - Case 1

### Overview and Assumptions

* **Condition:** The forcing function on the right-hand side contains no derivative terms of the input $u$:



$$y^{(n)} + a_1 y^{(n-1)} + \dots + a_{n-1}\dot{y} + a_n y = u$$


* **Selection of State Variables:** Defined using phase variables (the output and its successive $n-1$ derivatives):



$$x_1 = y$$


$$x_2 = \dot{y}$$


$$\vdots$$


$$x_n = y^{(n-1)}$$


* **Practical Limitation / Engineering Failure Mode:** While mathematically convenient, higher-order numerical or analog time derivatives amplify high-frequency measurement noise inherent in real-world systems, making direct differentiation of physical outputs undesirable for physical states.



### Mathematical Formulation

Differentiating the chosen state variables:


$$\dot{x}_1 = x_2$$

$$\dot{x}_2 = x_3$$

$$\vdots$$

$$\dot{x}_{n-1} = x_n$$

$$\dot{x}_n = -a_n x_1 - a_{n-1} x_2 - \dots - a_1 x_n + u$$

Output equation:


$$y = x_1$$

### Matrix Form (Phase-Variable Canonical Form / Companion Form)

$$\begin{bmatrix} \dot{x}_1 \\ \dot{x}_2 \\ \vdots \\ \dot{x}_{n-1} \\ \dot{x}_n \end{bmatrix} = \begin{bmatrix}  0 & 1 & 0 & \dots & 0 \\  0 & 0 & 1 & \dots & 0 \\  \vdots & \vdots & \vdots & \ddots & \vdots \\  0 & 0 & 0 & \dots & 1 \\  -a_n & -a_{n-1} & -a_{n-2} & \dots & -a_1  \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_{n-1} \\ x_n \end{bmatrix} + \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 0 \\ 1 \end{bmatrix} u$$

$$\mathbf{y} = \begin{bmatrix} 1 & 0 & \dots & 0 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix}$$

The corresponding SISO Transfer Function is:


$$\frac{Y(s)}{U(s)} = \frac{1}{s^n + a_1 s^{n-1} + \dots + a_{n-1} s + a_n}$$

---

## State-Space of nth-Order Systems - Case 2

### Overview and Problem Statement

* **Condition:** The forcing function involves derivatives of the input signal $u(t)$:



$$y^{(n)} + a_1 y^{(n-1)} + \dots + a_{n-1}\dot{y} + a_n y = b_0 u^{(n)} + b_1 u^{(n-1)} + \dots + b_{n-1}\dot{u} + b_n u$$


* **Fundamental Challenge:** State-space standard formulation requires first-order derivative equations of the form $\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}$, which explicitly **forbids** derivative terms of the input ($\dot{u}, \ddot{u}, \dots$) from appearing in the state derivative equations.


* **Solution Strategy:** Define composite state variables by subtracting linear combinations of $u(t)$ and its derivatives scaled by recurrence constants $\beta_k$.



### State Variable Definitions and Beta ($\beta$) Coefficients

To eliminate input derivatives, define the states as:


$$x_1 = y - \beta_0 u$$

$$x_2 = \dot{y} - \beta_0 \dot{u} - \beta_1 u = \dot{x}_1 - \beta_1 u$$

$$x_3 = \ddot{y} - \beta_0 \ddot{u} - \beta_1 \dot{u} - \beta_2 u = \dot{x}_2 - \beta_2 u$$

$$\vdots$$

$$x_n = y^{(n-1)} - \beta_0 u^{(n-1)} - \beta_1 u^{(n-2)} - \dots - \beta_{n-2}\dot{u} - \beta_{n-1}u = \dot{x}_{n-1} - \beta_{n-1} u$$

Where the intermediate $\beta$-coefficients are defined recursively by matching algebraic terms:


$$\beta_0 = b_0$$

$$\beta_1 = b_1 - a_1 \beta_0$$

$$\beta_2 = b_2 - a_1 \beta_1 - a_2 \beta_0$$

$$\beta_3 = b_3 - a_1 \beta_2 - a_2 \beta_1 - a_3 \beta_0$$

$$\vdots$$

$$\beta_n = b_n - a_1 \beta_{n-1} - \dots - a_{n-1} \beta_1 - a_n \beta_0$$

### Resulting First-Order State Equations

Rearranging each derivative definition:


$$\dot{x}_1 = x_2 + \beta_1 u$$

$$\dot{x}_2 = x_3 + \beta_2 u$$

$$\vdots$$

$$\dot{x}_{n-1} = x_n + \beta_{n-1} u$$

$$\dot{x}_n = -a_n x_1 - a_{n-1} x_2 - \dots - a_1 x_n + \beta_n u$$

From the definition of $x_1$, the output equation is:


$$y = x_1 + \beta_0 u$$

* Note: While this choice provides uniqueness of the solution to the state equation, it is not the only valid choice of state variables.



### Matrix Form (Controller / Phase Canonical Form with Numerator Dynamics)

$$\begin{bmatrix} \dot{x}_1 \\ \dot{x}_2 \\ \vdots \\ \dot{x}_{n-1} \\ \dot{x}_n \end{bmatrix} = \begin{bmatrix}  0 & 1 & 0 & \dots & 0 \\  0 & 0 & 1 & \dots & 0 \\  \vdots & \vdots & \vdots & \ddots & \vdots \\  0 & 0 & 0 & \dots & 1 \\  -a_n & -a_{n-1} & -a_{n-2} & \dots & -a_1  \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_{n-1} \\ x_n \end{bmatrix} + \begin{bmatrix} \beta_1 \\ \beta_2 \\ \vdots \\ \beta_{n-1} \\ \beta_n \end{bmatrix} u$$

$$y = \begin{bmatrix} 1 & 0 & \dots & 0 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix} + \beta_0 u$$

The corresponding transfer function is:


$$\frac{Y(s)}{U(s)} = \frac{b_0 s^n + b_1 s^{n-1} + \dots + b_{n-1} s + b_n}{s^n + a_1 s^{n-1} + \dots + a_{n-1} s + a_n}$$

---

### EXAMPLE 4

Find the state-space representation of the system defined by:


$$\dddot{y} + 2\ddot{y} + 3\dot{y} + 4y = 5\dddot{u} + 6\ddot{u} + 7\dot{u} + 8u$$

**Step 1: Map system parameters to general polynomial coefficients**

Here $n = 3$:

* Denominator: $a_1 = 2, \quad a_2 = 3, \quad a_3 = 4$

* Numerator: $b_0 = 5, \quad b_1 = 6, \quad b_2 = 7, \quad b_3 = 8$


**Step 2: Calculate $\beta$ coefficients**

* $\beta_0 = b_0 = 5$
* $\beta_1 = b_1 - a_1 \beta_0 = 6 - (2 \times 5) = 6 - 10 = -4$
* $\beta_2 = b_2 - a_1 \beta_1 - a_2 \beta_0 = 7 - 2(-4) - (3 \times 5) = 7 + 8 - 15 = 0$
* $\beta_3 = b_3 - a_1 \beta_2 - a_2 \beta_1 - a_3 \beta_0 = 8 - (2 \times 0) - 3(-4) - (4 \times 5) = 8 - 0 + 12 - 20 = 0$

**Step 3: Define state equations**

$$x_1 = y - \beta_0 u = y - 5u$$

$$x_2 = \dot{x}_1 - \beta_1 u = \dot{x}_1 + 4u$$

$$x_3 = \dot{x}_2 - \beta_2 u = \dot{x}_2$$

State derivative equations:


$$\dot{x}_1 = x_2 + \beta_1 u = x_2 - 4u$$

$$\dot{x}_2 = x_3 + \beta_2 u = x_3$$

$$\dot{x}_3 = -a_3 x_1 - a_2 x_2 - a_1 x_3 + \beta_3 u = -4x_1 - 3x_2 - 2x_3 + (0)u$$

Output equation:


$$y = x_1 + \beta_0 u = x_1 + 5u$$

**Step 4: Vector-matrix assembly**

$$\begin{bmatrix} \dot{x}_1 \\ \dot{x}_2 \\ \dot{x}_3 \end{bmatrix} = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -4 & -3 & -2 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} + \begin{bmatrix} -4 \\ 0 \\ 0 \end{bmatrix} u$$

$$y = \begin{bmatrix} 1 & 0 & 0 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} + 5u$$

---

### EXERCISE 2

Find the state-space equation and output equation for the system defined by:


$$\frac{Y(s)}{U(s)} = \frac{2s^3 + s^2 + s + 2}{s^3 + 4s^2 + 5s + 2}$$


*(Refer to Open / Unresolved section)*.

---

## Notes on the State-Space of nth-Order Systems

1. **Invariance of $\mathbf{A}$ and $\mathbf{C}$ Matrices:** When comparing the state-space representations of Case 1 (no input derivatives) and Case 2 (with input derivatives), the state matrix $\mathbf{A}$ and the output matrix $\mathbf{C}$ remain identical.


2. **Impact of Input Derivatives:** The derivatives of the input signal in Case 2 affect only the elements of the $\mathbf{B}$ matrix (via the $\beta_1, \dots, \beta_n$ components).


3. **Feedforward Matrix Origin:** The gain of the highest-order derivative of the input ($b_0$) directly dictates the direct transmission scalar/matrix $\mathbf{D} = [b_0] = [\beta_0]$.



---

## Key Equations

**General Continuous-Time State-Space Representation**

$$\dot{\mathbf{x}}(t) = \mathbf{A}(t)\mathbf{x}(t) + \mathbf{B}(t)\mathbf{u}(t)$$

$$\mathbf{y}(t) = \mathbf{C}(t)\mathbf{x}(t) + \mathbf{D}(t)\mathbf{u}(t)$$

* **Variables:**
* $\mathbf{x}(t) \in \mathbb{R}^{n \times 1}$: State vector representing dynamic memory/energy storage states of the system [dimensionless or mixed physical units, e.g., $\text{m}$, $\text{m/s}$].


* $\dot{\mathbf{x}}(t) \in \mathbb{R}^{n \times 1}$: First time derivative of state vector [$\text{units of } \mathbf{x} \cdot \text{s}^{-1}$].


* $\mathbf{u}(t) \in \mathbb{R}^{m \times 1}$: System control/input vector [e.g., $\text{V}$, $\text{N}$].


* $\mathbf{y}(t) \in \mathbb{R}^{p \times 1}$: Measured system output vector [e.g., $\text{m}$, $\text{rad}$].


* $\mathbf{A}(t) \in \mathbb{R}^{n \times n}$: System dynamics matrix [$\text{s}^{-1}$].


* $\mathbf{B}(t) \in \mathbb{R}^{n \times m}$: Input distribution matrix [$\text{units of } \mathbf{x} \cdot (\text{units of } \mathbf{u})^{-1} \cdot \text{s}^{-1}$].


* $\mathbf{C}(t) \in \mathbb{R}^{p \times n}$: Output measurement matrix [$\text{units of } \mathbf{y} \cdot (\text{units of } \mathbf{x})^{-1}$].


* $\mathbf{D}(t) \in \mathbb{R}^{p \times m}$: Direct transmission/feedforward matrix [$\text{units of } \mathbf{y} \cdot (\text{units of } \mathbf{u})^{-1}$].




* **Assumes:** System linearity; continuous differentiability over time domain $t$.


* **Breaks when:** The system operates nonlinearly (saturation, dead zones, friction), experiences discrete event jumps, or contains distributed parameters (infinite-dimensional partial differential equations).

---

**Translational Mechanical System Dynamic Equation**

$$m\ddot{y}(t) + b\dot{y}(t) + ky(t) = u(t)$$

* **Variables:**
* $m$: Mass of the body [$\text{kg}$].


* $b$: Viscous friction / damping coefficient [$\text{N}\cdot\text{s/m}$ or $\text{kg/s}$].


* $k$: Linear spring stiffness coefficient [$\text{N/m}$ or $\text{kg/s}^2$].


* $y(t)$: Mass translational displacement from equilibrium [$\text{m}$].


* $\dot{y}(t)$: Mass translational velocity [$\text{m/s}$].


* $\ddot{y}(t)$: Mass translational acceleration [$\text{m/s}^2$].


* $u(t)$: Applied external control force [$\text{N}$].




* **Assumes:** Constant lumped parameters; ideal linear Hookean elasticity; ideal viscous damping; 1D rectilinear motion with negligible friction other than the dashpot.


* **Breaks when:** Spring yield displacement is exceeded (plastic deformation); damper undergoes turbulent/non-viscous fluid flow (quadratic air drag); mass varies over time.

---

**Phase-Variable Companion Form (Case 1: No Input Derivatives)**

$$\begin{bmatrix} \dot{x}_1 \\ \dot{x}_2 \\ \vdots \\ \dot{x}_{n-1} \\ \dot{x}_n \end{bmatrix} = \begin{bmatrix} 0 & 1 & 0 & \dots & 0 \\ 0 & 0 & 1 & \dots & 0 \\ \vdots & \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & 0 & \dots & 1 \\ -a_n & -a_{n-1} & -a_{n-2} & \dots & -a_1 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_{n-1} \\ x_n \end{bmatrix} + \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 0 \\ 1 \end{bmatrix} u$$

$$y = \begin{bmatrix} 1 & 0 & \dots & 0 \end{bmatrix} \mathbf{x}$$

* **Variables:**
* $x_1, \dots, x_n$: Phase variables representing the output $y$ and its sequential time derivatives up to order $n-1$ [$\text{units of } y \cdot \text{s}^{-(k-1)}$].


* $a_1, \dots, a_n$: Constant scalar coefficients of the monic characteristic differential equation [$\text{s}^{-(n-k)}$].


* $u$: Scalar input [$\text{units of } u$].


* $y$: Scalar output [$\text{units of } y$].




* **Assumes:** Strictly proper transfer function (degree of numerator is zero, $m = 0 < n$); constant coefficients (time-invariant); input contains no derivative components.


* **Breaks when:** Forcing function features input rate-of-change ($\dot{u} \neq 0$); parameters drift with time ($a_i = a_i(t)$).

---

**Recursive Beta ($\beta$) Coefficients for Input Derivative Elimination (Case 2)**

$$\beta_0 = b_0$$

$$\beta_k = b_k - \sum_{j=1}^{k} a_j \beta_{k-j} \quad \text{for } k = 1, 2, \dots, n$$

* **Variables:**
* $\beta_0$: Direct feedforward transmission scalar [$\text{units of } y \cdot (\text{units of } u)^{-1}$].


* $\beta_k$: Input coupling state weighting factor for $k^{\text{th}}$ state derivative [$\text{units of } x_k \cdot (\text{units of } u)^{-1} \cdot \text{s}^{-1}$].


* $b_0, \dots, b_n$: Numerator polynomial coefficients of differential operator [$\text{s}^{k-n}$].


* $a_1, \dots, a_n$: Denominator polynomial coefficients of differential operator [$\text{s}^{-k}$].




* **Assumes:** System is proper (order of input derivatives $m \le n$, where $n$ is system differential order).


* **Breaks when:** System is strictly improper ($m > n$, requiring non-causal differentiating elements).

---

## Concept Index

* State variables


* State-space representation


* Dynamic system


* First-order differential equations


* Difference equations


* Linear Time-Invariant (LTI) systems


* Multi-Input Multi-Output (MIMO)


* Single-Input Single-Output (SISO)


* State vector ($\mathbf{x}$)


* State derivative vector ($\dot{\mathbf{x}}$)


* System matrix ($\mathbf{A}$)


* Input matrix ($\mathbf{B}$)


* Output matrix ($\mathbf{C}$)


* Feedforward / Direct transmission matrix ($\mathbf{D}$)


* Output vector ($\mathbf{y}$)


* Input / Control vector ($\mathbf{u}$)


* Mass-spring-damper system


* Equilibrium position


* Vector block diagram


* Phase variables


* Companion form / Canonical state representation


* Forcing function


* Input derivatives


* $\beta$-coefficients (Beta formulation)


* Proper transfer functions



---

## Open / Unresolved

* ❓ **EXERCISE 1 (Slide 12):**
The slide presents an unsolved student exercise:


$$\dddot{c} + 9\ddot{c} + 26\dot{c} + 24c = 24r$$


*Unresolved requirements from slide:* Derive the system's state-space representation and construct its block diagram. *(Note: Requires identifying whether to use standard ascending phase variables $x_1=c, x_2=\dot{c}, x_3=\ddot{c}$ as in Case 1, or the descending state assignments used in Example 3: $x_1=\ddot{c}, x_2=\dot{c}, x_3=c$)*.


* ❓ **EXERCISE 2 (Slide 20):**
The slide poses an unsolved student exercise:


$$\frac{Y(s)}{U(s)} = \frac{2s^3 + s^2 + s + 2}{s^3 + 4s^2 + 5s + 2}$$


*Unresolved requirements from slide:* Compute the $\beta_0, \beta_1, \beta_2, \beta_3$ parameters and write out the numerical $\mathbf{A}, \mathbf{B}, \mathbf{C}, \mathbf{D}$ matrices.


* ❓ **Preview Topic (Slide 22):**
"Transformation of State-Space" is flagged as the topic for "Next Week" without definitions, transformation matrices ($\mathbf{P}$ or $\mathbf{T}$ similarity transformations), or invariant characteristics provided in this deck.