#!/usr/bin/env python3
"""
Generate monochrome LaTeX/TikZ-style block diagrams for Figure 1 (System Architecture)
and Figure 2 (Methodology Flow) using serif typography, crisp black borders, and zero pastel fills.
"""
import os
os.environ['MPLCONFIGDIR'] = '/tmp/mpl_cache'

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Liberation Serif', 'DejaVu Serif', 'Times New Roman'],
    'mathtext.fontset': 'cm',
    'axes.edgecolor': 'black',
    'axes.linewidth': 1.0,
})

ASSETS_DIR = '/home/nicholas/projects/y4_ee/modules/EEEE4077_mechatronics_proj/chapters/deliverables/assets'


def draw_box(ax, x, y, w, h, title, subtitle=None, lw=1.1, ls='-', fill='#FFFFFF', title_size=10.5, sub_size=8.8):
    """Draw a sharp-cornered or slightly rounded TikZ-style rectangular node centered at (x, y)."""
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.06",
        facecolor=fill, edgecolor='black', linewidth=lw, linestyle=ls, zorder=3
    )
    ax.add_patch(box)
    if subtitle:
        ax.text(x, y + h * 0.17, title, ha='center', va='center',
                fontsize=title_size, fontweight='bold', color='black', zorder=4)
        ax.text(x, y - h * 0.16, subtitle, ha='center', va='center',
                fontsize=sub_size, color='black', linespacing=1.25, zorder=4)
    else:
        ax.text(x, y, title, ha='center', va='center',
                fontsize=title_size, fontweight='bold', color='black', zorder=4)


def draw_group(ax, x, y, w, h, label):
    """Draw a dashed TikZ-style group container with a top-left label pill."""
    rect = Rectangle(
        (x - w / 2, y - h / 2), w, h,
        facecolor='none', edgecolor='black', linewidth=0.9, linestyle='--', zorder=1
    )
    ax.add_patch(rect)
    ax.text(
        x - w / 2 + 0.25, y + h / 2, f" {label} ",
        ha='left', va='center', fontsize=9.2, fontweight='bold', style='italic',
        color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.18', lw=0.7),
        zorder=5
    )


def draw_arrow(ax, x1, y1, x2, y2, label=None, ls='-', lw=1.0, label_pos=0.5, label_offset=(0, 0)):
    """Draw a clean straight arrow with an optional inline white-backed text label."""
    ax.annotate(
        '', xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle='-|>,head_length=0.55,head_width=0.3', color='black', lw=lw, ls=ls, shrinkA=0, shrinkB=0),
        zorder=4
    )
    if label:
        lx = x1 + (x2 - x1) * label_pos + label_offset[0]
        ly = y1 + (y2 - y1) * label_pos + label_offset[1]
        ax.text(
            lx, ly, label, ha='center', va='center', fontsize=8.4, color='black',
            bbox=dict(facecolor='white', edgecolor='none', pad=1.2), zorder=6
        )


