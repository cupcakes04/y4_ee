#!/usr/bin/env python3
"""
test_adversarial_physics.py
===========================
Adversarial Verification & Mathematical Physics Stress-Test Harness
for EEEE4138 Aerial Robotics.

Challenger 1 (Mathematical & Physics Adversarial Verifier)

Test Domains:
  1. Actuator Disc Momentum Theory: asymptotic inflow limits (m -> 0, m -> inf),
     vacuum limits (rho -> 0), disc area limits (A -> 0, A -> inf), and convexity.
  2. Attitude Kinematics & Extreme Orientations: SO(3) orthonormality and det(R) = 1
     at theta = +-89.99 deg and +-90.0 deg; Euler gimbal lock singularity;
     unit quaternion invariant ||q|| = 1; quaternion derivative linearity.
  3. Transport Theorem & 6-DoF Dynamics: Coriolis acceleration identity across
     arbitrary rotating frames; catastrophic error quantification of naive translation;
     Coriolis zero-work energetic invariant; gyroscopic torque cross-coupling.
  4. Mixer Matrix Inverses & Allocation: Analytical inverses for Plus (+) and Cross (x)
     quadrotors; ill-conditioning analysis; Moore-Penrose pseudo-inverse for hexarotors;
     minimum 2-norm uniqueness; quadrotor vs hexarotor fault tolerance.
  5. Motor Lag Closed-Loop Stability & Bifurcation: Characteristic polynomial roots;
     exact marginal stability on imaginary axis (kd = tau_m * kp); unstable right half-plane
     crossing (kd < tau_m * kp); Hopf bifurcation.
  6. State-Space Longitudinal Controllability & Observability: Symbolic and numerical
     proof that det(C) = g^2 / Jy^4 != 0; rank 4 controllability; position vs angle
     observability; LQR Riccati solver & closed-loop Hurwitz spectrum.
"""

