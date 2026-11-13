%% Section 6: Isolated Validation Tests (student_id = 19, X configuration)
if ~exist('results','dir'), mkdir('results'); end

%% 1. Frame mapping check (analytic)
phi = 0; theta = 0; psi = pi/2;
Rx = [1 0 0; 0 cos(phi) -sin(phi); 0 sin(phi) cos(phi)];
Ry = [cos(theta) 0 sin(theta); 0 1 0; -sin(theta) 0 cos(theta)];
Rz = [cos(psi) -sin(psi) 0; sin(psi) cos(psi) 0; 0 0 1];
R  = Rz*Ry*Rx;
v_ned_pred = [0; 5; 0];
v_ned = R * [5; 0; 0];
ortho_err = norm(R*R.' - eye(3));
det_R = det(R);
fprintf('Frame mapping: v_ned = [%.4f %.4f %.4f], norm(R*R''-I) = %.2e, det(R) = %.6f\n', ...
    v_ned(1), v_ned(2), v_ned(3), ortho_err, det_R);

%% 2. Hover (load Section 5 baseline to inspect initial derivative & drift)
load('results/hover.mat');
X_hov  = extract_ts(out.X_log);
Xd_hov = extract_ts(out.Xdot_log);
hov_xdot0_max = max(abs(Xd_hov(1,:)));
hov_xend_max  = max(abs(X_hov(end,:)));
fprintf('Hover: max|Xdot(0)| = %.2e, max|X(end)| = %.2e\n', hov_xdot0_max, hov_xend_max);

%% 3. Free fall (2 s)
practical2_parameters
X0 = zeros(12,1);
Omega_cmd = zeros(4,1);
out = sim('Practical2_Quadrotor','StopTime','2');
save('results/freefall.mat','out','X0','Omega_cmd','m','J');

t_ff = out.X_log.Time;
X_ff = extract_ts(out.X_log);
pD_ff_pred = 0.5 * g * 2^2;
w_ff_pred  = g * 2;
pD_ff_sim  = X_ff(end,3);
w_ff_sim   = X_ff(end,6);
att_ff_max = max(abs(X_ff(end,7:12)));
fprintf('Free fall (t=2 s): pD = %.6f m, w = %.6f m/s, max|att,rates| = %.2e\n', ...
    pD_ff_sim, w_ff_sim, att_ff_max);

figure;
plot(t_ff, X_ff(:,3), 'LineWidth', 1.5); hold on;
plot(t_ff, X_ff(:,6), '--', 'LineWidth', 1.5);
xlabel('Time (s)'); ylabel('Down position (m) / w (m/s)');
legend('p_D (m)', 'w (m/s)', 'Location', 'northwest'); grid on;
title('Section 6: Free Fall Response');
saveas(gcf,'results/freefall.png');

%% 4. Differential pitch (0.20 s)
practical2_parameters
Ti0 = m_nom*g/4;
delta = 0.05*Ti0;
T_target = [Ti0+delta; Ti0+delta; Ti0-delta; Ti0-delta];
Omega_cmd = sqrt(T_target/kT);
assert(all(Omega_cmd >= 0 & Omega_cmd <= Omega_max), 'Omega_cmd out of bounds!');
out = sim('Practical2_Quadrotor','StopTime','0.20');
save('results/diff_pitch.mat','out','X0','Omega_cmd','m','J','T_target');

t_dp  = out.X_log.Time;
X_dp  = extract_ts(out.X_log);
Xd_dp = extract_ts(out.Xdot_log);
F_dp  = extract_ts(out.Fprop_log);
M_dp  = extract_ts(out.Mprop_log);

d_arm        = l/sqrt(2);
Ttotal_pred  = 4*Ti0;
My_pred      = 4*d_arm*delta;
qdot0_pred   = My_pred / J(2,2);
Ttotal_dp    = -F_dp(1,3);
Mx_dp        = M_dp(1,1);
My_dp        = M_dp(1,2);
Mz_dp        = M_dp(1,3);
qdot0_dp     = Xd_dp(1,11);
q_end_dp     = X_dp(end,11);
theta_end_dp = X_dp(end,8);

fprintf('Diff pitch: Fprop(0) = [%.4f %.4f %.4f] N, Mprop(0) = [%.6f %.6f %.6f] N*m\n', ...
    F_dp(1,1), F_dp(1,2), F_dp(1,3), Mx_dp, My_dp, Mz_dp);
fprintf('Diff pitch: qdot(0) = %.6f rad/s^2, q(0.20) = %.6f rad/s, theta(0.20) = %.6f rad\n', ...
    qdot0_dp, q_end_dp, theta_end_dp);

figure;
subplot(2,1,1); plot(t_dp, X_dp(:,11), 'LineWidth', 1.5);
ylabel('q (rad/s)'); title('Section 6: Differential Pitch (0.20 s)'); grid on;
subplot(2,1,2); plot(t_dp, X_dp(:,8), 'LineWidth', 1.5);
xlabel('Time (s)'); ylabel('\theta (rad)'); grid on;
saveas(gcf,'results/diff_pitch.png');

%% 5. Yaw reaction (0.20 s)
practical2_parameters
Ti0 = m_nom*g/4;
delta = 0.05*Ti0;
T_target = [Ti0+delta; Ti0-delta; Ti0+delta; Ti0-delta];
Omega_cmd = sqrt(T_target/kT);
assert(all(Omega_cmd >= 0 & Omega_cmd <= Omega_max), 'Omega_cmd out of bounds!');
out = sim('Practical2_Quadrotor','StopTime','0.20');
save('results/yaw_reaction.mat','out','X0','Omega_cmd','m','J','T_target');

t_yaw  = out.X_log.Time;
X_yaw  = extract_ts(out.X_log);
Xd_yaw = extract_ts(out.Xdot_log);
F_yaw  = extract_ts(out.Fprop_log);
M_yaw  = extract_ts(out.Mprop_log);

Mz_pred     = 4*kMT*delta;
rdot0_pred  = Mz_pred / J(3,3);
Ttotal_yaw  = -F_yaw(1,3);
Mx_yaw      = M_yaw(1,1);
My_yaw      = M_yaw(1,2);
Mz_yaw      = M_yaw(1,3);
rdot0_yaw   = Xd_yaw(1,12);
r_end_yaw   = X_yaw(end,12);
psi_end_yaw = X_yaw(end,9);

fprintf('Yaw reaction: Fprop(0) = [%.4f %.4f %.4f] N, Mprop(0) = [%.6f %.6f %.6f] N*m\n', ...
    F_yaw(1,1), F_yaw(1,2), F_yaw(1,3), Mx_yaw, My_yaw, Mz_yaw);
fprintf('Yaw reaction: rdot(0) = %.6f rad/s^2, r(0.20) = %.6f rad/s, psi(0.20) = %.6f rad\n', ...
    rdot0_yaw, r_end_yaw, psi_end_yaw);

figure;
subplot(2,1,1); plot(t_yaw, X_yaw(:,12), 'LineWidth', 1.5);
ylabel('r (rad/s)'); title('Section 6: Yaw Reaction (0.20 s)'); grid on;
subplot(2,1,2); plot(t_yaw, X_yaw(:,9), 'LineWidth', 1.5);
xlabel('Time (s)'); ylabel('\psi (rad)'); grid on;
saveas(gcf,'results/yaw_reaction.png');

%% 6. Export validation summary table (matches PDF Section 6 table) to CSV
Test = { ...
    'Frame mapping'; ...
    'Hover'; ...
    'Free fall'; ...
    'Differential pitch'; ...
    'Yaw reaction' };

Predicted_quantity_and_value = { ...
    'v_ned = [0; 5; 0] m/s; R*R'' = I3; det(R) = 1'; ...
    'Xdot(0) = 0 (12x1); drift = 0 m over 2 s'; ...
    sprintf('pD(2s) = %.6f m; w(2s) = %.6f m/s; att,rates = 0', pD_ff_pred, w_ff_pred); ...
    sprintf('My = %.6f N*m; qdot(0) = %.6f rad/s^2; Ttotal = %.6f N; Mx = Mz = 0', My_pred, qdot0_pred, Ttotal_pred); ...
    sprintf('Mz = %.6f N*m; rdot(0) = %.6f rad/s^2; Ttotal = %.6f N; Mx = My = 0', Mz_pred, rdot0_pred, Ttotal_pred) };

Simulated_value = { ...
    sprintf('v_ned = [%.4f; %.4f; %.4f] m/s; norm(R*R''-I) = %.2e; det(R) = %.6f', v_ned(1), v_ned(2), v_ned(3), ortho_err, det_R); ...
    sprintf('max|Xdot(0)| = %.2e; max|X(2s)| = %.2e', hov_xdot0_max, hov_xend_max); ...
    sprintf('pD(2s) = %.6f m; w(2s) = %.6f m/s; max|att,rates| = %.2e', pD_ff_sim, w_ff_sim, att_ff_max); ...
    sprintf('My = %.6f N*m; qdot(0) = %.6f rad/s^2; Ttotal = %.6f N; Mx = %.2e, Mz = %.2e N*m; q(0.20) = %.6f rad/s, theta(0.20) = %.6f rad', My_dp, qdot0_dp, Ttotal_dp, Mx_dp, Mz_dp, q_end_dp, theta_end_dp); ...
    sprintf('Mz = %.6f N*m; rdot(0) = %.6f rad/s^2; Ttotal = %.6f N; Mx = %.2e, My = %.2e N*m; r(0.20) = %.6f rad/s, psi(0.20) = %.6f rad', Mz_yaw, rdot0_yaw, Ttotal_yaw, Mx_yaw, My_yaw, r_end_yaw, psi_end_yaw) };

Difference_and_explanation = { ...
    sprintf('max|v_err| = %.2e m/s; orthogonal R (det = +1) maps +x body to +y NED East at psi = pi/2.', max(abs(v_ned - v_ned_pred))); ...
    sprintf('max|X(2s)| = %.2e m; hover thrust cancels gravity (Fg + Fprop = 0) with Mprop = 0 up to roundoff.', hov_xend_max); ...
    sprintf('dpD = %.2e m, dw = %.2e m/s; +g acts along +z Down with zero thrust and unchanged attitude.', abs(pD_ff_sim - pD_ff_pred), abs(w_ff_sim - w_ff_pred)); ...
    sprintf('dMy = %.2e N*m, dqdot(0) = %.2e rad/s^2; +My about body y accelerates q linearly over 0.20 s (zero initial coupling).', abs(My_dp - My_pred), abs(qdot0_dp - qdot0_pred)); ...
    sprintf('dMz = %.2e N*m, drdot(0) = %.2e rad/s^2; sigma = [1;-1;1;-1] produces +Mz and +r/+psi yaw acceleration with Mx = My = 0.', abs(Mz_yaw - Mz_pred), abs(rdot0_yaw - rdot0_pred)) };

T_val = table(Test, Predicted_quantity_and_value, Simulated_value, Difference_and_explanation, ...
    'VariableNames', {'Test', 'Predicted quantity and value', 'Simulated value', 'Difference and explanation'});
writetable(T_val, 'results/section6_validation.csv');
disp(T_val);

%% Local helper
function A = extract_ts(ts)
    if ts.IsTimeFirst
        A = reshape(ts.Data, numel(ts.Time), []);
    else
        A = reshape(ts.Data, [], numel(ts.Time)).';
    end
end

