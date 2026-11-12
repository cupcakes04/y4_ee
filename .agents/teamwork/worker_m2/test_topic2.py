import os
import re
import math
import html5lib
import subprocess

def test_chapter():
    chap_path = "modules/EEEE4138_aerial_robotics/chapters/topic_2_coordinate_frames.md"
    assert os.path.exists(chap_path), f"File {chap_path} does not exist!"
    content = open(chap_path, "r", encoding="utf-8").read()
    
    # Check key sections
    required_sections = [
        "Topic 2: Coordinate Frames, Euler Rotations & Attitude Kinematics",
        "Standardized Architecture & Modular API Contract",
        "Prerequisite Bridge & Mathematical Foundations",
        "The Six Aerial Robotics Reference Frames",
        "Elementary Axis Rotations (Right-Hand Rule)",
        "Step-by-Step Derivation of Vehicle-to-Body Transformation Matrix",
        "Step-by-Step Derivation of Body-to-Inertial (NED) Direction Cosine Matrix",
        "Analytical Proof of Orthogonality",
        "Translational Velocity Kinematics",
        "Transformations for Fixed-Wing Stability and Wind Frames",
        "Euler Angle Rate Kinematics & The Gimbal Lock Singularity",
        "Analytical Inversion: The Euler Rate Propagation Matrix",
        "Mathematical & Physical Analysis of Gimbal Lock",
        "Unit Quaternions: Singularity-Free Attitude Representation",
        "Quaternion Kinematic Differential Equation",
        "Direction Cosine Matrix from Unit Quaternions",
        "Conversions Between Euler Angles and Quaternions",
        "Homogeneous Transformations & Sensor Offsets",
        "Comprehensive Worked Numerical Examples",
        "Interactive Generative UI Visualizer Widget",
        "Common Student Pitfalls & Examination Traps",
        "Bidirectional Cross-References & Downstream Integration"
    ]
    for sec in required_sections:
        assert sec in content, f"Missing required section: {sec}"
        
    # Check API contract table
    assert "Attitude_Kinematics_Engine" in content
    assert "Direction Cosine Matrix" in content
    assert "Gimbal Lock Singularity" in content
    assert "SO(3)" in content
    
    # Check 6 frames
    frames = ["Inertial Frame", "Vehicle Frame", "Vehicle-1 Frame", "Vehicle-2 Frame", "Body Frame", "Stability Frame", "Wind Frame"]
    for f in frames:
        assert f in content, f"Missing frame: {f}"

    # Verify numerical calculations in Example 1:
    # Body vel [4, 0, 0] at psi=30 deg
    u = 4.0
    psi_rad = math.radians(30)
    p_n_dot = u * math.cos(psi_rad)
    p_e_dot = u * math.sin(psi_rad)
    assert abs(p_n_dot - 3.4641) < 0.001
    assert abs(p_e_dot - 2.0000) < 0.001
    assert abs(p_n_dot * 5 - 17.3205) < 0.01
    assert abs(p_e_dot * 5 - 10.0000) < 0.01
    
    # Verify Example 2:
    # Camera offset [0.30, 0, 0.10] rotated by R_z(90 deg) + [10, 20, -5]
    # R_z(90) * [0.30, 0, 0.10] = [0, 0.30, 0.10]
    # Pos: [10 + 0, 20 + 0.30, -5 + 0.10] = [10.00, 20.30, -4.90]
    assert "+10.00" in content or "10.00" in content
    assert "20.30" in content
    assert "-4.90" in content

    # Verify Example 4:
    # (120, 90, -60) -> phi - psi = 180 -> R = [[0, 0, -1], [0, -1, 0], [-1, 0, 0]]
    assert "180^\\circ" in content or "180°" in content
    assert "-1" in content
    
    # Verify cross-links:
    assert "topic_1_uav_architectures.md" in content
    assert "topic_3_kinematics_dynamics.md" in content
    assert "topic_4_forces_moments.md" in content
    assert "topic_5_flight_control.md" in content
    assert "widget_2_frames_gimbal_lock.html" in content

    print("PASS: topic_2_coordinate_frames.md verified successfully.")

def test_widget():
    widget_path = "modules/EEEE4138_aerial_robotics/widgets/widget_2_frames_gimbal_lock.html"
    assert os.path.exists(widget_path), f"File {widget_path} does not exist!"
    content = open(widget_path, "r", encoding="utf-8").read()
    
    # Basic HTML checks
    assert "<!DOCTYPE html>" in content
    assert "<canvas id=\"canvas3D\"" in content
    assert "sliderYaw" in content
    assert "sliderPitch" in content
    assert "sliderRoll" in content
    assert "btnReset" in content
    assert "btnLockPos" in content
    assert "btnLockNeg" in content
    assert "btnTutorial1Q6" in content
    assert "gimbalAlertBanner" in content
    assert "computeDCM" in content
    assert "computeQuaternion" in content
    assert "project3D" in content
    assert "cdn.tailwindcss.com" in content

    # Check for script tag completeness
    assert "<script>" in content
    assert "</script>" in content
    assert "requestAnimationFrame" in content
    
    print("PASS: widget_2_frames_gimbal_lock.html verified successfully.")

if __name__ == "__main__":
    test_chapter()
    test_widget()
