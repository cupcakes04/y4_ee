const window = { addEventListener: () => {} }; const document = { getElementById: () => ({ addEventListener: () => {}, getContext: () => ({ getBoundingClientRect: () => ({ width: 800, height: 600 }), clearRect: () => {}, save: () => {}, restore: () => {}, beginPath: () => {}, moveTo: () => {}, lineTo: () => {}, stroke: () => {}, fillText: () => {}, setLineDash: () => {} }), getBoundingClientRect: () => ({ width: 800, height: 600 }), classList: { add: () => {}, remove: () => {} }, style: {} }) }; const requestAnimationFrame = () => {};

    // --- STATE VARIABLES ---
    const state = {
      // Euler Angles (degrees)
      yaw: 0,
      pitch: 0,
      roll: 0,
      // Camera Orbit Controls
      camera: {
        azimuth: 45,     // degrees
        elevation: 25,   // degrees
        distance: 7.5,   // distance units
        isDragging: false,
        lastMouseX: 0,
        lastMouseY: 0,
        autoOrbit: false
      },
      // Velocity Inputs (m/s)
      vel: { u: 4.0, v: 0.0, w: 0.0 },
      // Visibility Toggles
      showGimbals: true,
      showAirframe: true,
      showBodyAxes: true,
      showInertialAxes: true,
      showIntermediate: false
    };

    // --- DOM REFERENCES ---
    const canvas = document.getElementById('canvas3D');
    const ctx = canvas.getContext('2d');

    const sliderYaw = document.getElementById('sliderYaw');
    const sliderPitch = document.getElementById('sliderPitch');
    const sliderRoll = document.getElementById('sliderRoll');
    const numYaw = document.getElementById('numYaw');
    const numPitch = document.getElementById('numPitch');
    const numRoll = document.getElementById('numRoll');

    const btnReset = document.getElementById('btnReset');
    const btnLockPos = document.getElementById('btnLockPos');
    const btnLockNeg = document.getElementById('btnLockNeg');
    const btnTutorial1Q6 = document.getElementById('btnTutorial1Q6');
    const btnBankedTurn = document.getElementById('btnBankedTurn');
    const btnFastForward = document.getElementById('btnFastForward');
    const btnResetCam = document.getElementById('btnResetCam');

    const chkGimbals = document.getElementById('chkGimbals');
    const chkAirframe = document.getElementById('chkAirframe');
    const chkBodyAxes = document.getElementById('chkBodyAxes');
    const chkInertialAxes = document.getElementById('chkInertialAxes');
    const chkIntermediate = document.getElementById('chkIntermediate');
    const chkAutoOrbit = document.getElementById('chkAutoOrbit');

    const inputU = document.getElementById('inputU');
    const inputV = document.getElementById('inputV');
    const inputW = document.getElementById('inputW');

    const resPn = document.getElementById('resPn');
    const resPe = document.getElementById('resPe');
    const resPd = document.getElementById('resPd');

    const gimbalAlertBanner = document.getElementById('gimbalAlertBanner');
    const statusSingularity = document.getElementById('statusSingularity');
    const valCosTheta = document.getElementById('valCosTheta');
    const barCondition = document.getElementById('barCondition');

    const quatQ0 = document.getElementById('quatQ0');
    const quatQ1 = document.getElementById('quatQ1');
    const quatQ2 = document.getElementById('quatQ2');
    const quatQ3 = document.getElementById('quatQ3');
    const quatNorm = document.getElementById('quatNorm');

    const recPitch = document.getElementById('recPitch');
    const recRoll = document.getElementById('recRoll');
    const recYaw = document.getElementById('recYaw');
    const recDiffRow = document.getElementById('recDiffRow');
    const recDiffVal = document.getElementById('recDiffVal');

    const camAzimuth = document.getElementById('camAzimuth');
    const camElevation = document.getElementById('camElevation');

    // Matrix DOM cells
    const mCells = [
      [document.getElementById('m00'), document.getElementById('m01'), document.getElementById('m02')],
      [document.getElementById('m10'), document.getElementById('m11'), document.getElementById('m12')],
      [document.getElementById('m20'), document.getElementById('m21'), document.getElementById('m22')]
    ];

    // --- MATHEMATICAL FUNCTIONS ---
    const DEG2RAD = Math.PI / 180;
    const RAD2DEG = 180 / Math.PI;

    // 3D Vector operations
    function vec3(x, y, z) { return { x, y, z }; }
    function vecAdd(a, b) { return { x: a.x + b.x, y: a.y + b.y, z: a.z + b.z }; }
    function vecSub(a, b) { return { x: a.x - b.x, y: a.y - b.y, z: a.z - b.z }; }
    function vecScale(v, s) { return { x: v.x * s, y: v.y * s, z: v.z * s }; }
    function vecDot(a, b) { return a.x * b.x + a.y * b.y + a.z * b.z; }
    function vecCross(a, b) {
      return {
        x: a.y * b.z - a.z * b.y,
        y: a.z * b.x - a.x * b.z,
        z: a.x * b.y - a.y * b.x
      };
    }
    function vecNorm(v) { return Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z); }

    // 3x3 Matrix Multiplication
    function mat3Multiply(A, B) {
      const C = [[0,0,0],[0,0,0],[0,0,0]];
      for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
          C[i][j] = A[i][0]*B[0][j] + A[i][1]*B[1][j] + A[i][2]*B[2][j];
        }
      }
      return C;
    }

    // Multiply 3x3 Matrix by 3D Vector
    function mat3Vec(M, v) {
      return {
        x: M[0][0]*v.x + M[0][1]*v.y + M[0][2]*v.z,
        y: M[1][0]*v.x + M[1][1]*v.y + M[1][2]*v.z,
        z: M[2][0]*v.x + M[2][1]*v.y + M[2][2]*v.z
      };
    }

    // Direction Cosine Matrix R_b^n (Body to NED) via Tait-Bryan ZYX sequence
    function computeDCM(yawDeg, pitchDeg, rollDeg) {
      const psi = yawDeg * DEG2RAD;
      const theta = pitchDeg * DEG2RAD;
      const phi = rollDeg * DEG2RAD;

      const cPsi = Math.cos(psi), sPsi = Math.sin(psi);
      const cTheta = Math.cos(theta), sTheta = Math.sin(theta);
      const cPhi = Math.cos(phi), sPhi = Math.sin(phi);

      return [
        [
          cTheta * cPsi,
          sPhi * sTheta * cPsi - cPhi * sPsi,
          cPhi * sTheta * cPsi + sPhi * sPsi
        ],
        [
          cTheta * sPsi,
          sPhi * sTheta * sPsi + cPhi * cPsi,
          cPhi * sTheta * sPsi - sPhi * cPsi
        ],
        [
          -sTheta,
          sPhi * cTheta,
          cPhi * cTheta
        ]
      ];
    }

    // Euler to Unit Quaternion
    function computeQuaternion(yawDeg, pitchDeg, rollDeg) {
      const psi = (yawDeg * DEG2RAD) / 2;
      const theta = (pitchDeg * DEG2RAD) / 2;
      const phi = (rollDeg * DEG2RAD) / 2;

      const cPsi = Math.cos(psi), sPsi = Math.sin(psi);
      const cTheta = Math.cos(theta), sTheta = Math.sin(theta);
      const cPhi = Math.cos(phi), sPhi = Math.sin(phi);

      const q0 = cPhi * cTheta * cPsi + sPhi * sTheta * sPsi;
      const q1 = sPhi * cTheta * cPsi - cPhi * sTheta * sPsi;
      const q2 = cPhi * sTheta * cPsi + sPhi * cTheta * sPsi;
      const q3 = cPhi * cTheta * sPsi - sPhi * sTheta * cPsi;

      return { q0, q1, q2, q3 };
    }

    // --- 3D PERSPECTIVE RENDERING PIPELINE ---
    // World coordinates convention:
    // +X: North (Forward)
    // +Y: East (Right)
    // +Z: Down (Earth)
    function project3D(point, width, height) {
      // Camera spherical coordinates to Cartesian position
      const az = state.camera.azimuth * DEG2RAD;
      const el = state.camera.elevation * DEG2RAD;
      const dist = state.camera.distance;

      // Camera position in world coordinates (looking at origin)
      const camX = dist * Math.cos(el) * Math.cos(az);
      const camY = dist * Math.cos(el) * Math.sin(az);
      const camZ = -dist * Math.sin(el); // camera elevation is upwards, which is -Z in NED

      // Camera basis vectors
      // Forward view vector: from cam towards origin
      const fwd = vecScale(vecSub(vec3(0,0,0), vec3(camX, camY, camZ)), 1/dist);
      // World up vector in NED is -Z (towards sky)
      const worldUp = vec3(0, 0, -1);
      // Right vector: fwd x worldUp
      let right = vecCross(fwd, worldUp);
      const rNorm = vecNorm(right);
      if (rNorm > 1e-4) right = vecScale(right, 1/rNorm);
      else right = vec3(0, 1, 0);
      // Camera up vector: right x fwd
      const up = vecCross(right, fwd);

      // Vector from camera to point
      const rel = vecSub(point, vec3(camX, camY, camZ));

      // Project onto camera axes
      const depth = vecDot(rel, fwd);
      const xCam = vecDot(rel, right);
      const yCam = vecDot(rel, up);

      if (depth <= 0.1) return null; // Behind camera clipping

      // Perspective projection
      const fov = 650; // Focal length in pixels
      const xScreen = width / 2 + (xCam / depth) * fov;
      const yScreen = height / 2 - (yCam / depth) * fov;

      return { x: xScreen, y: yScreen, depth };
    }

    // Draw 3D Line with depth clipping
    function drawLine3D(p1, p2, color, lineWidth = 2, dash = []) {
      const s1 = project3D(p1, canvas.width, canvas.height);
      const s2 = project3D(p2, canvas.width, canvas.height);
      if (!s1 || !s2) return;

      ctx.save();
      ctx.strokeStyle = color;
      ctx.lineWidth = lineWidth;
      ctx.setLineDash(dash);
      ctx.beginPath();
      ctx.moveTo(s1.x, s1.y);
      ctx.lineTo(s2.x, s2.y);
      ctx.stroke();
      ctx.restore();
    }

    // Draw 3D Text Label
    function drawText3D(text, point, color, font = "11px monospace", align = "center") {
      const s = project3D(point, canvas.width, canvas.height);
      if (!s) return;

      ctx.save();
      ctx.font = font;
      ctx.fillStyle = color;
      ctx.textAlign = align;
      ctx.textBaseline = "middle";
      ctx.fillText(text, s.x, s.y);
      ctx.restore();
    }

    // --- MAIN RENDER LOOP ---
    function render() {
      // Auto-Orbit camera if toggled
      if (state.camera.autoOrbit && !state.camera.isDragging) {
        state.camera.azimuth = (state.camera.azimuth + 0.3) % 360;
        camAzimuth.textContent = `${Math.round(state.camera.azimuth)}°`;
      }

      // Handle Canvas DPI scaling
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      if (canvas.width !== rect.width * dpr || canvas.height !== rect.height * dpr) {
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
      }
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Direction Cosine Matrix R_b^n
      const R = computeDCM(state.yaw, state.pitch, state.roll);

      // Intermediate rotation matrices
      const psi = state.yaw * DEG2RAD;
      const theta = state.pitch * DEG2RAD;
      const R_z = [
        [Math.cos(psi), -Math.sin(psi), 0],
        [Math.sin(psi), Math.cos(psi), 0],
        [0, 0, 1]
      ];
      const R_y = [
        [Math.cos(theta), 0, Math.sin(theta)],
        [0, 1, 0],
        [-Math.sin(theta), 0, Math.cos(theta)]
      ];
      const R_zy = mat3Multiply(R_z, R_y); // Vehicle-2 orientation

      // 1. DRAW INERTIAL HORIZONTAL REFERENCE GRID (at z = +2.0 NED ground)
      const gridSize = 3.0;
      const gridStep = 1.0;
      const groundZ = 2.0;
      ctx.save();
      for (let x = -gridSize; x <= gridSize; x += gridStep) {
        drawLine3D(vec3(x, -gridSize, groundZ), vec3(x, gridSize, groundZ), "rgba(51, 65, 85, 0.25)", 1);
      }
      for (let y = -gridSize; y <= gridSize; y += gridStep) {
        drawLine3D(vec3(-gridSize, y, groundZ), vec3(gridSize, y, groundZ), "rgba(51, 65, 85, 0.25)", 1);
      }
      ctx.restore();

      // 2. DRAW FIXED INERTIAL NED AXES (Origin 0,0,0)
      if (state.showInertialAxes) {
        const axisLen = 2.2;
        // North +X (Red)
        drawLine3D(vec3(0,0,0), vec3(axisLen, 0, 0), "rgba(239, 68, 68, 0.75)", 2.5);
        drawText3D("+X_n (North)", vec3(axisLen + 0.2, 0, 0), "#f87171");
        // East +Y (Green)
        drawLine3D(vec3(0,0,0), vec3(0, axisLen, 0), "rgba(34, 197, 94, 0.75)", 2.5);
        drawText3D("+Y_n (East)", vec3(0, axisLen + 0.2, 0), "#4ade80");
        // Down +Z (Blue)
        drawLine3D(vec3(0,0,0), vec3(0, 0, axisLen), "rgba(59, 130, 246, 0.75)", 2.5);
        drawText3D("+Z_n (Down)", vec3(0, 0, axisLen + 0.2), "#60a5fa");
      }

      // 3. DRAW INTERMEDIATE FRAMES (If enabled)
      if (state.showIntermediate) {
        const intLen = 1.6;
        // Vehicle-1 axes (after yaw psi)
        const v1_x = mat3Vec(R_z, vec3(intLen, 0, 0));
        const v1_y = mat3Vec(R_z, vec3(0, intLen, 0));
        drawLine3D(vec3(0,0,0), v1_x, "rgba(56, 189, 248, 0.5)", 1.5, [4, 4]);
        drawLine3D(vec3(0,0,0), v1_y, "rgba(56, 189, 248, 0.5)", 1.5, [4, 4]);
        drawText3D("X_v1", v1_x, "#38bdf8", "10px monospace");
      }

      // 4. DRAW 3 CONCENTRIC 3D GIMBAL RINGS
      if (state.showGimbals) {
        const numSegments = 64;
        const isGimbalLock = Math.abs(state.pitch) >= 85;

        // A. Outer Yaw Ring (Cyan): Fixed in horizontal plane, rotates around Zn
        const rYaw = 2.0;
        ctx.save();
        for (let i = 0; i < numSegments; i++) {
          const a1 = (i / numSegments) * Math.PI * 2;
          const a2 = ((i + 1) / numSegments) * Math.PI * 2;
          // In horizontal plane X_v, Y_v
          const p1 = mat3Vec(R_z, vec3(rYaw * Math.cos(a1), rYaw * Math.sin(a1), 0));
          const p2 = mat3Vec(R_z, vec3(rYaw * Math.cos(a2), rYaw * Math.sin(a2), 0));
          const color = isGimbalLock ? "rgba(244, 63, 94, 0.9)" : "rgba(6, 182, 212, 0.65)";
          drawLine3D(p1, p2, color, isGimbalLock ? 2.5 : 1.5);
        }
        ctx.restore();

        // B. Middle Pitch Ring (Emerald): Pivots around Y_v1 axis
        const rPitch = 1.7;
        ctx.save();
        for (let i = 0; i < numSegments; i++) {
          const a1 = (i / numSegments) * Math.PI * 2;
          const a2 = ((i + 1) / numSegments) * Math.PI * 2;
          // Circle in X-Z plane, rotated by R_zy
          const pt1Local = vec3(rPitch * Math.cos(a1), 0, rPitch * Math.sin(a1));
          const pt2Local = vec3(rPitch * Math.cos(a2), 0, rPitch * Math.sin(a2));
          const p1 = mat3Vec(R_zy, pt1Local);
          const p2 = mat3Vec(R_zy, pt2Local);
          drawLine3D(p1, p2, "rgba(16, 185, 129, 0.65)", 1.5);
        }
        ctx.restore();

        // C. Inner Roll Ring (Amber): Pivots around X_b axis (attached to airframe)
        const rRoll = 1.4;
        ctx.save();
        for (let i = 0; i < numSegments; i++) {
          const a1 = (i / numSegments) * Math.PI * 2;
          const a2 = ((i + 1) / numSegments) * Math.PI * 2;
          // Circle in Y-Z plane, rotated by full body rotation R
          const pt1Local = vec3(0, rRoll * Math.cos(a1), rRoll * Math.sin(a1));
          const pt2Local = vec3(0, rRoll * Math.cos(a2), rRoll * Math.sin(a2));
          const p1 = mat3Vec(R, pt1Local);
          const p2 = mat3Vec(R, pt2Local);
          const color = isGimbalLock ? "rgba(244, 63, 94, 0.9)" : "rgba(245, 158, 11, 0.65)";
          drawLine3D(p1, p2, color, isGimbalLock ? 2.5 : 1.5);
        }
        ctx.restore();

        // Draw Gimbal Bearings / Pivots
        const pivotY = mat3Vec(R_z, vec3(0, rYaw, 0));
        const pivotX = mat3Vec(R_zy, vec3(rPitch, 0, 0));
        drawLine3D(pivotY, vecScale(pivotY, -1), "rgba(6, 182, 212, 0.4)", 1, [2, 2]);
        drawLine3D(pivotX, vecScale(pivotX, -1), "rgba(16, 185, 129, 0.4)", 1, [2, 2]);
      }

      // 5. DRAW QUADROTOR AIRFRAME MODEL (X-Configuration)
      if (state.showAirframe) {
        const armL = 0.95;
        const d = armL / Math.SQRT2; // 45 degree arms

        // 4 Motor Positions in Body Frame (FRD)
        // 1: Front-Left (+x, -y), 2: Front-Right (+x, +y), 3: Rear-Right (-x, +y), 4: Rear-Left (-x, -y)
        const motorsBody = [
          vec3(d, -d, 0), // Rotor 1 (CCW)
          vec3(d, d, 0),  // Rotor 2 (CW)
          vec3(-d, d, 0), // Rotor 3 (CCW)
          vec3(-d, -d, 0) // Rotor 4 (CW)
        ];

        // Transform to Inertial NED
        const motorsNED = motorsBody.map(m => mat3Vec(R, m));
        const centerNED = vec3(0, 0, 0);

        // Draw Carbon Fiber Arms
        drawLine3D(centerNED, motorsNED[0], "#94a3b8", 3);
        drawLine3D(centerNED, motorsNED[1], "#94a3b8", 3);
        drawLine3D(centerNED, motorsNED[2], "#64748b", 3);
        drawLine3D(centerNED, motorsNED[3], "#64748b", 3);

        // Center Fuselage Hub
        const hubTop = mat3Vec(R, vec3(0, 0, -0.08));
        const hubBot = mat3Vec(R, vec3(0, 0, 0.08));
        drawLine3D(hubTop, hubBot, "#38bdf8", 8);

        // Forward Nose Orientation Arrow on Fuselage
        const noseTip = mat3Vec(R, vec3(0.35, 0, 0));
        const noseLeft = mat3Vec(R, vec3(0.18, -0.09, 0));
        const noseRight = mat3Vec(R, vec3(0.18, 0.09, 0));
        drawLine3D(noseLeft, noseTip, "#ef4444", 2.5);
        drawLine3D(noseRight, noseTip, "#ef4444", 2.5);
        drawLine3D(noseLeft, noseRight, "#ef4444", 2.5);

        // Draw 4 Rotor Discs with Spin Directions
        const propRadius = 0.32;
        const discSegs = 24;
        motorsNED.forEach((hub, idx) => {
          // Draw Motor Pod
          const podTop = vecAdd(hub, mat3Vec(R, vec3(0, 0, -0.05)));
          const podBot = vecAdd(hub, mat3Vec(R, vec3(0, 0, 0.05)));
          drawLine3D(podTop, podBot, "#e2e8f0", 4);

          // Draw Rotor Disc Ring in Body X-Y plane
          const isCCW = (idx === 0 || idx === 2);
          const discColor = isCCW ? "rgba(34, 197, 94, 0.7)" : "rgba(56, 189, 248, 0.7)";

          for (let s = 0; s < discSegs; s++) {
            const t1 = (s / discSegs) * Math.PI * 2;
            const t2 = ((s + 1) / discSegs) * Math.PI * 2;
            const p1Local = vecAdd(motorsBody[idx], vec3(propRadius * Math.cos(t1), propRadius * Math.sin(t1), -0.05));
            const p2Local = vecAdd(motorsBody[idx], vec3(propRadius * Math.cos(t2), propRadius * Math.sin(t2), -0.05));
            drawLine3D(mat3Vec(R, p1Local), mat3Vec(R, p2Local), discColor, 1.5);
          }
          drawText3D(`M${idx+1} (${isCCW?'CCW':'CW'})`, vecAdd(hub, mat3Vec(R, vec3(0, 0, -0.15))), discColor, "9px monospace");
        });
      }

      // 6. DRAW MOVING BODY FRD AXES (Anchored to Drone CoM)
      if (state.showBodyAxes) {
        const bodyLen = 1.7;
        const bX = mat3Vec(R, vec3(bodyLen, 0, 0));
        const bY = mat3Vec(R, vec3(0, bodyLen, 0));
        const bZ = mat3Vec(R, vec3(0, 0, bodyLen));

        // +X_b Nose/Forward (Bright Red)
        drawLine3D(vec3(0,0,0), bX, "#f43f5e", 3.5);
        drawText3D("+X_b (Nose)", bX, "#fb7185", "bold 11px monospace");

        // +Y_b Starboard/Right (Bright Green)
        drawLine3D(vec3(0,0,0), bY, "#10b981", 3.5);
        drawText3D("+Y_b (Starboard)", bY, "#34d399", "bold 11px monospace");

        // +Z_b Belly/Down (Bright Blue)
        drawLine3D(vec3(0,0,0), bZ, "#0ea5e9", 3.5);
        drawText3D("+Z_b (Belly)", bZ, "#38bdf8", "bold 11px monospace");
      }

      // Schedule next frame
      requestAnimationFrame(render);
    }

    // --- TELEMETRY & MATH HUD UPDATES ---
    function updateHUD() {
      const R = computeDCM(state.yaw, state.pitch, state.roll);
      const Q = computeQuaternion(state.yaw, state.pitch, state.roll);

      // 1. Update DCM table
      for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 3; c++) {
          const val = R[r][c];
          mCells[r][c].textContent = (val >= 0 ? "+" : "") + val.toFixed(4);
        }
      }

      // Determinant
      const det = R[0][0]*(R[1][1]*R[2][2] - R[1][2]*R[2][1])
                - R[0][1]*(R[1][0]*R[2][2] - R[1][2]*R[2][0])
                + R[0][2]*(R[1][0]*R[2][1] - R[1][1]*R[2][0]);
      document.getElementById('valDet').textContent = (det >= 0 ? "+" : "") + det.toFixed(4);

      // 2. Update Quaternions
      quatQ0.textContent = (Q.q0 >= 0 ? "+" : "") + Q.q0.toFixed(4);
      quatQ1.textContent = (Q.q1 >= 0 ? "+" : "") + Q.q1.toFixed(4);
      quatQ2.textContent = (Q.q2 >= 0 ? "+" : "") + Q.q2.toFixed(4);
      quatQ3.textContent = (Q.q3 >= 0 ? "+" : "") + Q.q3.toFixed(4);
      const qNorm = Math.sqrt(Q.q0*Q.q0 + Q.q1*Q.q1 + Q.q2*Q.q2 + Q.q3*Q.q3);
      quatNorm.textContent = qNorm.toFixed(4);

      // 3. Singularity Condition det(W_η⁻¹) = cos(theta)
      const cosTheta = Math.cos(state.pitch * DEG2RAD);
      valCosTheta.textContent = cosTheta.toFixed(4);
      const absCos = Math.abs(cosTheta);
      barCondition.style.width = `${Math.round(absCos * 100)}%`;

      if (absCos < 0.15) {
        barCondition.className = "h-full bg-rose-500 animate-pulse transition-all duration-150";
        statusSingularity.className = "px-2.5 py-1 rounded bg-rose-950 border border-rose-700 text-rose-300 font-bold animate-pulse";
        statusSingularity.textContent = "GIMBAL LOCK ACTIVE";
        gimbalAlertBanner.classList.remove('hidden');
      } else if (absCos < 0.5) {
        barCondition.className = "h-full bg-amber-400 transition-all duration-150";
        statusSingularity.className = "px-2.5 py-1 rounded bg-amber-950 border border-amber-700 text-amber-300 font-medium";
        statusSingularity.textContent = "Regime: High Pitch";
        gimbalAlertBanner.classList.add('hidden');
      } else {
        barCondition.className = "h-full bg-emerald-400 transition-all duration-150";
        statusSingularity.className = "px-2.5 py-1 rounded bg-slate-800 border border-slate-700 text-emerald-400 font-semibold";
        statusSingularity.textContent = "Regime: Nominal";
        gimbalAlertBanner.classList.add('hidden');
      }

      // 4. Update Velocity Transformation (Tutorial 1 Drill)
      const u = parseFloat(inputU.value) || 0;
      const v = parseFloat(inputV.value) || 0;
      const w = parseFloat(inputW.value) || 0;
      const vBody = vec3(u, v, w);
      const vNED = mat3Vec(R, vBody);

      resPn.textContent = (vNED.x >= 0 ? "+" : "") + vNED.x.toFixed(3) + " m/s";
      resPe.textContent = (vNED.y >= 0 ? "+" : "") + vNED.y.toFixed(3) + " m/s";
      resPd.textContent = (vNED.z >= 0 ? "+" : "") + vNED.z.toFixed(3) + " m/s";

      // 5. Tutorial 1 Angle Recovery Analysis
      // R_v^b is R^T
      const Rvb = [
        [R[0][0], R[1][0], R[2][0]],
        [R[0][1], R[1][1], R[2][1]],
        [R[0][2], R[1][2], R[2][2]]
      ];

      if (absCos < 0.087) { // Within 5 degrees of +/- 90
        recPitch.textContent = (state.pitch > 0 ? "+90.0°" : "-90.0°") + " (Singular!)";
        recRoll.textContent = "Undefined (Coupled)";
        recYaw.textContent = "Undefined (Coupled)";
        recDiffRow.classList.remove('hidden');
        // Observable is atan2(R21, R22)
        const diffRad = Math.atan2(Rvb[1][0], Rvb[1][1]);
        const diffDeg = diffRad * RAD2DEG;
        recDiffVal.textContent = `${diffDeg >= 0 ? "+" : ""}${diffDeg.toFixed(1)}° (ϕ - ψ)`;
      } else {
        recDiffRow.classList.add('hidden');
        const recoveredTheta = Math.atan2(-Rvb[0][2], Math.sqrt(Rvb[0][0]*Rvb[0][0] + Rvb[0][1]*Rvb[0][1])) * RAD2DEG;
        const recoveredPhi = Math.atan2(Rvb[1][2], Rvb[2][2]) * RAD2DEG;
        const recoveredPsi = Math.atan2(Rvb[0][1], Rvb[0][0]) * RAD2DEG;
        recPitch.textContent = `${recoveredTheta >= 0 ? "+" : ""}${recoveredTheta.toFixed(1)}°`;
        recRoll.textContent = `${recoveredPhi >= 0 ? "+" : ""}${recoveredPhi.toFixed(1)}°`;
        recYaw.textContent = `${recoveredPsi >= 0 ? "+" : ""}${recoveredPsi.toFixed(1)}°`;
      }
    }

    // --- EVENT LISTENERS & CONTROLS BINDING ---
    function syncInputs(yaw, pitch, roll) {
      state.yaw = parseFloat(yaw);
      state.pitch = parseFloat(pitch);
      state.roll = parseFloat(roll);

      sliderYaw.value = state.yaw;
      sliderPitch.value = state.pitch;
      sliderRoll.value = state.roll;

      numYaw.value = state.yaw;
      numPitch.value = state.pitch;
      numRoll.value = state.roll;

      updateHUD();
    }

    sliderYaw.addEventListener('input', e => syncInputs(e.target.value, state.pitch, state.roll));
    sliderPitch.addEventListener('input', e => syncInputs(state.yaw, e.target.value, state.roll));
    sliderRoll.addEventListener('input', e => syncInputs(state.yaw, state.pitch, e.target.value));

    numYaw.addEventListener('change', e => syncInputs(e.target.value, state.pitch, state.roll));
    numPitch.addEventListener('change', e => syncInputs(state.yaw, e.target.value, state.roll));
    numRoll.addEventListener('change', e => syncInputs(state.yaw, state.pitch, e.target.value));

    // Preset buttons
    btnReset.addEventListener('click', () => syncInputs(0, 0, 0));
    btnLockPos.addEventListener('click', () => syncInputs(state.yaw, 90, state.roll));
    btnLockNeg.addEventListener('click', () => syncInputs(state.yaw, -90, state.roll));
    btnTutorial1Q6.addEventListener('click', () => syncInputs(-60, 90, 120)); // (phi=120, theta=90, psi=-60)
    btnBankedTurn.addEventListener('click', () => syncInputs(45, -10, 30));
    btnFastForward.addEventListener('click', () => syncInputs(0, -20, 0));

    btnResetCam.addEventListener('click', () => {
      state.camera.azimuth = 45;
      state.camera.elevation = 25;
      state.camera.distance = 7.5;
      camAzimuth.textContent = "45°";
      camElevation.textContent = "25°";
    });

    // Visibility checkboxes
    chkGimbals.addEventListener('change', e => { state.showGimbals = e.target.checked; });
    chkAirframe.addEventListener('change', e => { state.showAirframe = e.target.checked; });
    chkBodyAxes.addEventListener('change', e => { state.showBodyAxes = e.target.checked; });
    chkInertialAxes.addEventListener('change', e => { state.showInertialAxes = e.target.checked; });
    chkIntermediate.addEventListener('change', e => { state.showIntermediate = e.target.checked; });
    chkAutoOrbit.addEventListener('change', e => { state.camera.autoOrbit = e.target.checked; });

    // Velocity input updates
    [inputU, inputV, inputW].forEach(inp => inp.addEventListener('input', updateHUD));

    // --- MOUSE & TOUCH ORBIT CONTROLS ---
    canvas.addEventListener('mousedown', e => {
      state.camera.isDragging = true;
      state.camera.lastMouseX = e.clientX;
      state.camera.lastMouseY = e.clientY;
    });

    window.addEventListener('mouseup', () => {
      state.camera.isDragging = false;
    });

    window.addEventListener('mousemove', e => {
      if (!state.camera.isDragging) return;
      const dx = e.clientX - state.camera.lastMouseX;
      const dy = e.clientY - state.camera.lastMouseY;

      state.camera.azimuth = (state.camera.azimuth - dx * 0.5) % 360;
      if (state.camera.azimuth < 0) state.camera.azimuth += 360;

      state.camera.elevation = Math.max(-85, Math.min(85, state.camera.elevation + dy * 0.5));

      state.camera.lastMouseX = e.clientX;
      state.camera.lastMouseY = e.clientY;

      camAzimuth.textContent = `${Math.round(state.camera.azimuth)}°`;
      camElevation.textContent = `${Math.round(state.camera.elevation)}°`;
    });

    // Mouse wheel zoom
    canvas.addEventListener('wheel', e => {
      e.preventDefault();
      const zoomFactor = e.deltaY * 0.005;
      state.camera.distance = Math.max(3.5, Math.min(18.0, state.camera.distance + zoomFactor));
    }, { passive: false });

    // Touch controls for mobile/tablet devices
    let touchStartX = 0, touchStartY = 0;
    canvas.addEventListener('touchstart', e => {
      if (e.touches.length === 1) {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
      }
    });
    canvas.addEventListener('touchmove', e => {
      if (e.touches.length === 1) {
        e.preventDefault();
        const dx = e.touches[0].clientX - touchStartX;
        const dy = e.touches[0].clientY - touchStartY;
        state.camera.azimuth = (state.camera.azimuth - dx * 0.5) % 360;
        state.camera.elevation = Math.max(-85, Math.min(85, state.camera.elevation + dy * 0.5));
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
        camAzimuth.textContent = `${Math.round(state.camera.azimuth)}°`;
        camElevation.textContent = `${Math.round(state.camera.elevation)}°`;
      }
    }, { passive: false });

    // --- INITIALIZATION ---
    window.addEventListener('resize', () => {
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
    });

    // Initial state and start rendering loop
    syncInputs(0, 0, 0);
    render();
  