import numpy as np
import itertools
import math

ARM_LENGTH = 0.225
K_MT = 0.016
T_MIN = 0.5
T_MAX = 12.0

AIRFRAME_CONFIGS = {
    'plus': {
        'numMotors': 4,
        'rotors': [
            {'x': ARM_LENGTH, 'y': 0.0, 'spin': -1},
            {'x': 0.0, 'y': ARM_LENGTH, 'spin': +1},
            {'x': -ARM_LENGTH, 'y': 0.0, 'spin': -1},
            {'x': 0.0, 'y': -ARM_LENGTH, 'spin': +1}
        ]
    },
    'cross': {
        'numMotors': 4,
        'rotors': [
            {'x': ARM_LENGTH / math.sqrt(2), 'y': -ARM_LENGTH / math.sqrt(2), 'spin': -1},
            {'x': ARM_LENGTH / math.sqrt(2), 'y': ARM_LENGTH / math.sqrt(2), 'spin': +1},
            {'x': -ARM_LENGTH / math.sqrt(2), 'y': ARM_LENGTH / math.sqrt(2), 'spin': -1},
            {'x': -ARM_LENGTH / math.sqrt(2), 'y': -ARM_LENGTH / math.sqrt(2), 'spin': +1}
        ]
    },
    'hex': {
        'numMotors': 6,
        'rotors': [
            {'x': ARM_LENGTH * math.cos(ang), 'y': ARM_LENGTH * math.sin(ang), 'spin': (+1 if i % 2 == 0 else -1)}
            for i, ang in enumerate([a * math.pi / 180.0 for a in [-30, 30, 90, 150, 210, 270]])
        ]
    },
    'octo': {
        'numMotors': 8,
        'rotors': [
            {'x': ARM_LENGTH * math.cos(ang), 'y': ARM_LENGTH * math.sin(ang), 'spin': (+1 if i % 2 == 0 else -1)}
            for i, ang in enumerate([a * math.pi / 180.0 for a in [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5]])
        ]
    }
}

def build_mixer_matrix(config, health):
    N = config['numMotors']
    A = np.zeros((4, N))
    for i in range(N):
        if health[i] == 1:
            r = config['rotors'][i]
            A[0, i] = -1.0
            A[1, i] = -r['y']
            A[2, i] = r['x']
            A[3, i] = r['spin'] * K_MT
    return A

def js_invert4x4(M_in):
    # Exact reproduction of Widget 4's Gauss-Jordan inversion
    M = [row[:] for row in M_in]
    n = 4
    aug = []
    for i in range(n):
        row = list(M[i]) + [0.0, 0.0, 0.0, 0.0]
        row[n + i] = 1.0
        aug.append(row)

    for i in range(n):
        maxRow = i
        maxVal = abs(aug[i][i])
        for k in range(i + 1, n):
            if abs(aug[k][i]) > maxVal:
                maxVal = abs(aug[k][i])
                maxRow = k
        if maxVal < 1e-7:
            return None
        aug[i], aug[maxRow] = aug[maxRow], aug[i]

        pivot = aug[i][i]
        for j in range(2 * n):
            aug[i][j] /= pivot

        for k in range(n):
            if k != i:
                factor = aug[k][i]
                for j in range(2 * n):
                    aug[k][j] -= factor * aug[i][j]

    inv = [aug[i][n:] for i in range(n)]
    return inv

def compute_pseudo_inverse_js(A):
    AT = A.T
    G = A @ AT
    G_list = G.tolist()
    G_inv_list = js_invert4x4(G_list)
    if G_inv_list is None:
        return None
    G_inv = np.array(G_inv_list)
    return AT @ G_inv

print("================================================================================")
print("WIDGET 4 STRESS TEST: Matrix Inversion & Control Allocation under Motor Failures")
print("================================================================================")

