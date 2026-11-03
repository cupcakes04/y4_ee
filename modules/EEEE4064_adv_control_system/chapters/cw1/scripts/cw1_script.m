%% EEEE4064 Advanced Control System Design - Coursework 1
% Student Name: [Nicholas Khor]
% Student ID:   [20617556]

% NOTE: This is very much Ai-assisted, but only in
% - syntax (formating, visualisation, plotting)
% - comments (refining my gibberish)
% - restructuring/teach concepts (oh damn they are good)

clear; clc; close all;

%% 1. Data Import, Preprocessing & Saving (.mat)
% Locate Experimental Data.xlsx
% dT_meas and def_meas are the 2 main datasets (1 input, 2 outputs)
% u is the input and t is the time (dt is sampling interval)

raw_data = readmatrix('Experimental Data.xlsx');
T_meas   = raw_data(:, 1);   % Measured LC heater temperature (deg C)
def_meas = raw_data(:, 2);   % Measured chamber deformation (um)

% Reconstruct time vector (0 to 280 s) and RF input signal (60 mW for 50 s)
N  = size(raw_data, 1);
t  = linspace(0, 280, N)';
dt = t(2) - t(1);            % Sampling interval = 0.625 s
u  = 60 * double(t <= 50);   % RF input power: 60 mW (0-50s), 0 mW (>50s)

% Remove initial ambient temperature offset (23 deg C)
T_ambient = T_meas(1);
dT_meas   = T_meas - T_ambient;

% Save preprocessed data and System Identification objects to .mat file
temperature = iddata(dT_meas,  u, dt, 'Name', 'temperature');
deform      = iddata(def_meas, u, dt, 'Name', 'deform');

%% 2. System Identification
% Load the saved models (from system_identification.sid or cw1_data.mat)
if isfile('system_identification.sid')
    sid_data    = load('system_identification.sid', '-mat');
    pole1_zero1 = sid_data.Model{1};
    pole2_zero1 = sid_data.Model{2};
    pole3_zero1 = sid_data.Model{3};
    pole1_zero0 = sid_data.Model{4};
    pole2_zero0 = sid_data.Model{5};
else
    load('cw1_data.mat', 'pole1_zero1', 'pole2_zero1', 'pole3_zero1', 'pole1_zero0', 'pole2_zero0');
end

% Select the best 2nd-order models (>85% accuracy):
sys_id_T = pole2_zero1;   % Heater Temperature (92.11% fit)
sys_id_D = pole2_zero0;   % Chamber Deformation (93.24% fit)

fit_T = sys_id_T.Report.Fit.FitPercent;
fit_D = sys_id_D.Report.Fit.FitPercent;

fprintf('=== Identified Models ===\n');
fprintf('  Heater Temperature  (%s): Fit = %.2f%%\n', sys_id_T.Name, fit_T);
fprintf('  Chamber Deformation (%s): Fit = %.2f%%\n', sys_id_D.Name, fit_D);

% Simulate identified models over experimental input u(t) and compute residuals
dT_sim   = lsim(sys_id_T, u, t);
T_sim    = dT_sim + T_ambient;
def_sim  = lsim(sys_id_D, u, t);

T_diff   = T_meas - T_sim;       % Temperature estimation difference / error
def_diff = def_meas - def_sim;   % Deformation estimation difference / error

% Populate cw1_data.mat with preprocessed signals, iddata, models, and simulated outputs
save('cw1_data.mat', 't', 'dt', 'u', 'T_meas', 'T_ambient', 'dT_meas', 'def_meas', ...
    'temperature', 'deform', 'pole1_zero1', 'pole2_zero1', 'pole3_zero1', ...
    'pole1_zero0', 'pole2_zero0', 'sys_id_T', 'sys_id_D', ...
    'dT_sim', 'T_sim', 'def_sim', 'T_diff', 'def_diff');