def generate_fig1():
    fig, ax = plt.subplots(figsize=(8.0, 8.6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10.8)
    ax.axis('off')

    # Group 1: Sensors
    draw_group(ax, 4.7, 9.55, 8.8, 1.75, "1. Simulated Sensors (Gazebo World)")
    draw_box(ax, 2.55, 9.48, 3.9, 1.15,
             "Monocular RGB Camera",
             "Front camera stream (80° FOV, 30 Hz)\nCaptures visual appearance of obstacles")
    draw_box(ax, 6.85, 9.48, 3.9, 1.15,
             "Planar 2D Safety LiDAR",
             "360° laser scan (/scan at 20-40 Hz)\nMeasures floor-plane obstacle distances")

    # Group 2: Multi-Modal Tracker (O1)
    draw_group(ax, 4.7, 6.15, 8.8, 3.45, "2. Obstacle Detection and Tracking (Objective O1)")
    draw_box(ax, 2.55, 7.02, 3.9, 1.15,
             "2D Object Detector (YOLOv8)",
             "Detects moving obstacle classes\nand outputs 2D bounding boxes")
    draw_box(ax, 2.55, 5.22, 3.9, 1.15,
             "2D Multi-Object Tracker (ByteTrack)",
             "Matches bounding boxes across frames\nto keep consistent obstacle IDs")
    draw_box(ax, 6.85, 7.02, 3.9, 1.15,
             "Camera-LiDAR Frustum Gate",
             "Projects laser rays into 2D boxes\nand takes median obstacle depth")
    draw_box(ax, 6.85, 5.22, 3.9, 1.15,
             "Linear Kalman Filter",
             "Constant-velocity state filter\nestimating position and velocity (x, y, vx, vy)")

    # Group 3: Local Planning (O2)
    draw_group(ax, 4.7, 3.1, 8.8, 1.75, "3. Motion-Aware Local Planning (Objective O2)")
    draw_box(ax, 2.55, 3.03, 3.9, 1.15,
             "Dynamic Obstacle Critic Plugin",
             "Projects obstacle motion over 2.0 s\nand scores candidate trajectories")
    draw_box(ax, 6.85, 3.03, 3.9, 1.15,
             "Nav2 MPPI Local Controller",
             "Combines dynamic critic cost and static\ncostmap to output safe velocity commands")

    # Group 4: Execution & Evaluation (O3)
    draw_group(ax, 4.7, 0.95, 8.8, 1.65, "4. Robot Control and Evaluation (Objective O3)")
    draw_box(ax, 2.55, 0.88, 3.9, 1.05,
             "Simulated Differential-Drive Base",
             "Executes /cmd_vel in indoor world")
    draw_box(ax, 6.85, 0.88, 3.9, 1.05,
             "Automated Evaluation Logger",
             "Records freezes, collisions, travel time,\nand velocity tracking error")

    # Arrows
    draw_arrow(ax, 2.55, 8.90, 2.55, 7.60, label="RGB Frames")
    draw_arrow(ax, 6.85, 8.90, 6.85, 7.60, label="2D Laser Scan")
    draw_arrow(ax, 2.55, 6.44, 2.55, 5.80, label="2D Boxes")
    draw_arrow(ax, 4.50, 5.22, 4.90, 7.02, label="Tracked Boxes", label_pos=0.52)
    draw_arrow(ax, 6.85, 6.44, 6.85, 5.80, label="Median Depth")
    draw_arrow(ax, 6.85, 4.64, 2.95, 3.61, label="Tracked Positions & Velocities", label_pos=0.36, label_offset=(0.2, 0.03))
    draw_arrow(ax, 4.50, 3.03, 4.90, 3.03, label="Cost", label_offset=(0, 0.22))
    draw_arrow(ax, 6.85, 2.45, 2.95, 1.41, label="Velocity Commands (/cmd_vel)", label_pos=0.36, label_offset=(0.2, 0.03))
    draw_arrow(ax, 4.50, 0.88, 4.90, 0.88, label="States", label_offset=(0, 0.20))

    # Right-side bypass line from 2D LiDAR to Nav2 MPPI Static Costmap
    bx = 9.52
    ax.plot([8.80, bx, bx, 8.0], [9.48, 9.48, 4.15, 4.15], color='black', lw=1.0, zorder=3)
    draw_arrow(ax, 8.0, 4.15, 8.0, 3.61)
    ax.text(bx, 6.6, "Static Walls\n(2D Costmap)", ha='center', va='center', rotation=90,
            fontsize=8.3, color='black', bbox=dict(facecolor='white', edgecolor='black', lw=0.6, pad=1.8), zorder=6)

    plt.tight_layout(pad=0.2)
    out_path = os.path.join(ASSETS_DIR, 'fig1_latex_arch.png')
    fig.savefig(out_path, dpi=300, facecolor='white')
    plt.close(fig)
    print("Saved:", out_path)


def generate_fig2():
    fig, ax = plt.subplots(figsize=(8.0, 7.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 9.6)
    ax.axis('off')

    # Legend bar at top
    ax.text(
        5.0, 9.35,
        "Solid Line: Core Critical Path (M0 -> M1 -> M2 -> M3 -> M5)    |    Dashed Line: Parallel Harness (M4)    |    Dotted Line: Fallback (F1)",
        ha='center', va='center', fontsize=8.3, color='black',
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.35', lw=0.8)
    )

    # M0
    draw_box(ax, 5.0, 8.35, 5.6, 1.05,
             "M0: Environment and Docker Setup",
             "Configure Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic, and Docker container")

    # M1
    draw_box(ax, 5.0, 6.65, 5.6, 1.05,
             "M1: Simulation World and Baseline (C0)",
             "Build indoor corridor worlds, moving obstacle actors, and log 2D LiDAR baseline")

    # M2 (left) and M4 (right)
    draw_box(ax, 2.65, 4.75, 4.3, 1.20,
             "M2: Vision-LiDAR Tracker (O1)",
             "Adapt YOLOv8, ByteTrack, frustum depth\ngating, and linear Kalman velocity filter")
    draw_box(ax, 7.35, 4.75, 4.3, 1.20,
             "M4: Automated Testing Harness (O3)",
             "Parallel development of scenario runner,\nGazebo reset script, and metric logger",
             ls='--')

    # M3 (left) and F1 (right)
    draw_box(ax, 2.65, 2.75, 4.3, 1.20,
             "M3: Predictive MPPI Critic (O2)",
             "Develop C++ dynamic obstacle critic plugin\ninside Nav2 MPPI controller")
    draw_box(ax, 7.35, 2.75, 4.3, 1.20,
             "F1: Costmap Fallback Layer",
             "Inject velocity-stretched safety zones into\n2D costmap if C++ critic plugin is blocked",
             ls=':')

    # M5 (bottom)
    draw_box(ax, 5.0, 0.85, 6.8, 1.15,
             "M5: Comparative Ablation and Statistical Analysis (O3)",
             "Compare C0 (LiDAR-only), C1 (Vision without prediction), and C2 (Full predictive MPPI)\nacross varying obstacle speeds, crossing angles, and crowd densities")

    # Arrows
    draw_arrow(ax, 5.0, 7.82, 5.0, 7.18, lw=1.2)
    draw_arrow(ax, 3.8, 6.12, 2.65, 5.35, label="Baseline Ready", lw=1.2)
    draw_arrow(ax, 6.2, 6.12, 7.35, 5.35, label="Parallel Task", ls='--', lw=1.0)

    draw_arrow(ax, 2.65, 4.15, 2.65, 3.35, label="Tracked Velocities", lw=1.2)
    draw_arrow(ax, 4.0, 4.15, 6.2, 3.35, label="If Critic Blocked", ls=':', lw=1.1)

    draw_arrow(ax, 2.65, 2.15, 3.8, 1.43, label="Predictive Controller (C2)", lw=1.2)
    draw_arrow(ax, 6.5, 2.15, 5.6, 1.43, label="Fallback Path", ls=':', lw=1.1)

    # Outer right dashed line from M4 to M5
    rx = 9.72
    ax.plot([9.50, rx, rx], [4.75, 4.75, 0.85], color='black', lw=1.0, ls='--', zorder=3)
    draw_arrow(ax, rx, 0.85, 8.40, 0.85, ls='--', lw=1.0)
    ax.text(rx, 2.75, "Automated Test Suite", ha='center', va='center', rotation=90,
            fontsize=8.3, color='black', bbox=dict(facecolor='white', edgecolor='black', lw=0.6, pad=1.8), zorder=6)

    plt.tight_layout(pad=0.2)
    out_path = os.path.join(ASSETS_DIR, 'fig2_latex_flow.png')
    fig.savefig(out_path, dpi=300, facecolor='white')
    plt.close(fig)
    print("Saved:", out_path)


if __name__ == '__main__':
    generate_fig1()
    generate_fig2()