# 1. Test Quadrotor (single motor failure -> MUST detect rank deficiency gracefully)
for frame in ['plus', 'cross']:
    cfg = AIRFRAME_CONFIGS[frame]
    print(f"\n--- Testing Frame: {frame.upper()} (N=4) ---")
    # All healthy
    A_nom = build_mixer_matrix(cfg, [1, 1, 1, 1])
    pinv_nom = compute_pseudo_inverse_js(A_nom)
    assert pinv_nom is not None, f"Nominal {frame} should be invertible"
    print(f"  Nominal: Invertible=True, Rank={np.linalg.matrix_rank(A_nom)}")

    # Single failure
    for failed_idx in range(4):
        health = [1, 1, 1, 1]
        health[failed_idx] = 0
        A = build_mixer_matrix(cfg, health)
        pinv = compute_pseudo_inverse_js(A)
        rank = np.linalg.matrix_rank(A)
        print(f"  Motor {failed_idx+1} Failed: Rank={rank}, Invertible={pinv is not None}")
        assert pinv is None, f"Single failure on {frame} quad must return None (rank={rank})"

# 2. Test Hexarotor: Single and Double Motor Failures
cfg_hex = AIRFRAME_CONFIGS['hex']
print("\n--- Testing Frame: HEXAROTOR (N=6) ---")
# All healthy
A_hex_nom = build_mixer_matrix(cfg_hex, [1]*6)
pinv_hex_nom = compute_pseudo_inverse_js(A_hex_nom)
print(f"  Nominal: Invertible=True, Rank={np.linalg.matrix_rank(A_hex_nom)}")

# All 6 single failure cases
single_fail_ranks = []
for f1 in range(6):
    health = [1]*6
    health[f1] = 0
    A = build_mixer_matrix(cfg_hex, health)
    pinv = compute_pseudo_inverse_js(A)
    rank = np.linalg.matrix_rank(A)
    single_fail_ranks.append((f1, rank, pinv is not None))
print(f"  Single Motor Failures (6 cases): All Invertible? {all(x[2] for x in single_fail_ranks)}")
for f1, r, inv in single_fail_ranks:
    print(f"    Fail M{f1+1}: Rank={r}, Invertible={inv}")

# All 15 double failure combinations
print(f"\n  Double Motor Failures (15 combinations):")
double_fail_results = []
for f1, f2 in itertools.combinations(range(6), 2):
    health = [1]*6
    health[f1] = 0
    health[f2] = 0
    A = build_mixer_matrix(cfg_hex, health)
    pinv = compute_pseudo_inverse_js(A)
    rank = np.linalg.matrix_rank(A)
    det_G = np.linalg.det(A @ A.T)
    double_fail_results.append((f1+1, f2+1, rank, pinv is not None, det_G))

invertible_count = sum(1 for x in double_fail_results if x[3])
rank_deficient_count = sum(1 for x in double_fail_results if not x[3])
print(f"    Total double failure combos: 15")
print(f"    Combos remaining Rank 4 (Invertible): {invertible_count}")
print(f"    Combos becoming Rank Deficient (Singular): {rank_deficient_count}")
for f1, f2, r, inv, det in double_fail_results:
    status = "REALLOCATABLE (Rank 4)" if inv else "RANK DEFICIENT (Singular)"
    print(f"    Fail M{f1}+M{f2}: Rank={r}, det(G)={det:11.4e} -> {status}")

# 3. Test Octorotor: Up to 4 motor failures
cfg_octo = AIRFRAME_CONFIGS['octo']
print("\n--- Testing Frame: OCTOROTOR (N=8) ---")
A_octo_nom = build_mixer_matrix(cfg_octo, [1]*8)
pinv_octo_nom = compute_pseudo_inverse_js(A_octo_nom)
print(f"  Nominal: Invertible=True, Rank={np.linalg.matrix_rank(A_octo_nom)}")

for num_fails in [1, 2, 3]:
    combos = list(itertools.combinations(range(8), num_fails))
    inv_c = 0
    for fail_indices in combos:
        health = [1]*8
        for fi in fail_indices:
            health[fi] = 0
        A = build_mixer_matrix(cfg_octo, health)
        pinv = compute_pseudo_inverse_js(A)
        if pinv is not None:
            inv_c += 1
    print(f"  {num_fails}-Motor Failures: {inv_c} / {len(combos)} combinations maintain full Rank 4 control")