import sys
import math
import unittest
import numpy as np
import sympy as sp
from scipy import linalg

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class TestActuatorDiscMomentumLimits(unittest.TestCase):
    """Stress-test 1D Actuator Disc Momentum Theory under extreme physical limits."""

    def setUp(self):
        self.rho_std = 1.225  # kg/m^3 (sea-level air density)
        self.g = 9.81         # m/s^2
        self.R = 0.127        # 5-inch prop radius (m)
        self.A = math.pi * (self.R ** 2)

    def test_mass_approaching_zero(self):
        """As mass m -> 0+, induced velocity, power, and disc loading vanish, while PL -> inf."""
        masses = [1e-3, 1e-6, 1e-9, 1e-12]
        prev_vi = float("inf")
        prev_Pi = float("inf")
        prev_PL = 0.0

        for m in masses:
            T = m * self.g
            vi = math.sqrt(T / (2.0 * self.rho_std * self.A))
            Pi = (T ** 1.5) / math.sqrt(2.0 * self.rho_std * self.A)
            DL = T / self.A
            PL = math.sqrt(2.0 * self.rho_std / DL)

            # Monotonic convergence to zero
            self.assertLess(vi, prev_vi)
            self.assertLess(Pi, prev_Pi)
            self.assertGreater(vi, 0.0)
            self.assertGreater(Pi, 0.0)
            self.assertGreater(PL, prev_PL)  # Power loading strictly increases as mass shrinks

            prev_vi = vi
            prev_Pi = Pi
            prev_PL = PL

        # At the extreme limit (m = 1e-12 kg), PL has diverged past 1e5 N/W
        self.assertGreater(prev_PL, 1e5)

        # At the limit m = 0
        vi_zero = math.sqrt(0.0 / (2.0 * self.rho_std * self.A))
        self.assertEqual(vi_zero, 0.0)

    def test_mass_approaching_infinity(self):
        """As mass m -> inf, induced velocity and power diverge to infinity."""
        masses = [1e2, 1e4, 1e6, 1e8]
        prev_vi = 0.0
        prev_Pi = 0.0

        for m in masses:
            T = m * self.g
            vi = math.sqrt(T / (2.0 * self.rho_std * self.A))
            Pi = (T ** 1.5) / math.sqrt(2.0 * self.rho_std * self.A)
            DL = T / self.A
            PL = math.sqrt(2.0 * self.rho_std / DL)

            self.assertGreater(vi, prev_vi)
            self.assertGreater(Pi, prev_Pi)
            self.assertLess(PL, 0.1)  # Power loading drops to near zero

            prev_vi = vi
            prev_Pi = Pi

    def test_vacuum_limit_zero_density(self):
        """In a vacuum (rho -> 0), aerodynamic hover requires infinite induced velocity and infinite power."""
        m = 1.0  # 1 kg drone
        T = m * self.g
        rhos = [1.0, 1e-2, 1e-4, 1e-6]
        prev_vi = 0.0

        for rho in rhos:
            vi = math.sqrt(T / (2.0 * rho * self.A))
            Pi = (T ** 1.5) / math.sqrt(2.0 * rho * self.A)
            self.assertGreater(vi, prev_vi)
            prev_vi = vi

        # Exact vacuum check: division by zero raises ZeroDivisionError
        with self.assertRaises(ZeroDivisionError):
            _ = math.sqrt(T / (2.0 * 0.0 * self.A))

    def test_disc_area_limits(self):
        """Infinite disc area requires zero power (v_i -> 0); point disc (A -> 0) requires infinite power."""
        m = 1.5
        T = m * self.g

        # Point disc limit (A -> 0)
        A_small = 1e-8
        vi_small = math.sqrt(T / (2.0 * self.rho_std * A_small))
        Pi_small = (T ** 1.5) / math.sqrt(2.0 * self.rho_std * A_small)
        self.assertGreater(vi_small, 1e4)
        self.assertGreater(Pi_small, 1e5)

        # Huge disc limit (A -> inf)
        A_large = 1e8
        vi_large = math.sqrt(T / (2.0 * self.rho_std * A_large))
        Pi_large = (T ** 1.5) / math.sqrt(2.0 * self.rho_std * A_large)
        self.assertLess(vi_large, 1e-3)
        self.assertLess(Pi_large, 1e-2)

    def test_symbolic_first_and_second_derivatives(self):
        """Prove strict monotonicity and convexity of ideal hover power with respect to mass."""
        m_sym, g_sym, rho_sym, A_sym = sp.symbols('m g rho A', positive=True)
        Pi_sym = ((m_sym * g_sym) ** sp.Rational(3, 2)) / sp.sqrt(2 * rho_sym * A_sym)

        dPi_dm = sp.diff(Pi_sym, m_sym)
        d2Pi_dm2 = sp.diff(dPi_dm, m_sym)

        # First derivative must be strictly positive: dPi/dm = (3/2) * g * sqrt(mg / (2 rho A)) > 0
        self.assertTrue(sp.simplify(dPi_dm > 0))
        # Second derivative must be strictly positive: d2Pi/dm^2 = (3/4) * g^2 / sqrt(2 rho A mg) > 0 (strictly convex)
        self.assertTrue(sp.simplify(d2Pi_dm2 > 0))