% Plot experimental vs. identified model responses
figure('Name', 'System Identification Verification', 'Color', 'w', 'Position', [100 100 850 380]);
subplot(1, 2, 1);
plot(t, T_meas, 'r-', 'LineWidth', 1.5); hold on;
plot(t, T_sim, 'k--', 'LineWidth', 1.5);
xlabel('Time (s)'); ylabel('Temperature (^\circC)');
title(sprintf('Heater Temperature (%s: %.2f%%)', sys_id_T.Name, fit_T));
legend('Experimental', 'Identified Model', 'Location', 'northeast'); grid on;

subplot(1, 2, 2);
plot(t, def_meas, 'b-', 'LineWidth', 1.5); hold on;
plot(t, def_sim, 'k--', 'LineWidth', 1.5);
xlabel('Time (s)'); ylabel('Deformation (\mum)');
title(sprintf('Chamber Deformation (%s: %.2f%%)', sys_id_D.Name, fit_D));
legend('Experimental', 'Identified Model', 'Location', 'northeast'); grid on;

%% 3. State-Space Modeling & Analysis
models = {
    struct('name', 'Heater Temperature (pole2_zero1)', 'sys_id', sys_id_T, 'unit', 'deg C'), ...
    struct('name', 'Chamber Deformation (pole2_zero0)', 'sys_id', sys_id_D, 'unit', 'um')
};

