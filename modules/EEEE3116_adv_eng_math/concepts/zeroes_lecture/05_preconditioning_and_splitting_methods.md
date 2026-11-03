# Chapter 05: Preconditioning & Matrix Splitting Methods

**Subject:** Spectral Clustering, Preconditioned Conjugate Gradients (PCG), Jacobi & Gauss-Seidel Relaxations  
**Depends on:** [Chapter 04: Gradient Methods & CG], [Diagonal Dominance], [Matrix Inversion]  
**Lecture Reference:** Slides 32–34

---

## The Intuition: Reshaping the Canyon

* **The Problem:** In Chapter 04, we saw that Conjugate Gradients (CG) is theoretical perfection, but on stiff engineering matrices, numerical roundoff errors destroy orthogonality and cause the algorithm to stall after dozens of steps.
* **The Diagnosis:** The shape of the energy landscape is determined by the **eigenvalue spectrum** of $\mathbf{A}$. If the eigenvalues are scattered across many orders of magnitude ($\lambda_{\max} / \lambda_{\min} \gg 1$), the energy bowl is a warped, twisted crevasse.
* **The Cure (Preconditioning):** We cannot change the physical laws of our system, but we can multiply both sides of $\mathbf{A}\mathbf{x} = \mathbf{b}$ by an intelligent transformation matrix $\mathbf{Z}$:
  $$\mathbf{Z}\mathbf{A}\mathbf{x} = \mathbf{Z}\mathbf{b}$$
* **The Goal of $\mathbf{Z}$:** We want $\mathbf{Z} \approx \mathbf{A}^{-1}$. If $\mathbf{Z}$ is a good approximation of the inverse, then the new system matrix $\widetilde{\mathbf{A}} = \mathbf{Z}\mathbf{A} \approx \mathbf{I}$ (the identity matrix!).
* **The Result:** The twisted crevasse is reshaped into an almost perfectly spherical bowl. All eigenvalues cluster tightly around $1.0$. Conjugate Gradients now races to machine precision in a handful of iterations!

```
    [Raw System: Twisted Canyon]                [Preconditioned: Spherical Bowl]
            κ(A) = 10⁶                                     κ(ZA) ≈ 1.05
                 |                                                |
          (Slow, Stalling)                              (Fires in < 20 steps)
              \     /                                           ( * )
               \   /                                           /     \
                \_/                                           (   x*  )
                 v                                             \     /
                x*                                              ( * )
```

---

## The Detail: The Preconditioned Conjugate Gradient (PCG) Framework

As Dr. Sewell emphasizes on **Slide 32**, to solve $\mathbf{A}\mathbf{x} = \mathbf{b}$ for large sparse $\mathbf{A}$, we seek a matrix $\mathbf{Z}$ that satisfies two conflicting engineering criteria:
1. **Faithfulness:** $\mathbf{Z}$ must be a sufficiently close approximation to $\mathbf{A}^{-1}$ so that $\mathbf{Z}\mathbf{A} \approx \mathbf{I}$.
2. **Computational Cheapness:** $\mathbf{Z}$ must be **sparse** and trivial to evaluate or invert. (If computing $\mathbf{Z}$ were as difficult as computing $\mathbf{A}^{-1}$, we would be back to our original impossible problem!).

### What the Preconditioned Matrix Looks Like

If $\mathbf{Z}\mathbf{A} \approx \mathbf{I}$, the product looks like:

$$\mathbf{Z}\mathbf{A} = \begin{bmatrix}
\mathbf{1.0001} & 10^{-2} & 10^{-4} & 10^{-6} \\
10^{-2} & \mathbf{0.9999} & 10^{-2} & 10^{-4} \\
10^{-4} & 10^{-2} & \mathbf{1.0010} & 10^{-2} \\
10^{-6} & 10^{-4} & 10^{-2} & \mathbf{1.0000}
\end{bmatrix}$$

Notice:
* The main diagonal entries are all within $0.01\%$ of $1.0$.
* The off-diagonal coupling terms are tiny parasitic residuals ($10^{-2}$ to $10^{-6}$).
* This matrix is heavily **diagonally dominant**. The condition number drops from $\kappa \sim 10^6$ to $\kappa \sim 1.05$.

---

## Matrix Splitting: Jacobi and Gauss-Seidel (Slide 33)

Where do practical preconditioners come from? The simplest family stems from **Matrix Splitting**.

Suppose we decompose $\mathbf{A}$ into an "easy" part and a "hard" part:

$$\mathbf{A} = \mathbf{D} + \mathbf{E}$$

where:
* $\mathbf{D}$ contains only the diagonal elements of $\mathbf{A}$ (trivial to store and invert).
* $\mathbf{E}$ contains all the off-diagonal elements of $\mathbf{A}$ (the coupling terms).

$$\mathbf{A} = \begin{bmatrix}
A_{00} & A_{01} & A_{02} \\
A_{10} & A_{11} & A_{12} \\
A_{20} & A_{21} & A_{22}
\end{bmatrix}, \quad
\mathbf{D} = \begin{bmatrix}
A_{00} & 0 & 0 \\
0 & A_{11} & 0 \\
0 & 0 & A_{22}
\end{bmatrix}, \quad
\mathbf{E} = \begin{bmatrix}
0 & A_{01} & A_{02} \\
A_{10} & 0 & A_{12} \\
A_{20} & A_{21} & 0
\end{bmatrix}$$

Now rewrite the linear system $\mathbf{A}\mathbf{x} = \mathbf{b}$:

$$(\mathbf{D} + \mathbf{E})\mathbf{x} = \mathbf{b} \implies \mathbf{D}\mathbf{x} = \mathbf{b} - \mathbf{E}\mathbf{x}$$

### 1. Gauss-Jacobi Iteration

Turn this into an iterative recurrence relation:

$$\mathbf{D}\mathbf{x}_{k+1} = \mathbf{b} - \mathbf{E}\mathbf{x}_k$$

Since $\mathbf{D}$ is purely diagonal, "solving" for $\mathbf{x}_{k+1}$ does not require Gaussian elimination or LU decomposition! It requires simply dividing each component by a single scalar:

$$x_{k+1, i} = \frac{1}{A_{ii}} \left( b_i - \sum_{j \ne i} A_{ij} x_{k, j} \right)$$

* **Storage:** No fill-in whatsoever.
* **Cost:** Exactly $O(\text{NNZ})$ operations per step.

### 2. Gauss-Seidel Iteration

In Jacobi iteration, when computing $x_{k+1, 2}$, you still use the old value $x_{k, 1}$ from the previous iteration.  
In **Gauss-Seidel**, the moment an updated variable is computed, it is immediately plugged into the subsequent equations in the same pass!

We split $\mathbf{A} = \mathbf{D} - \mathbf{L} - \mathbf{U}$ (where $-\mathbf{L}$ is strictly lower triangular and $-\mathbf{U}$ is strictly upper triangular):

$$(\mathbf{D} - \mathbf{L})\mathbf{x}_{k+1} = \mathbf{U}\mathbf{x}_k + \mathbf{b}$$

Because $(\mathbf{D} - \mathbf{L})$ is lower triangular, $\mathbf{x}_{k+1}$ is computed via immediate **forward substitution**:

$$x_{k+1, i} = \frac{1}{A_{ii}} \left( b_i - \sum_{j < i} A_{ij} x_{k+1, j} - \sum_{j > i} A_{ij} x_{k, j} \right)$$

* **Convergence:** Typically twice as fast as Jacobi.

---

## Splittings as Preconditioners

While Jacobi and Gauss-Seidel can act as standalone solvers, their true modern power is serving as **Preconditioners ($\mathbf{Z}$)** for Conjugate Gradients:

1. **Jacobi (Diagonal) Preconditioner:**
   $$\mathbf{Z} = \mathbf{D}^{-1} = \text{diag}\left(\frac{1}{A_{11}}, \frac{1}{A_{22}}, \dots, \frac{1}{A_{NN}}\right)$$
   Costs almost nothing to compute; normalizes all diagonal entries to exactly $1$.
2. **Incomplete Cholesky / Incomplete LU (IC / ILU):**
   Perform standard LU factorization, but enforce a strict sparsity rule: **if a fill-in entry falls on a position $(i,j)$ where the original matrix $A_{ij} == 0$, drop it immediately!**  
   This creates an approximate factor pair $\mathbf{L}\mathbf{U} \approx \mathbf{A}$ with **zero memory growth**, giving a potent preconditioner $\mathbf{Z} = (\mathbf{L}\mathbf{U})^{-1}$.

---

## The Industrial Reality of Iterative Solvers (Slide 34)

Dr. Phil Sewell concludes this section with profound practical advice derived from decades of industrial CAD simulation experience:

### Question 1: How many flavours of iterative methods are there?
There is an entire zoo of iterative algorithms tailored to different mathematical structures:
* **Conjugate Gradients (CG):** Symmetric Positive Definite matrices (electrostatics, heat diffusion, structural mechanics).
* **MINRES / SYMMLQ:** Symmetric Indefinite matrices.
* **BiCGSTAB / GMRES:** General non-symmetric, non-Hermitian matrices (high-frequency wave scattering, Navier-Stokes fluid dynamics).

### Question 2: How long do they take to converge in real engineering?

> [!WARNING]
> **The Golden Rule of Engineering Simulation (Dr. Phil Sewell):**  
> *"My experience is that even for very large problems, unless you have strong convergence in less than 100 iterations, it is unlikely to ever converge: Preconditioning is the absolutely critical must."*

Why?
If an iterative algorithm has not converged after 100 iterations on a matrix with millions of nodes:
1. Floating-point roundoff errors will have completely polluted the search subspace.
2. The residual error will stall on an asymptotic plateau (numerical stagnation).
3. The only way forward is not to let the computer grind for 10,000 steps, but to **stop the solver and redesign the preconditioner $\mathbf{Z}$**.

---

## Key Takeaways & Self-Check

1. **What is preconditioning?** Transforming $\mathbf{A}\mathbf{x} = \mathbf{b}$ into $\mathbf{Z}\mathbf{A}\mathbf{x} = \mathbf{Z}\mathbf{b}$ where $\mathbf{Z} \approx \mathbf{A}^{-1}$ to cluster the eigenvalues near $1$ and squash the condition number.
2. **How does Jacobi splitting avoid fill-in?** It isolates the diagonal $\mathbf{D}$, reducing matrix "inversion" to simple scalar division by $A_{ii}$.
3. **What is the practical convergence threshold?** If an iterative method does not reach convergence within $\sim 100$ iterations, the conditioning is defective; no amount of extra CPU time will save it without preconditioning.

Next chapter: [**`06_structured_matrices_and_node_ordering.md`**](file:///home/nicholas/projects/y4_ee/modules/EEEE3116_adv_eng_math/concepts/zeroes_lecture/06_structured_matrices_and_node_ordering.md) — How does the physical geometry of 1D vs 2D meshes create banded structures, and why does node indexing order make or break performance?