class TestAttitudeKinematicsAndQuaternions(unittest.TestCase):
    """Stress-test Direction Cosine Matrices at extreme pitch angles and unit quaternions."""

    def dcm_zyx(self, phi: float, theta: float, psi: float) -> np.ndarray:
        """Standard aerospace Tait-Bryan ZYX rotation matrix R_b^n."""
        c_phi, s_phi = math.cos(phi), math.sin(phi)
        c_th, s_th = math.cos(theta), math.sin(theta)
        c_psi, s_psi = math.cos(psi), math.sin(psi)

        R = np.array([
            [c_th * c_psi, s_phi * s_th * c_psi - c_phi * s_psi, c_phi * s_th * c_psi + s_phi * s_psi],
            [c_th * s_psi, s_phi * s_th * s_psi + c_phi * c_psi, c_phi * s_th * s_psi - s_phi * c_psi],
            [-s_th,        s_phi * c_th,                         c_phi * c_th]
        ], dtype=np.float64)
        return R

    def test_dcm_orthonormality_at_extreme_angles(self):
        """det(R) == 1 and R^T R == I_3 everywhere, including theta = +-89.99 deg and +-90.0 deg."""
        test_angles = [
            (0.0, math.radians(89.0), 0.0),
            (0.0, math.radians(-89.0), 0.0),
            (math.radians(45.0), math.radians(89.99), math.radians(30.0)),
            (math.radians(-30.0), math.radians(-89.99), math.radians(60.0)),
            (0.0, math.radians(89.999), 0.0),
            (0.0, math.radians(90.0), 0.0),      # Exact pitch vertical up
            (0.0, math.radians(-90.0), 0.0),     # Exact pitch vertical down
            (math.radians(180.0), 0.0, 0.0),     # Completely inverted
            (math.radians(45.0), math.radians(90.0), math.radians(-45.0)),
        ]

        I3 = np.eye(3, dtype=np.float64)
        for phi, theta, psi in test_angles:
            R = self.dcm_zyx(phi, theta, psi)
            det_R = np.linalg.det(R)
            ortho_error = np.linalg.norm(R.T @ R - I3, ord="fro")

            self.assertAlmostEqual(det_R, 1.0, places=13,
                                   msg=f"det(R) failed at angles ({phi}, {theta}, {psi})")
            self.assertLess(ortho_error, 1e-13,
                            msg=f"Orthogonality failed at angles ({phi}, {theta}, {psi})")

    def test_gimbal_lock_euler_rate_singularity(self):
        """At theta -> +-90 deg, Euler rate matrix W_eta diverges and condition number explodes."""
        pitches_deg = [0.0, 45.0, 80.0, 89.0, 89.9, 89.99]
        prev_cond = 0.0

        for pitch_deg in pitches_deg:
            th = math.radians(pitch_deg)
            # M_omega maps Euler rates to body rates: omega_b = M_omega * d_eta/dt
            # det(M_omega) = cos(th)
            M_omega = np.array([
                [1.0, 0.0, -math.sin(th)],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, math.cos(th)]
            ])
            cond = np.linalg.cond(M_omega)
            self.assertGreater(cond, prev_cond)
            prev_cond = cond

        # At theta = 89.99 deg, condition number exceeds 5000
        self.assertGreater(prev_cond, 5000.0)

        # At theta = 90.0 deg exact, M_omega is singular
        th_exact = math.radians(90.0)
        M_omega_exact = np.array([
            [1.0, 0.0, -math.sin(th_exact)],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, math.cos(th_exact)]
        ])
        det_M = np.linalg.det(M_omega_exact)
        self.assertAlmostEqual(det_M, 0.0, places=14)

    def test_unit_quaternion_norm_invariance(self):
        """Quaternion representation maintains ||q|| = 1.0 across random 3D rotations."""
        np.random.seed(42)
        I3 = np.eye(3)

        for _ in range(100):
            phi = np.random.uniform(-math.pi, math.pi)
            theta = np.random.uniform(-math.pi / 2, math.pi / 2)
            psi = np.random.uniform(-math.pi, math.pi)

            # Euler to Quaternion conversion
            c_p, s_p = math.cos(phi / 2), math.sin(phi / 2)
            c_t, s_t = math.cos(theta / 2), math.sin(theta / 2)
            c_ps, s_ps = math.cos(psi / 2), math.sin(psi / 2)

            q0 = c_p * c_t * c_ps + s_p * s_t * s_ps
            q1 = s_p * c_t * c_ps - c_p * s_t * s_ps
            q2 = c_p * s_t * c_ps + s_p * c_t * s_ps
            q3 = c_p * c_t * s_ps - s_p * s_t * c_ps

            q = np.array([q0, q1, q2, q3])
            norm_q = np.linalg.norm(q)
            self.assertAlmostEqual(norm_q, 1.0, places=14)

            # Direction cosine matrix from quaternion
            Rq = np.array([
                [1 - 2*(q2**2 + q3**2), 2*(q1*q2 - q0*q3),     2*(q1*q3 + q0*q2)],
                [2*(q1*q2 + q0*q3),     1 - 2*(q1**2 + q3**2), 2*(q2*q3 - q0*q1)],
                [2*(q1*q3 - q0*q2),     2*(q2*q3 + q0*q1),     1 - 2*(q1**2 + q2**2)]
            ])

            # Compare with Euler DCM
            Re = self.dcm_zyx(phi, theta, psi)
            fro_diff = np.linalg.norm(Rq - Re, ord="fro")
            self.assertLess(fro_diff, 1e-12)

    def test_quaternion_kinematic_derivative_regularity_at_gimbal_lock(self):
        """At theta = 90 deg, quaternion derivative q_dot = 0.5 * q x omega_b remains smooth and finite."""
        # Pure pitch up 90 deg
        theta = math.radians(90.0)
        c_t, s_t = math.cos(theta / 2), math.sin(theta / 2)
        q = np.array([c_t, 0.0, s_t, 0.0])  # Pitch quaternion

        omega_b = np.array([2.5, -1.8, 3.2])  # Nonzero body rates [p, q, r]

        # S(omega) matrix for quaternion kinematics
        p, q_rate, r = omega_b
        Omega_mat = np.array([
            [0, -p, -q_rate, -r],
            [p, 0, r, -q_rate],
            [q_rate, -r, 0, p],
            [r, q_rate, -p, 0]
        ])
        q_dot = 0.5 * Omega_mat @ q

        # q_dot must be finite and well-conditioned
        self.assertTrue(np.all(np.isfinite(q_dot)))
        # Invariant: d/dt(||q||^2) = 2 q^T q_dot = 0 (orthogonality of rate to unit sphere)
        rate_dot_product = np.dot(q, q_dot)
        self.assertAlmostEqual(rate_dot_product, 0.0, places=14)


