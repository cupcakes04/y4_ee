To invert a $3 \times 3$ matrix $A$, the standard algebraic method uses the formula:

$$A^{-1} = \frac{1}{\det(A)} \operatorname{adj}(A)$$

where $\det(A)$ is the determinant of $A$, and $\operatorname{adj}(A)$ is the adjugate (the transpose of the cofactor matrix). A matrix is invertible if and only if $\det(A) \neq 0$.

Let the matrix be:

$$A = \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}$$

---

### Step 1: Calculate the Determinant $\det(A)$

Expand along the first row:

$$\det(A) = a(ei - fh) - b(di - fg) + c(dh - eg)$$

* If $\det(A) = 0$, the matrix is singular and has no inverse.
* If $\det(A) \neq 0$, proceed to Step 2.

---

### Step 2: Form the Matrix of Minors

For every entry in the $3 \times 3$ matrix, cross out its row and column, then compute the determinant of the remaining $2 \times 2$ submatrix:

$$M = \begin{bmatrix} \det\begin{bmatrix} e & f \\ h & i \end{bmatrix} & \det\begin{bmatrix} d & f \\ g & i \end{bmatrix} & \det\begin{bmatrix} d & e \\ g & h \end{bmatrix} \\ \det\begin{bmatrix} b & c \\ h & i \end{bmatrix} & \det\begin{bmatrix} a & c \\ g & i \end{bmatrix} & \det\begin{bmatrix} a & b \\ g & h \end{bmatrix} \\ \det\begin{bmatrix} b & c \\ e & f \end{bmatrix} & \det\begin{bmatrix} a & c \\ d & f \end{bmatrix} & \det\begin{bmatrix} a & b \\ d & e \end{bmatrix} \end{bmatrix}$$

Each $2 \times 2$ determinant is calculated as $\det\begin{bmatrix} p & q \\ r & s \end{bmatrix} = ps - qr$.

---

### Step 3: Apply Alternating Signs (Cofactor Matrix)

Apply a checkerboard pattern of signs ($+$ and $-$) according to $(-1)^{i+j}$:

$$\begin{bmatrix} + & - & + \\ - & + & - \\ + & - & + \end{bmatrix}$$

The cofactor matrix $C$ becomes:

$$C = \begin{bmatrix} +(ei - fh) & -(di - fg) & +(dh - eg) \\ -(bi - ch) & +(ai - cg) & -(ah - bg) \\ +(bf - ce) & -(af - cd) & +(ae - bd) \end{bmatrix}$$

---

### Step 4: Transpose the Cofactor Matrix (Adjugate)

Swap the rows and columns of $C$ to obtain $\operatorname{adj}(A) = C^T$:

$$\operatorname{adj}(A) = \begin{bmatrix} C_{11} & C_{21} & C_{31} \\ C_{12} & C_{22} & C_{32} \\ C_{13} & C_{23} & C_{33} \end{bmatrix}$$

---

### Step 5: Scale by $\frac{1}{\det(A)}$

Multiply every element of $\operatorname{adj}(A)$ by $\frac{1}{\det(A)}$:

$$A^{-1} = \frac{1}{\det(A)} \operatorname{adj}(A)$$

---

### Worked Example

Find the inverse of:

$$A = \begin{bmatrix} 1 & 2 & 3 \\ 0 & 1 & 4 \\ 5 & 6 & 0 \end{bmatrix}$$

**1. Determinant:**


$$\det(A) = 1(1 \cdot 0 - 4 \cdot 6) - 2(0 \cdot 0 - 4 \cdot 5) + 3(0 \cdot 6 - 1 \cdot 5)$$

$$\det(A) = 1(-24) - 2(-20) + 3(-5) = -24 + 40 - 15 = 1$$

Since $\det(A) = 1 \neq 0$, the inverse exists.

**2. Matrix of Minors:**

* $M_{11} = 1(0) - 4(6) = -24$
* $M_{12} = 0(0) - 4(5) = -20$
* $M_{13} = 0(6) - 1(5) = -5$
* $M_{21} = 2(0) - 3(6) = -18$
* $M_{22} = 1(0) - 3(5) = -15$
* $M_{23} = 1(6) - 2(5) = -4$
* $M_{31} = 2(4) - 3(1) = 5$
* $M_{32} = 1(4) - 3(0) = 4$
* $M_{33} = 1(1) - 2(0) = 1$

**3. Cofactor Matrix ($C$):**
Apply the alternating signs $\begin{bmatrix} + & - & + \\ - & + & - \\ + & - & + \end{bmatrix}$:

$$C = \begin{bmatrix} -24 & 20 & -5 \\ 18 & -15 & 4 \\ 5 & -4 & 1 \end{bmatrix}$$

**4. Adjugate ($\operatorname{adj}(A) = C^T$):**
Transpose $C$:

$$\operatorname{adj}(A) = \begin{bmatrix} -24 & 18 & 5 \\ 20 & -15 & -4 \\ -5 & 4 & 1 \end{bmatrix}$$

**5. Compute $A^{-1}$:**
Since $\det(A) = 1$:

$$A^{-1} = \frac{1}{1} \begin{bmatrix} -24 & 18 & 5 \\ 20 & -15 & -4 \\ -5 & 4 & 1 \end{bmatrix} = \begin{bmatrix} -24 & 18 & 5 \\ 20 & -15 & -4 \\ -5 & 4 & 1 \end{bmatrix}$$
