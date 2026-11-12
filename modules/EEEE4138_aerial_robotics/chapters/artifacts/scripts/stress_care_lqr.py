import numpy as np
import scipy.linalg
import json
import subprocess
import sys

g = 9.81
Jy = 0.035
A = np.array([
    [0, 1, 0, 0],
    [0, 0, -g, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0]
], dtype=float)
B = np.array([[0], [0], [0], [1.0 / Jy]], dtype=float)

test_cases = [
    {'name': 'Nominal UI', 'qx': 4.0, 'qv': 1.0, 'qtheta': 8.0, 'qq': 0.5, 'ru': 2.0},
    {'name': 'Min UI Bounds', 'qx': 0.1, 'qv': 0.1, 'qtheta': 0.1, 'qq': 0.05, 'ru': 20.0},
    {'name': 'Max UI Bounds', 'qx': 50.0, 'qv': 25.0, 'qtheta': 50.0, 'qq': 10.0, 'ru': 0.1},
    {'name': 'Heavy Position Penalty', 'qx': 50.0, 'qv': 0.1, 'qtheta': 0.1, 'qq': 0.05, 'ru': 1.0},
    {'name': 'Heavy Attitude Penalty', 'qx': 0.1, 'qv': 0.1, 'qtheta': 50.0, 'qq': 10.0, 'ru': 0.1},
    {'name': 'Cheap Control (ru=0.05)', 'qx': 10.0, 'qv': 5.0, 'qtheta': 10.0, 'qq': 1.0, 'ru': 0.05},
    {'name': 'Expensive Control (ru=100.0)', 'qx': 1.0, 'qv': 0.5, 'qtheta': 1.0, 'qq': 0.1, 'ru': 100.0},
    {'name': 'Extreme Skewed', 'qx': 100.0, 'qv': 1.0, 'qtheta': 100.0, 'qq': 5.0, 'ru': 0.01},
]

def js_solve_lqr(qx, qv, qtheta, qq, ru, max_iters=12):
    # Python reproduction of exact JS code in Widget 5 lines 588-701
    A_mat = [
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, -g, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 0.0]
    ]
    B_vec = [0.0, 0.0, 0.0, 1.0 / Jy]
    Q_mat = [
        [qx, 0.0, 0.0, 0.0],
        [0.0, qv, 0.0, 0.0],
        [0.0, 0.0, qtheta, 0.0],
        [0.0, 0.0, 0.0, qq]
    ]
    R_val = ru
    invR = 1.0 / R_val

    lookup = [
        [0, 1, 2, 3],
        [1, 4, 5, 6],
        [2, 5, 7, 8],
        [3, 6, 8, 9]
    ]

    def solveLyap(F, M):
        Asys = [[0.0]*10 for _ in range(10)]
        bsys = [0.0]*10
        eq = 0
        for i in range(4):
            for j in range(i, 4):
                for k in range(4):
                    Asys[eq][lookup[k][j]] += F[k][i]
                    Asys[eq][lookup[i][k]] += F[k][j]
                bsys[eq] = -M[i][j]
                eq += 1

        p = [0.0]*10
        for i in range(10):
            maxRow = i
            for r in range(i + 1, 10):
                if abs(Asys[r][i]) > abs(Asys[maxRow][i]):
                    maxRow = r
            if maxRow != i:
                Asys[i], Asys[maxRow] = Asys[maxRow], Asys[i]
                bsys[i], bsys[maxRow] = bsys[maxRow], bsys[i]

            pivot = Asys[i][i]
            if abs(pivot) < 1e-12:
                continue
            for r in range(i + 1, 10):
                factor = Asys[r][i] / pivot
                for c in range(i, 10):
                    Asys[r][c] -= factor * Asys[i][c]
                bsys[r] -= factor * bsys[i]

        for i in range(9, -1, -1):
            s = bsys[i]
            for c in range(i + 1, 10):
                s -= Asys[i][c] * p[c]
            p[i] = s / Asys[i][i] if Asys[i][i] != 0 else 0.0

        P_res = [[0.0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                P_res[i][j] = p[lookup[i][j]]
        return P_res

    K = [-0.5, -1.0, 2.0, 0.5]
    itersRun = 0
    converged = False
    for iter_idx in range(max_iters):
        itersRun += 1
        F = [[0.0]*4 for _ in range(4)]
        for r in range(4):
            for c in range(4):
                F[r][c] = A_mat[r][c] - B_vec[r] * K[c]

        M = [[0.0]*4 for _ in range(4)]
        for r in range(4):
            for c in range(4):
                M[r][c] = Q_mat[r][c] + K[r] * R_val * K[c]

        P = solveLyap(F, M)

        K_new = [0.0]*4
        for c in range(4):
            K_new[c] = invR * (B_vec[0]*P[0][c] + B_vec[1]*P[1][c] + B_vec[2]*P[2][c] + B_vec[3]*P[3][c])

        diff = sum(abs(K_new[c] - K[c]) for c in range(4))
        K = K_new
        if diff < 1e-5:
            converged = True
            break
    return K, itersRun, converged

print("================================================================================")
print("CARE SOLVER EMPIRICAL COMPARISON: Widget 5 (Newton-Kleinman) vs SciPy ARE Baseline")
print("================================================================================")

for tc in test_cases:
    Q = np.diag([tc['qx'], tc['qv'], tc['qtheta'], tc['qq']])
    R = np.array([[tc['ru']]])
    P_scipy = scipy.linalg.solve_continuous_are(A, B, Q, R)
    K_scipy = (np.linalg.inv(R) @ B.T @ P_scipy).flatten()

    K_js, iters, conv = js_solve_lqr(tc['qx'], tc['qv'], tc['qtheta'], tc['qq'], tc['ru'])
    K_js_arr = np.array(K_js)

    diff = np.abs(K_js_arr - K_scipy)
    max_err = np.max(diff)
    rel_err = max_err / (np.max(np.abs(K_scipy)) + 1e-9)

    status = "EXACT MATCH" if max_err < 1e-4 else ("CONVERGED" if max_err < 1e-2 else "DIVERGED/MISMATCH")

    print(f"\nScenario: {tc['name']}")
    print(f"  Weights: Q=[{tc['qx']}, {tc['qv']}, {tc['qtheta']}, {tc['qq']}], R={tc['ru']}")
    print(f"  Widget 5 Gain : [{K_js[0]:9.4f}, {K_js[1]:9.4f}, {K_js[2]:9.4f}, {K_js[3]:9.4f}] (iters: {iters:2d}, conv={conv})")
    print(f"  SciPy ARE Gain: [{K_scipy[0]:9.4f}, {K_scipy[1]:9.4f}, {K_scipy[2]:9.4f}, {K_scipy[3]:9.4f}]")
    print(f"  Max Absolute Error: {max_err:10.4e} | Rel Error: {rel_err:10.4e} -> {status}")