class TestTransportTheoremAndCoriolis(unittest.TestCase):
    """Stress-test Transport Theorem, Coriolis acceleration, and rigid body dynamics."""

    def test_transport_theorem_kinematic_identity(self):
        """Verify: d/dt(R_b^n v_b) == R_b^n (v_dot_b + omega_b x v_b) for arbitrary 3D vectors."""
        np.random.seed(123)

        for _ in range(50):
            # Arbitrary orientation
            phi = np.random.uniform(-math.pi, math.pi)
            theta = np.random.uniform(-1.4, 1.4)
            psi = np.random.uniform(-math.pi, math.pi)

            c_phi, s_phi = math.cos(phi), math.sin(phi)
            c_th, s_th = math.cos(theta), math.sin(theta)
            c_psi, s_psi = math.cos(psi), math.sin(psi)

            R_b_n = np.array([
                [c_th * c_psi, s_phi * s_th * c_psi - c_phi * s_psi, c_phi * s_th * c_psi + s_phi * s_psi],
                [c_th * s_psi, s_phi * s_th * s_psi + c_phi * c_psi, c_phi * s_th * s_psi - s_phi * c_psi],
                [-s_th,        s_phi * c_th,                         c_phi * c_th]
            ])

            v_b = np.random.uniform(-10.0, 10.0, size=3)
            v_dot_b = np.random.uniform(-5.0, 5.0, size=3)
            omega_b = np.random.uniform(-3.0, 3.0, size=3)

            # Poisson's formula: R_dot = R * [omega_b x]
            omega_cross = np.array([
                [0.0, -omega_b[2], omega_b[1]],
                [omega_b[2], 0.0, -omega_b[0]],
                [-omega_b[1], omega_b[0], 0.0]
            ])
            R_dot = R_b_n @ omega_cross

            # Inertial acceleration derived via chain rule
            a_n_chain = R_dot @ v_b + R_b_n @ v_dot_b

            # Inertial acceleration derived via Transport Theorem
            a_n_transport = R_b_n @ (v_dot_b + np.cross(omega_b, v_b))

            diff = np.linalg.norm(a_n_chain - a_n_transport)
            self.assertLess(diff, 1e-12)

    def test_coriolis_acceleration_significance_and_zero_work(self):
        """Quantify Coriolis acceleration magnitude and prove zero-work invariant."""
        # Quadrotor moving forward at 15 m/s while yawing at 2 rad/s (115 deg/s)
        v_b = np.array([15.0, 0.0, 0.0])
        omega_b = np.array([0.0, 0.0, 2.0])

        coriolis = np.cross(omega_b, v_b)
        expected_coriolis = np.array([0.0, 30.0, 0.0])  # 30 m/s^2 sideways! (~ 3.06 g)

        self.assertTrue(np.allclose(coriolis, expected_coriolis))

        # Energetic invariant: Coriolis force does zero mechanical work
        work_rate = np.dot(v_b, coriolis)
        self.assertAlmostEqual(work_rate, 0.0, places=15)

    def test_rotational_cross_coupling_euler_dynamics(self):
        """Verify Euler's rotational equations and gyroscopic cross-coupling."""
        Jx, Jy, Jz = 0.025, 0.035, 0.045
        J = np.diag([Jx, Jy, Jz])
        omega = np.array([1.2, -0.8, 2.5])  # [p, q, r]
        tau_ext = np.array([0.15, -0.20, 0.05])

        # J * omega_dot + omega x (J * omega) = tau_ext
        # omega_dot = J^-1 * (tau_ext - omega x (J * omega))
        H = J @ omega
        cross_term = np.cross(omega, H)
        omega_dot = np.linalg.inv(J) @ (tau_ext - cross_term)

        # Expected p_dot = (tau_x - (Jz - Jy)*q*r) / Jx = (tau_x + (Jy - Jz)*q*r) / Jx
        expected_p_dot = (tau_ext[0] + (Jy - Jz) * omega[1] * omega[2]) / Jx
        expected_q_dot = (tau_ext[1] + (Jz - Jx) * omega[2] * omega[0]) / Jy
        expected_r_dot = (tau_ext[2] + (Jx - Jy) * omega[0] * omega[1]) / Jz

        self.assertAlmostEqual(omega_dot[0], expected_p_dot, places=14)
        self.assertAlmostEqual(omega_dot[1], expected_q_dot, places=14)
        self.assertAlmostEqual(omega_dot[2], expected_r_dot, places=14)