for m = 1:length(models)
    mdl = models{m};
    fprintf('\n======================================================\n');
    fprintf('%s\n', mdl.name);
    fprintf('======================================================\n');

    % Extract transfer function coefficients:
    % G(s) = (b0*s^2 + b1*s + b2) / (s^2 + a1*s + a2)
    [num, den] = tfdata(tf(mdl.sys_id), 'v');
    b0 = num(1); b1 = num(2); b2 = num(3);
    a1 = den(2); a2 = den(3);

    % --- 1. nth-Order State-Space Form (Beta Coefficients) ---
    beta0 = b0;
    beta1 = b1 - a1 * beta0;
    beta2 = b2 - a1 * beta1 - a2 * beta0;

    A_nth = [0, 1; -a2, -a1];
    B_nth = [beta1; beta2];
    C_nth = [1, 0];
    D_nth = beta0;

    % --- 2. Controllable Canonical Form (CCF) ---
    A_CCF = [0, 1; -a2, -a1];
    B_CCF = [0; 1];
    C_CCF = [b2 - a2 * b0, b1 - a1 * b0];
    D_CCF = b0;

    % --- 3. Observable Canonical Form (OCF) ---
    A_OCF = [0, -a2; 1, -a1];
    B_OCF = [b2 - a2 * b0; b1 - a1 * b0];
    C_OCF = [0, 1];
    D_OCF = b0;

    % --- 4. Eigenvalues, Damping Behavior & Diagonal Canonical Form (DCF) ---
    % Characteristic equation: |lambda*I - A| = lambda^2 + a1*lambda + a2 = 0
    disc = a1^2 - 4 * a2;
    lambda1 = (-a1 + sqrt(disc)) / 2;
    lambda2 = (-a1 - sqrt(disc)) / 2;
    p1 = -lambda1;
    p2 = -lambda2;

    % Damping behavior classification from discriminant (b^2 vs 4ac)
    if disc > 0
        damping_type = 'Overdamped (b^2 > 4ac)';
    elseif disc == 0
        damping_type = 'Critically damped (b^2 = 4ac)';
    else
        damping_type = 'Underdamped (b^2 < 4ac)';
    end

    % Partial fraction residues: G(s) = b0 + c1/(s + p1) + c2/(s + p2)
    c1 = ((b1 - a1 * b0) * lambda1 + (b2 - a2 * b0)) / (lambda1 - lambda2);
    c2 = ((b1 - a1 * b0) * lambda2 + (b2 - a2 * b0)) / (lambda2 - lambda1);

    A_DCF = [-p1, 0; 0, -p2];
    B_DCF = [1; 1];
    C_DCF = [c1, c2];
    D_DCF = b0;

    % --- 5. Diagonalization via Vandermonde Matrix P (x = P*z) ---
    % For distinct real eigenvalues: P = [1, 1; lambda1, lambda2]
    P     = [1, 1; lambda1, lambda2];
    det_P = P(1,1)*P(2,2) - P(1,2)*P(2,1);
    inv_P = (1 / det_P) * [P(2,2), -P(1,2); -P(2,1), P(1,1)];

    A_diag = inv_P * A_CCF * P;   % D = P^(-1)*A*P
    B_diag = inv_P * B_CCF;       % E = P^(-1)*B
    C_diag = C_CCF * P;           % C*P
    D_diag = D_CCF;

    % --- 6. Matrix Algebra & State-Space to Transfer Function ---
    % Determinant and 2x2 cofactor inverse of A_CCF: A^(-1) = (1/|A|) * [d, -b; -c, a]
    det_A = A_CCF(1,1)*A_CCF(2,2) - A_CCF(1,2)*A_CCF(2,1);
    inv_A = (1 / det_A) * [A_CCF(2,2), -A_CCF(1,2); -A_CCF(2,1), A_CCF(1,1)];
    rank_A = (abs(det_A) > 1e-12) + 1;

    % Convert CCF back to Transfer Function: G(s) = C*(sI - A)^(-1)*B + D
    num_manual = [D_CCF, C_CCF(2) + a1*D_CCF, C_CCF(1) + a2*D_CCF];
    den_manual = [1, a1, a2];

    % --- 7. Controllability & Stabilizability ---
    % State controllability matrix: M = [B, A*B] (n x n = 2 x 2)
    M_ctrl     = [B_CCF, A_CCF * B_CCF];
    det_M_ctrl = M_ctrl(1,1)*M_ctrl(2,2) - M_ctrl(1,2)*M_ctrl(2,1);
    rank_M     = (abs(det_M_ctrl) > 1e-12) + 1;

    % Alternative diagonal form condition: no row of E = P^(-1)*B is all zero
    diag_ctrl_ok = all(abs(B_diag) > 1e-12);

    % Output controllability matrix: N = [C*B, C*A*B, D] (m x (n+1)r = 1 x 3)
    N_out  = [C_CCF * B_CCF, C_CCF * A_CCF * B_CCF, D_CCF];
    rank_N = double(any(abs(N_out) > 1e-12));

    % Stabilizability mode test: Ti = [lambda_i*I - A, B] has rank n = 2
    T1_stab = [lambda1*eye(2) - A_CCF, B_CCF];
    T2_stab = [lambda2*eye(2) - A_CCF, B_CCF];

    % --- 8. Observability, Duality & Detectability ---
    % State observability matrix: O = [C^T, A^T * C^T] (n x n = 2 x 2)
    O_obs     = [C_CCF', A_CCF' * C_CCF'];
    det_O_obs = O_obs(1,1)*O_obs(2,2) - O_obs(1,2)*O_obs(2,1);
    rank_O    = (abs(det_O_obs) > 1e-12) + 1;

    % Alternative diagonal form condition: no column of C*P is all zero
    diag_obs_ok = all(abs(C_diag) > 1e-12);

    % Duality principle: observability of (A, B, C) == controllability of dual (A^T, C^T, B^T)
    M_dual = [C_CCF', A_CCF' * C_CCF']; % Identical to O_obs

    % s-Plane pole-zero cancellation check (controllable & observable iff no cancellation)
    tf_zeros = roots(num(find(num ~= 0, 1):end));
    no_cancellation = isempty(tf_zeros) || all(min(abs(tf_zeros - [lambda1, lambda2])) > 1e-6);

    % --- 9. Compare Formula Results with MATLAB Commands ---
    [~, p_mat, ~]      = residue(num, den);
    [num_mat, ~]       = ss2tf(A_CCF, B_CCF, C_CCF, D_CCF);
    M_matlab           = ctrb(A_CCF, B_CCF);
    O_matlab           = obsv(A_CCF, C_CCF); % Note: MATLAB obsv() stacks [C; C*A] = O_obs^T

    fprintf('Eigenvalues & Damping:\n');
    fprintf('  Eigenvalues (lambda) : %.4f, %.4f (MATLAB eig = %.4f, %.4f)\n', ...
        lambda1, lambda2, max(eig(A_CCF)), min(eig(A_CCF)));
    fprintf('  Damping Behavior     : %s\n', damping_type);

    fprintf('\nControllability & Observability Checks:\n');
    fprintf('  State Controllability: |M| = %.4f, rank(M) = %d (MATLAB rank(ctrb) = %d) -> Completely Controllable\n', ...
        det_M_ctrl, rank_M, rank(M_matlab));
    fprintf('  Output Controllability: rank(N) = %d (m = 1) -> Completely Output Controllable\n', rank_N);
    fprintf('  State Observability  : |O| = %.6f, rank(O) = %d (MATLAB rank(obsv) = %d) -> Completely Observable\n', ...
        det_O_obs, rank_O, rank(O_matlab));
    fprintf('  Diagonal Inspection  : E = P^-1*B non-zero = %d | C*P non-zero = %d\n', diag_ctrl_ok, diag_obs_ok);
    fprintf('  s-Plane Cancellation : No pole-zero cancellation = %d (Stabilizable & Detectable)\n', no_cancellation);

    fprintf('\nFormula vs. MATLAB Numerical Precision Check:\n');
    fprintf('  det(A) / inv(A) max diff  : %.2e / %.2e\n', abs(det_A - det(A_CCF)), max(abs(inv_A - inv(A_CCF)), [], 'all'));
    fprintf('  DCF vs residue() max diff : %.2e\n', max(abs(sort([lambda1; lambda2]) - sort(p_mat))));
    fprintf('  SS-to-TF vs ss2tf() diff  : %.2e\n', max(abs(num_manual - num_mat)));
    fprintf('  ctrb() / obsv() max diff  : %.2e / %.2e\n', max(abs(M_ctrl - M_matlab), [], 'all'), max(abs(O_obs' - O_matlab), [], 'all'));

    % Build state-space models and compare simulated responses
    sys_TF   = tf(num, den);
    sys_nth  = ss(A_nth,  B_nth,  C_nth,  D_nth);
    sys_CCF  = ss(A_CCF,  B_CCF,  C_CCF,  D_CCF);
    sys_OCF  = ss(A_OCF,  B_OCF,  C_OCF,  D_OCF);
    sys_DCF  = ss(A_DCF,  B_DCF,  C_DCF,  D_DCF);
    sys_diag = ss(A_diag, B_diag, C_diag, D_diag);

    figure('Name', ['Canonical Forms - ', mdl.name], 'Color', 'w', 'Position', [140+40*m 140+40*m 780 360]);
    lsim(sys_TF, 'k-', sys_nth, 'r--', sys_CCF, 'b:', sys_OCF, 'g-.', sys_DCF, 'm--', sys_diag, 'c:', u, t);
    title(['Response Comparison Across All Representations: ', mdl.name]);
    legend('TF', 'nth-Order', 'CCF', 'OCF', 'DCF', 'Diagonalized (P)', 'Location', 'northeast'); grid on;

    % --- 10. Stability & Transient Response Analysis ---
    cl_poles = pole(feedback(sys_TF, 1));
    info     = stepinfo(60 * sys_TF);
    y_ss     = 60 * (b2 / a2);               % Steady-state value for 60 mW step
    ess      = 1 / (1 + (b2 / a2));          % Unity-feedback step steady-state error

    fprintf('\nStability & Transient Characteristics (60 mW Step):\n');
    fprintf('  Open-Loop Poles   : %.4f, %.4f (Stable)\n', lambda1, lambda2);
    fprintf('  Closed-Loop Poles : %.4f, %.4f (Stable)\n', cl_poles(1), cl_poles(2));
    fprintf('  Rise Time (Tr)    : %.2f s\n', info.RiseTime);
    fprintf('  Settling Time (Ts): %.2f s\n', info.SettlingTime);
    fprintf('  Overshoot (%%OS)   : %.2f %%\n', info.Overshoot);
    fprintf('  Steady-State Value: %.2f %s (MATLAB dcgain = %.2f %s)\n', y_ss, mdl.unit, 60*dcgain(sys_TF), mdl.unit);
    fprintf('  Steady-State Error: %.4f (unit step unity feedback)\n', ess);
end
