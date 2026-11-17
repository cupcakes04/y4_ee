%% Section 7: Payload, drag and numerical checks (student_id = 19, X configuration)
% Needs results/diff_pitch.mat from run_validation_tests.m (for the step-size check).
if ~exist('results','dir'), mkdir('results'); end
mdl = 'Practical2_Quadrotor';

%% 1. Payload test: m = 1.80*m0, rotor speeds still at ORIGINAL hover (2 s)
practical2_parameters
m = 1.80*m0;                         % J, kT, kM, Omega_max, Omega_cmd unchanged
out = sim(mdl,'StopTime','2');
save('results/payload.mat','out','X0','Omega_cmd','m','J');

X  = extract_ts(out.X_log);  t = out.X_log.Time;
Xd = extract_ts(out.Xdot_log);
a_pred  = g*(1 - m_nom/m);           % net downward acceleration
fprintf('Payload: wdot(0) = %.6f (pred %.6f) m/s^2\n', Xd(1,6), a_pred);
fprintf('         pD(2) = %.6f (pred %.6f) m, w(2) = %.6f (pred %.6f) m/s\n', ...
    X(end,3), 0.5*a_pred*2^2, X(end,6), a_pred*2);

figure;
plot(t, X(:,3), 'LineWidth',1.5); hold on
plot(t, X(:,6), '--', 'LineWidth',1.5);
plot(t, 0.5*a_pred*t.^2, 'k:', 'LineWidth',1.2);
xlabel('Time (s)'); ylabel('p_D (m) / w (m/s)'); grid on
legend('p_D sim','w sim','p_D = a t^2/2 pred','Location','northwest');
title('Section 7: Payload (m = 1.80 m_0, hover speeds unchanged)');
saveas(gcf,'results/payload.png');

%% 2. Drag test: u(0) = 2 m/s, c_drag = 0.25 vs 0 (2 s)
practical2_parameters
X0(4) = 2.00;  c_drag = 0.25;
out_drag = sim(mdl,'StopTime','2');
save('results/drag.mat','out_drag','X0','c_drag','m');

practical2_parameters
X0(4) = 2.00;  c_drag = 0;
out_nodrag = sim(mdl,'StopTime','2');
save('results/nodrag.mat','out_nodrag','X0','c_drag','m');

Xa = extract_ts(out_drag.X_log);   Xda = extract_ts(out_drag.Xdot_log);  t = out_drag.X_log.Time;
Xb = extract_ts(out_nodrag.X_log);
tau    = m_nom/0.25;
u_pred = 2*exp(-t/tau);
pN_pred = 2*tau*(1 - exp(-t/tau));
fprintf('Drag: udot(0) = %.6f (pred %.6f) m/s^2\n', Xda(1,4), -0.25*2/m_nom);
fprintf('      u(2) = %.6f (pred %.6f) m/s, pN(2) = %.6f (pred %.6f) m, min u = %.4f m/s\n', ...
    Xa(end,4), u_pred(end), Xa(end,1), pN_pred(end), min(Xa(:,4)));
fprintf('No drag: u(2) = %.6f m/s, pN(2) = %.6f m\n', Xb(end,4), Xb(end,1));

figure;
subplot(2,1,1);
plot(t, Xa(:,4),'LineWidth',1.5); hold on
plot(t, Xb(:,4),'--','LineWidth',1.5); plot(t, u_pred,'k:','LineWidth',1.2);
ylabel('u (m/s)'); grid on; legend('c = 0.25','c = 0','2e^{-t/\tau} pred','Location','southwest');
title('Section 7: Drag test');
subplot(2,1,2);
plot(t, Xa(:,1),'LineWidth',1.5); hold on
plot(t, Xb(:,1),'--','LineWidth',1.5);
xlabel('Time (s)'); ylabel('p_N (m)'); grid on; legend('c = 0.25','c = 0','Location','northwest');
saveas(gcf,'results/drag.png');

%% 3. Numerical check: repeat differential pitch with MaxStep = 0.005 s
practical2_parameters
Ti0 = m_nom*g/4;  delta = 0.05*Ti0;
T_target  = [Ti0+delta; Ti0+delta; Ti0-delta; Ti0-delta];
Omega_cmd = sqrt(T_target/kT);
out_fine  = sim(mdl,'StopTime','0.20','MaxStep','0.005');
save('results/diff_pitch_fine.mat','out_fine','X0','Omega_cmd','T_target');

ref = load('results/diff_pitch.mat');               % original run, MaxStep 0.01
X1 = extract_ts(ref.out.X_log);
X2 = extract_ts(out_fine.X_log);
n  = min(size(X1,1), size(X2,1));                   % same 0.01 s logging grid
dX = abs(X1(1:n,:) - X2(1:n,:));
fprintf('Step check: max |dX| over trace = %.3e (any state)\n', max(dX(:)));
fprintf('            final |dq| = %.3e rad/s, |dtheta| = %.3e rad\n', dX(n,11), dX(n,8));

%% 4. Orthogonality / determinant / rank
A = [ones(1,4); -rotor_xy(2,:); rotor_xy(1,:); kMT*sigma(:).'];
fprintf('rank(A) = %d\n', rank(A));

%% helper
function A = extract_ts(ts)
    if ts.IsTimeFirst
        A = reshape(ts.Data, numel(ts.Time), []);
    else
        A = reshape(ts.Data, [], numel(ts.Time)).';
    end
end