class TestMixerMatricesAndAllocation(unittest.TestCase):
    """Stress-test mixer matrix inverses for +, x quadrotors and Moore-Penrose pseudo-inverse for hexarotors."""

    def test_plus_and_cross_analytical_inverses(self):
        """Symbolically and numerically verify A * A^-1 == I_4."""
        l_sym, d_sym, k_sym = sp.symbols('l d kMT', positive=True)

        A_plus = sp.Matrix([
            [-1, -1, -1, -1],
            [0, -l_sym, 0, l_sym],
            [l_sym, 0, -l_sym, 0],
            [k_sym, -k_sym, k_sym, -k_sym]
        ])
        A_plus_inv = A_plus.inv()
        I_plus = sp.simplify(A_plus * A_plus_inv)
        self.assertEqual(I_plus, sp.eye(4))

        A_cross = sp.Matrix([
            [-1, -1, -1, -1],
            [d_sym, -d_sym, -d_sym, d_sym],
            [d_sym, d_sym, -d_sym, -d_sym],
            [k_sym, -k_sym, k_sym, -k_sym]
        ])
        A_cross_inv = A_cross.inv()
        I_cross = sp.simplify(A_cross * A_cross_inv)
        self.assertEqual(I_cross, sp.eye(4))

        # Check determinants: det(A_plus) = 8 * l^2 * k_MT, det(A_cross) = 16 * d^2 * k_MT
        det_plus = sp.simplify(A_plus.det())
        det_cross = sp.simplify(A_cross.det())
        self.assertEqual(det_plus, 8 * (l_sym ** 2) * k_sym)
        self.assertEqual(det_cross, 16 * (d_sym ** 2) * k_sym)

    def test_cross_configuration_control_authority_advantage(self):
        """Prove cross configuration provides sqrt(2) (~41.4%) more maximum roll/pitch torque than plus."""
        l = 0.25
        d = l / math.sqrt(2.0)
        dT = 5.0  # Thrust differential limit per motor (N)

        # For Plus configuration: roll torque is purely from rotors 2 & 4: M_x_max = l * dT
        Mx_max_plus = l * dT

        # For Cross configuration: all 4 rotors contribute: M_x_max = 2 * d * dT = 2 * (l/sqrt(2)) * dT = sqrt(2) * l * dT
        Mx_max_cross = 2.0 * d * dT

        ratio = Mx_max_cross / Mx_max_plus
        self.assertAlmostEqual(ratio, math.sqrt(2.0), places=12)

    def test_hexarotor_pseudo_inverse_orthonormality_and_minimum_norm(self):
        """Verify hexarotor right Moore-Penrose pseudo-inverse and minimum 2-norm property."""
        l = 0.25
        k = 0.020
        a = 0.5 * l
        b = (math.sqrt(3.0) / 2.0) * l

        A_hex = np.array([
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [a, -a, -l, -a, a, l],
            [b, b, 0.0, -b, -b, 0.0],
            [k, -k, k, -k, k, -k]
        ], dtype=np.float64)

        # Gram matrix: G = A_hex * A_hex^T
        G = A_hex @ A_hex.T
        G_expected = np.diag([6.0, 3.0 * (l**2), 3.0 * (l**2), 6.0 * (k**2)])
        self.assertTrue(np.allclose(G, G_expected, atol=1e-12))

        # Moore-Penrose pseudo-inverse
        A_pinv = A_hex.T @ np.linalg.inv(G)
        # Right-inverse property: A * A^+ == I_4
        self.assertTrue(np.allclose(A_hex @ A_pinv, np.eye(4), atol=1e-12))

        # Demand: Fz = -20 N, Mx = 0.5 Nm, My = -0.3 Nm, Mz = 0.05 Nm
        u_cmd = np.array([-20.0, 0.5, -0.3, 0.05])
        t_opt = A_pinv @ u_cmd
        norm_opt = np.linalg.norm(t_opt)

        # Verify minimum-norm property: any perturbed solution in the null space has larger norm
        # Null space of A_hex has dimension 6 - 4 = 2
        U, S, Vt = np.linalg.svd(A_hex)
        null_space = Vt[4:].T  # 6 x 2

        np.random.seed(99)
        for _ in range(50):
            coeffs = np.random.uniform(-2.0, 2.0, size=2)
            null_vec = null_space @ coeffs
            t_perturbed = t_opt + null_vec

            # Both produce exact same virtual wrench
            u_check = A_hex @ t_perturbed
            self.assertTrue(np.allclose(u_check, u_cmd, atol=1e-10))

            # But perturbed solution MUST have strictly greater Euclidean norm
            norm_perturbed = np.linalg.norm(t_perturbed)
            self.assertGreaterEqual(norm_perturbed, norm_opt - 1e-12)

    def test_single_motor_fault_tolerance_quad_vs_hex(self):
        """Single motor failure drops quadrotor rank to 3 (uncontrollable), but hexarotor retains rank 4."""
        # Quadrotor with motor 1 failed (column 1 zeroed)
        l = 0.25
        k = 0.02
        A_quad = np.array([
            [-1, -1, -1, -1],
            [0, -l, 0, l],
            [l, 0, -l, 0],
            [k, -k, k, -k]
        ], dtype=float)

        A_quad_fault = A_quad[:, 1:]  # Drop failed motor 1
        rank_quad = np.linalg.matrix_rank(A_quad_fault)
        self.assertEqual(rank_quad, 3)  # UNCONTROLLABLE: Rank 3 < 4

        # Hexarotor with any single motor failed
        a = 0.5 * l
        b = (math.sqrt(3.0) / 2.0) * l
        A_hex = np.array([
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [a, -a, -l, -a, a, l],
            [b, b, 0.0, -b, -b, 0.0],
            [k, -k, k, -k, k, -k]
        ], dtype=float)

        for failed_idx in range(6):
            active_cols = [i for i in range(6) if i != failed_idx]
            A_hex_fault = A_hex[:, active_cols]
            rank_hex = np.linalg.matrix_rank(A_hex_fault)
            self.assertEqual(rank_hex, 4, msg=f"Hexarotor lost rank when motor {failed_idx+1} failed!")


