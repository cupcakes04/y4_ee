import numpy as np

def test_rotation_matrix():
    print("Testing Rotation Matrix Orthonormality and Determinant...")
    for phi, theta, psi in [(0.1, 0.2, 0.3), (-0.5, 0.4, -1.2), (0.0, 0.0, 0.0)]:
        c_p, s_p = np.cos(phi), np.sin(phi)
        c_t, s_t = np.cos(theta), np.sin(theta)
        c_ps, s_ps = np.cos(psi), np.sin(psi)
        
        R = np.array([
            [c_t * c_ps, s_p * s_t * c_ps - c_p * s_ps, c_p * s_t * c_ps + s_p * s_ps],
            [c_t * s_ps, s_p * s_t * s_ps + c_p * c_ps, c_p * s_t * s_ps - s_p * c_ps],
            [-s_t, s_p * c_t, c_p * c_t]
        ])
        
        assert np.allclose(R.T @ R, np.eye(3)), "R^T R != I"
        assert np.isclose(np.linalg.det(R), 1.0), "det(R) != 1"
    print("  [PASS] Rotation matrix tests passed.")

def test_allocation_matrices():
    print("Testing Allocation Matrix Inverses...")
    # Plus configuration
    l = 0.25
    k_MT = 0.015
    A_plus = np.array([
        [-1, -1, -1, -1],
        [0, -l, 0, l],
        [l, 0, -l, 0],
        [k_MT, -k_MT, k_MT, -k_MT]
    ])
    A_plus_inv_expected = np.array([
        [-1/4, 0, 1/(2*l), 1/(4*k_MT)],
        [-1/4, -1/(2*l), 0, -1/(4*k_MT)],
        [-1/4, 0, -1/(2*l), 1/(4*k_MT)],
        [-1/4, 1/(2*l), 0, -1/(4*k_MT)]
    ])
    assert np.allclose(np.linalg.inv(A_plus), A_plus_inv_expected), "Plus inverse failed"
    print("  [PASS] Plus allocation matrix inverse verified.")

    # Cross configuration
    d = l / np.sqrt(2)
    A_cross = np.array([
        [-1, -1, -1, -1],
        [d, -d, -d, d],
        [d, d, -d, -d],
        [k_MT, -k_MT, k_MT, -k_MT]
    ])
    A_cross_inv_expected = np.array([
        [-1/4, 1/(4*d), 1/(4*d), 1/(4*k_MT)],
        [-1/4, -1/(4*d), 1/(4*d), -1/(4*k_MT)],
        [-1/4, -1/(4*d), -1/(4*d), 1/(4*k_MT)],
        [-1/4, 1/(4*d), -1/(4*d), -1/(4*k_MT)]
    ])
    assert np.allclose(np.linalg.inv(A_cross), A_cross_inv_expected), "Cross inverse failed"
    print("  [PASS] Cross allocation matrix inverse verified.")

    # Hexarotor configuration
    beta = np.radians([-30, 30, 90, 150, 210, 270])
    x = l * np.cos(beta)
    y = l * np.sin(beta)
    sigma = np.array([1, -1, 1, -1, 1, -1])
    
    A_hex = np.array([
        [-1, -1, -1, -1, -1, -1],
        [l/2, -l/2, -l, -l/2, l/2, l],
        [np.sqrt(3)*l/2, np.sqrt(3)*l/2, 0, -np.sqrt(3)*l/2, -np.sqrt(3)*l/2, 0],
        [k_MT, -k_MT, k_MT, -k_MT, k_MT, -k_MT]
    ])
    # Pseudo-inverse property: A_hex @ A_hex_pinv = I_4
    pinv = np.linalg.pinv(A_hex)
    assert np.allclose(A_hex @ pinv, np.eye(4)), "Hex pseudo-inverse failed"
    print("  [PASS] Hexarotor allocation pseudo-inverse verified.")

def test_motor_lag_stability():
    print("Testing Motor Lag Routh-Hurwitz Stability Condition...")
    tau_m = 0.02
    k_p = 625.0
    
    # Stable case: k_d > tau_m * k_p = 0.02 * 625 = 12.5
    k_d_stable = 35.0
    poly_stable = [tau_m, 1.0, k_d_stable, k_p]
    roots_stable = np.roots(poly_stable)
    assert np.all(np.real(roots_stable) < 0), "Stable polynomial had unstable roots!"
    
    # Unstable case: k_d < tau_m * k_p
    k_d_unstable = 10.0
    poly_unstable = [tau_m, 1.0, k_d_unstable, k_p]
    roots_unstable = np.roots(poly_unstable)
    assert np.any(np.real(roots_unstable) > 0), "Unstable polynomial had no unstable roots!"
    print("  [PASS] Motor lag stability criterion (kd > tau_m * kp) verified via root locus.")

def test_controllability_observability():
    print("Testing Controllability and Observability of Hover Models...")
    # Vertical channel
    m = 1.5
    A_vert = np.array([[0, 1], [0, 0]])
    B_vert = np.array([[0], [-1/m]])
    C_vert = np.array([[1, 0]])
    
    C_mat = np.hstack([B_vert, A_vert @ B_vert])
    O_mat = np.vstack([C_vert, C_vert @ A_vert])
    assert np.linalg.matrix_rank(C_mat) == 2, "Vertical not controllable"
    assert np.linalg.matrix_rank(O_mat) == 2, "Vertical not observable"
    
    # Longitudinal channel (4-state)
    g = 9.81
    Jy = 0.005
    A_long = np.array([
        [0, 1, 0, 0],
        [0, 0, -g, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ])
    B_long = np.array([[0], [0], [0], [1/Jy]])
    C_long = np.array([[1, 0, 0, 0]])
    
    AB = A_long @ B_long
    A2B = A_long @ AB
    A3B = A_long @ A2B
    C_long_mat = np.hstack([B_long, AB, A2B, A3B])
    CA = C_long @ A_long
    CA2 = CA @ A_long
    CA3 = CA2 @ A_long
    O_long_mat = np.vstack([C_long, CA, CA2, CA3])
    
    assert np.linalg.matrix_rank(C_long_mat) == 4, "Longitudinal not controllable"
    assert np.linalg.matrix_rank(O_long_mat) == 4, "Longitudinal not observable"
    print("  [PASS] Full 4-state longitudinal and 2-state vertical controllability & observability verified.")

if __name__ == '__main__':
    test_rotation_matrix()
    test_allocation_matrices()
    test_motor_lag_stability()
    test_controllability_observability()
    print("\nALL MATHEMATICAL AND CONTROL SPECIFICATION TESTS PASSED SUCCESSFULLY!")
