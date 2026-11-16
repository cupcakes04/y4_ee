# University of Nottingham
## Faculty of Science and Engineering
### Department of Electrical and Electronic Engineering
### EEEE4077 Mechatronics Project

---

# Statement of Originality

* I have read and understood the University of Nottingham Academic Misconduct Policy.
* I am aware that failure to act in accordance with the Regulations Governing Academic Integrity may lead to the imposition of penalties which, for the most serious cases, may include termination of programme.
* I consent to the University copying and distributing any or all of my work in any form and using third parties to verify whether my work contains plagiarised material, and for quality assurance purposes.

> **Note**: You must change the statements in the boxes to reflect your individual submission.

---

### 1. Acknowledgment of Sources

You must acknowledge all sources of information (e.g. ideas, algorithms, data) using citations to auditable, authoritative sources. You must also put quotation marks around any sections of text that you have copied without paraphrasing and cite the original source. If any figures or tables have been taken or modified from another source, you must explain this in the caption, and cite the original source.

> **Student Declaration:**  
> I have acknowledged all sources, and identified any content taken from elsewhere. All non-original ideas, algorithms, mathematical formulations, and published benchmarks are formally cited to auditable, authoritative academic literature using IEEE-style numerical citations ([1]–[13]). No text has been copied verbatim without quotation and attribution. All system architecture and workflow diagrams (Figures 1 and 2) and schedule tables were authored directly by me for this project.

---

### 2. Resources Produced by Someone Else

If you have used any code (e.g., open-source code), reference designs, or similar resources that have been produced by anyone else, you must list them in the box below. In the report, you must explain what was used and how it relates to the work you have done.

> **Student Declaration:**  
> I have used the following resources that have been produced by someone else:
>
> 1. **Robot Operating System 2 (ROS 2 Jazzy Jalisco / Humble)**: Open-source robotics middleware providing message passing, lifecycle nodes, and coordinate transform (`tf2`) management.
> 2. **Nav2 Navigation Stack (`nav2_mppi_controller`, `nav2_costmap_2d`, `nav2_bringup`)**: Standard open-source mobile robot navigation architecture. The native MPPI trajectory rollout infrastructure and 2D costmap servers are leveraged directly.
> 3. **Gazebo Harmonic**: Open-source physics simulator utilized for world loading, differential-drive mobile robot dynamics, laser/camera sensor simulation, and dynamic pedestrian actor execution.
> 4. **Ultralytics YOLOv8 (`yolov8n` pre-trained weights)**: Open-source neural network weights and architecture used strictly as an off-the-shelf 2D visual detector for bounding box and semantic class generation.
> 5. **ByteTrack / BoxMOT**: Open-source 2D multi-object tracking implementation used for frame-to-frame bounding box data association in image pixel space.
> 6. **Open-Source Scientific & Math Libraries**: OpenCV (image handling and camera projection geometry), Eigen3 (C++ linear algebra matrix calculations), NumPy, and SciPy (data evaluation and statistical plotting).
>
> I have acknowledged all input (hardware, software, intellectual) taken from elsewhere and explained how this was used. All custom sensor fusion logic (camera–LiDAR frustum gating), linear Kalman filter velocity estimators, custom C++ dynamic obstacle MPPI critic plugin (`DynamicObstaclesCriticPlugin`), and automated evaluation test harnesses are developed by me.

---

### 3. Generative AI Declaration

If you have used generative AI tools in the preparation of your assessed work, or the underlying code/designs/underpinning work, its use must be declared in a signed statement in the box below. You must declare the tools employed and the method and extent of use. You can do this using the table below:

> **Generative AI tools have been used in the preparation of this work as follows:**
>
> | Tool | Application Scope | Nature of Assistance & Verification |
> | :--- | :--- | :--- |
> | **Google Gemini** | Drafting boilerplate configuration and editorial structuring | Used to generate standard ROS 2 node boilerplate, `CMakeLists.txt` templates, and `package.xml` dependency structures. Used iteratively to improve grammatical conciseness, structural cohesion, and technical phrasing across draft report sections. All generated templates and text were critically reviewed, manually edited, debugged, and integrated by the author. System architecture and design choices remain solely the author's work. |
> | **Microsoft Copilot / Anthropic Claude** | Syntax reference and proofreading | Used for target syntax lookups (e.g., C++17 idiom verification, ROS 2 parameter declaration schemas) and line-level proofreading of draft prose. |
>
> **Student Declaration:**  
> *"I confirm that all sources and forms of assistance have been fully acknowledged. Generative AI tools were employed strictly in an assistive capacity for syntax reference, boilerplate generation, and editorial refinement. All system engineering, conceptual design, mathematical derivations, analysis, and final conclusions represent my own original intellectual work, and I accept full responsibility for the technical accuracy and integrity of all submitted content."*

---

### 4. Independent Work & External Assistance

You can consult with teaching staff/demonstrators, but you should not show anyone else your work (this includes uploading your work to publicly accessible repositories e.g. GitHub, unless expressly permitted by your supervisor). Nor should you help other students with their work. You must get permission in writing before you seek outside assistance, e.g. a proofreading service, and declare it here.

> **Student Declaration:**  
> I did all the work myself, and have not helped anyone else. No external proofreading services, essay mills, or paid third-party contractors were engaged. The code repository is maintained privately and has not been distributed or made publicly accessible without explicit supervisory permission.

---

### 5. Research Data Integrity & Reproducibility

You must not have fabricated, modified or distorted any data, evidence, references, experimental results, or other material used or presented in the report. You must clearly describe your experiments and how the results were obtained, and include all data, source code and/or designs (submitted as a separate file) so that your results could be reproduced.

> **Student Declaration:**  
> The material in the report is genuine, and I have included all my data/code/designs. All simulated sensor parameters, mathematical formulations, and evaluation metrics are truthful and reproducible within the containerized simulation environment.

---

### 6. Ethical Approval

If your work involved research studies (including surveys) on human participants, their cells or data, or on animals, you must have been granted ethical approval before the work was carried out, and any experiments must have followed these requirements. You must give details of this in the report, and list the ethical approval reference number(s) in the box below.

> **Student Declaration:**  
> **Not applicable.** This project is conducted entirely within computer simulation (Gazebo Harmonic and ROS 2) utilizing synthetic actor models. It does not involve human subjects, live animal testing, clinical trials, or personal identifiable data.

---

### Supervisory Discussion & Final Sign-Off

My responses to these questions are full and complete, and I have discussed them with my supervisor.

| Field | Detail |
| :--- | :--- |
| **Student Name** | Nicholas Khor Han Le |
| **Student ID** | 20617556 |
| **Degree Programme** | MEng (Hons) Electrical and Electronic Engineering / Mechatronics |
| **Project Code & Title** | SD-MEng-26-01: Vision-Augmented Mobile Robot Navigation in Dynamic Environments |
| **Supervisor** | Dr. Shalini Darmaraju |
| **Moderator** | Ir Dr. Daniel Pu |
| **Date** | 2 November 2026 |
| **Student Signature** | *Nicholas Khor Han Le* |