class TestMotorLagRouthHurwitzAndBifurcation(unittest.TestCase):
    """Stress-test motor lag characteristic roots: marginal stability, instability, and Hopf bifurcation."""

    def compute_roots(self, tau_m: float, kp: float, kd: float) -> np.ndarray:
        """Characteristic polynomial: P(s) = tau_m * s^3 + s^2 + kd * s + kp = 0."""
        poly_coeffs = [tau_m, 1.0, kd, kp]
        return np.roots(poly_coeffs)

    def test_marginal_stability_exact_imaginary_roots(self):
        """When kd == tau_m * kp, closed-loop poles lie PRECISELY on the imaginary axis: s = +- j * sqrt(kp)."""
        test_cases = [
            (0.020, 9.0),
            (0.030, 25.0),
            (0.050, 100.0),
            (0.010, 625.0),
        ]

        for tau_m, kp in test_cases:
            kd_critical = tau_m * kp
            roots = self.compute_roots(tau_m, kp, kd_critical)

            # Sort roots by imaginary part
            # Analytical factorization: (s^2 + kp)(tau_m * s + 1) = 0
            # Root 1: s = -1 / tau_m (strictly real negative)
            # Roots 2, 3: s = +- j * sqrt(kp) (strictly imaginary, Re = 0)
            real_root_expected = -1.0 / tau_m
            omega_expected = math.sqrt(kp)

            found_real_pole = False
            found_imag_poles = False

            for r in roots:
                if abs(r.imag) < 1e-10:
                    self.assertAlmostEqual(r.real, real_root_expected, places=10)
                    found_real_pole = True
                else:
                    self.assertAlmostEqual(r.real, 0.0, places=10,
                                           msg=f"Real part of marginal pole is not zero: {r.real}")
                    self.assertAlmostEqual(abs(r.imag), omega_expected, places=10)
                    found_imag_poles = True

            self.assertTrue(found_real_pole)
            self.assertTrue(found_imag_poles)

    def test_unstable_regime_right_half_plane_crossing(self):
        """When kd < tau_m * kp, the complex conjugate pair enters the Right Half-Plane (Re(s) > 0)."""
        tau_m = 0.025
        kp = 100.0
        kd_crit = tau_m * kp  # 2.50

        # Sweep under-damped derivative gains: kd / kd_crit < 1.0
        ratios = [0.1, 0.5, 0.8, 0.95, 0.99]

        for ratio in ratios:
            kd = ratio * kd_crit
            roots = self.compute_roots(tau_m, kp, kd)
            max_real = np.max(np.real(roots))

            self.assertGreater(max_real, 0.0,
                               msg=f"Root did not enter RHP for kd={kd} < {kd_crit} (max_real={max_real})")

    def test_stable_regime_left_half_plane(self):
        """When kd > tau_m * kp, all closed-loop roots lie strictly in the Left Half-Plane (Re(s) < 0)."""
        tau_m = 0.025
        kp = 100.0
        kd_crit = tau_m * kp

        # Sweep adequately damped derivative gains: kd / kd_crit > 1.0
        ratios = [1.01, 1.1, 1.5, 2.0, 5.0]

        for ratio in ratios:
            kd = ratio * kd_crit
            roots = self.compute_roots(tau_m, kp, kd)
            max_real = np.max(np.real(roots))

            self.assertLess(max_real, 0.0,
                            msg=f"Root not in LHP for kd={kd} > {kd_crit} (max_real={max_real})")

    def test_hopf_bifurcation_continuity(self):
        """Verify that max(Re(s)) passes smoothly through zero at kd = tau_m * kp."""
        tau_m = 0.030
        kp = 64.0
        kd_crit = tau_m * kp  # 1.92

        alphas = np.linspace(0.8, 1.2, 41)
        real_parts = []

        for alpha in alphas:
            kd = alpha * kd_crit
            roots = self.compute_roots(tau_m, kp, kd)
            # Find the complex conjugate pair
            complex_roots = [r for r in roots if abs(r.imag) > 1e-4]
            self.assertEqual(len(complex_roots), 2)
            real_parts.append(complex_roots[0].real)

        real_parts = np.array(real_parts)

        # Monotonically decreasing real part as damping ratio increases
        self.assertTrue(np.all(np.diff(real_parts) < 0))

        # Exact zero crossing at index 20 (alpha = 1.0)
        self.assertAlmostEqual(real_parts[20], 0.0, places=12)


class TestLongitudinalStateSpaceControllability(unittest.TestCase):
    """Stress-test 4-state longitudinal hover controllability, observability, and LQR CARE."""

    def test_symbolic_controllability_determinant(self):
        """Symbolic proof: det(C_long) == g^2 / Jy^4 != 0."""
        g, Jy = sp.symbols('g Jy', positive=True)

        A = sp.Matrix([
            [0, 1, 0, 0],
            [0, 0, -g, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0]
        ])
        B = sp.Matrix([0, 0, 0, 1/Jy])

        C_mat = sp.Matrix.hstack(B, A * B, A**2 * B, A**3 * B)
        det_C = sp.factor(C_mat.det())

        expected_det = (g ** 2) / (Jy ** 4)
        self.assertEqual(det_C, expected_det)

    def test_controllability_rank_across_diverse_parameters(self):
        """Numerical rank == 4 across small micro-drones to heavy cargo UAVs."""
        cases = [
            (9.81, 1e-4),   # Tiny whoop
            (9.81, 0.025),  # Standard 450 quadrotor
            (9.81, 0.50),   # Heavy payload drone
            (1.62, 0.025),  # Lunar gravity (g = 1.62 m/s^2)
            (24.79, 0.025), # Jupiter gravity
        ]

        for g_val, Jy_val in cases:
            A = np.array([
                [0, 1, 0, 0],
                [0, 0, -g_val, 0],
                [0, 0, 0, 1],
                [0, 0, 0, 0]
            ], dtype=float)
            B = np.array([[0], [0], [0], [1.0 / Jy_val]], dtype=float)

            C_mat = np.hstack([B, A @ B, (A @ A) @ B, (A @ A @ A) @ B])
            rank = np.linalg.matrix_rank(C_mat)
            det_val = np.linalg.det(C_mat)

            self.assertEqual(rank, 4)
            expected_det = (g_val ** 2) / (Jy_val ** 4)
            self.assertAlmostEqual(det_val, expected_det, delta=abs(expected_det) * 1e-10)

    def test_observability_position_vs_tilt_only(self):
        """Full state is observable from position x alone, but NOT observable from pitch angle theta alone."""
        g = 9.81
        A = np.array([
            [0, 1, 0, 0],
            [0, 0, -g, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0]
        ], dtype=float)

        # Sensor 1: GNSS / Visual Position measurement y = x -> C = [1, 0, 0, 0]
        C_pos = np.array([[1, 0, 0, 0]], dtype=float)
        O_pos = np.vstack([C_pos, C_pos @ A, C_pos @ (A @ A), C_pos @ (A @ A @ A)])
        rank_pos = np.linalg.matrix_rank(O_pos)
        det_pos = np.linalg.det(O_pos)

        self.assertEqual(rank_pos, 4)
        self.assertAlmostEqual(det_pos, g ** 2, places=8)

        # Sensor 2: IMU Tilt measurement y = theta -> C = [0, 0, 1, 0]
        C_tilt = np.array([[0, 0, 1, 0]], dtype=float)
        O_tilt = np.vstack([C_tilt, C_tilt @ A, C_tilt @ (A @ A), C_tilt @ (A @ A @ A)])
        rank_tilt = np.linalg.matrix_rank(O_tilt)

        # Crucial Insight: Gyro/Accelerometer tilt alone CANNOT reconstruct position or velocity!
        self.assertEqual(rank_tilt, 2)  # UNPOS-OBSERVABLE: Rank 2 < 4

    def test_lqr_continuous_algebraic_riccati_equation(self):
        """Solve CARE for longitudinal channel; verify symmetric positive definite P and Hurwitz closed loop."""
        g = 9.81
        Jy = 0.035

        A = np.array([
            [0, 1, 0, 0],
            [0, 0, -g, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0]
        ], dtype=float)
        B = np.array([[0], [0], [0], [1.0 / Jy]], dtype=float)

        # Bryson weights: x_max = 0.5m, u_max = 1.0 m/s, theta_max = 15 deg (0.26 rad), q_max = 1.0 rad/s
        Q = np.diag([1.0 / (0.5**2), 1.0 / (1.0**2), 1.0 / (0.26**2), 1.0 / (1.0**2)])
        R = np.array([[1.0 / (0.5**2)]])  # My_max = 0.5 Nm

        P = linalg.solve_continuous_are(A, B, Q, R)

        # 1. P must be symmetric positive-definite
        self.assertTrue(np.allclose(P, P.T, atol=1e-10))
        eigenvals_P = np.linalg.eigvals(P)
        self.assertTrue(np.all(eigenvals_P > 0))

        # 2. Optimal gain K = R^-1 * B^T * P
        K = np.linalg.inv(R) @ B.T @ P

        # 3. Closed-loop system A_cl = A - B * K must be strictly Hurwitz (all Re(lambda) < 0)
        A_cl = A - B @ K
        cl_poles = np.linalg.eigvals(A_cl)
        self.assertTrue(np.all(np.real(cl_poles) < -1e-4),
                        msg=f"LQR closed-loop poles are not strictly Hurwitz: {cl_poles}")


def run_all_tests():
    """Execute the full test runner and return structured results."""
    print("=" * 80)
    print("EEEE4138 Aerial Robotics — Adversarial Mathematical & Physics Stress Harness")
    print("Challenger 1 Verification Engine")
    print("=" * 80)

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    suite.addTests(loader.loadTestsFromTestCase(TestActuatorDiscMomentumLimits))
    suite.addTests(loader.loadTestsFromTestCase(TestAttitudeKinematicsAndQuaternions))
    suite.addTests(loader.loadTestsFromTestCase(TestTransportTheoremAndCoriolis))
    suite.addTests(loader.loadTestsFromTestCase(TestMixerMatricesAndAllocation))
    suite.addTests(loader.loadTestsFromTestCase(TestMotorLagRouthHurwitzAndBifurcation))
    suite.addTests(loader.loadTestsFromTestCase(TestLongitudinalStateSpaceControllability))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 80)
    if result.wasSuccessful():
        print(f"ADVERSARIAL VERIFICATION PASSED: All {result.testsRun} stress tests succeeded (100%).")
        return 0
    else:
        print(f"ADVERSARIAL VERIFICATION FAILED: {len(result.failures)} failures, {len(result.errors)} errors.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
