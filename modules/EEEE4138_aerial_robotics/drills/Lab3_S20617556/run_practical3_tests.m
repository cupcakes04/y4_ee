%% Practical 3, Section 4: run and save all tests (student_id = 19, X configuration)
% Each test: practical3_setup -> overrides -> sim -> save .mat + plots in results/.
% Model settings must already be: fixed-step ode4, 0.01 s, Stop Time 15 s,
% Single simulation output (out), To Workspace blocks as Timeseries at 0.01 s.
if ~exist('results','dir'), mkdir('results'); end
mdl = 'Practical3_Cascaded_PD';

%% 1. Hover (mode 1)
practical3_setup
mode = 1;
run_one(mdl,'hover',15);

%% 2a. Roll 5 deg (mode 1)
practical3_setup
mode = 1;  e1(1) = 5*pi/180;
run_one(mdl,'roll5',15);

%% 2b. Pitch 5 deg (mode 1)
practical3_setup
mode = 1;  e1(2) = 5*pi/180;
run_one(mdl,'pitch5',15);

%% 3. Yaw wrap (mode 1): 179 deg -> 181 deg (= -179 deg)
practical3_setup
mode = 1;
X0(9) = 179*pi/180;  e0(3) = X0(9);  e1(3) = 181*pi/180;
run_one(mdl,'yaw_wrap',15);

%% 4. Climb (mode 2)
practical3_setup
mode = 2;  p1 = [0;0;-.50];
run_one(mdl,'climb',15);

%% 5a. North (mode 2, yaw 0)
practical3_setup
mode = 2;  p1 = [.50;0;0];
run_one(mdl,'north',15);

%% 5b. East (mode 2, yaw 0)
practical3_setup
mode = 2;  p1 = [0;.50;0];
run_one(mdl,'east',15);

%% 6. North facing East (mode 2, yaw +90 deg)
practical3_setup
mode = 2;  p1 = [.50;0;0];
X0(9) = pi/2;  e0(3) = pi/2;  e1(3) = pi/2;
run_one(mdl,'north_facing_east',15);

%% 7. Combined (mode 2)
practical3_setup
mode = 2;  p1 = [.50;.30;-.50];  e1(3) = 15*pi/180;
run_one(mdl,'combined',15);

%% 8. Combined with rotor-speed limit (Omega_max = 575, 8 s)
practical3_setup
mode = 2;  p1 = [.50;.30;-.50];  e1(3) = 15*pi/180;
Omega_max = 575;                  % override AFTER setup (kT stays at its 800 rad/s value)
out = run_one(mdl,'combined_limit',8);

Om   = extract_ts(out.Omega_log);
Traw = extract_ts(out.raw_log);
Tmax = kT*Omega_max^2;
atLimit   = any(Om >= Omega_max - 1e-6, 2);
rawAbove  = any(Traw > Tmax, 2);
rawBelow  = any(Traw < 0, 2);
fprintf('\nLimit test: Tmax = %.4f N per rotor (hover needs %.4f N)\n', Tmax, m_nom*g/4);
fprintf('  max Traw = %.4f N, min Traw = %.4f N\n', max(Traw(:)), min(Traw(:)));
fprintf('  fraction of samples with any applied speed at limit = %.3f\n', mean(atLimit));
fprintf('  fraction with any Traw > Tmax = %.3f, any Traw < 0 = %.3f\n', mean(rawAbove), mean(rawBelow));
t = out.Omega_log.Time;
idx = find(rawAbove);
if ~isempty(idx)
    fprintf('  first clipped sample t = %.2f s, last clipped sample t = %.2f s\n', t(idx(1)), t(idx(end)));
end

figure;
plot(t, Traw, 'LineWidth', 1.2); hold on
yline(Tmax,'k--','T_{max}'); yline(0,'k:','0');
xlabel('Time (s)'); ylabel('Requested rotor thrust T_{raw} (N)');
legend('T_1','T_2','T_3','T_4','Location','best'); grid on
title('Combined with limit: requested thrust vs bounds');
saveas(gcf,'results/combined_limit_traw.png');

% Restore nominal limit before any further runs
practical3_setup

%% ---------- local helpers ----------
function out = run_one(mdl, name, stopTime)
    % Pull the overridden variables from the base workspace and save them.
    out = sim(mdl, 'StopTime', num2str(stopTime));
    vars = {'p1','e0','e1','X0','Omega_max','mode'};
    S = struct('out', out);
    for k = 1:numel(vars)
        S.(vars{k}) = evalin('base', vars{k});
    end
    save(fullfile('results',[name '.mat']), '-struct', 'S');
    plot_run(out, name, S.p1, stopTime);
end

function plot_run(out, name, p1, stopTime)
    t    = out.X_log.Time;
    X    = extract_ts(out.X_log);
    pRef = extract_ts(out.ref_log);
    aRef = extract_ts(out.att_log);
    Om   = extract_ts(out.Omega_log);

    figure('Name',name,'Position',[100 100 900 750]);
    subplot(3,1,1);
    plot(t, X(:,1:3), 'LineWidth', 1.3); hold on
    set(gca,'ColorOrderIndex',1);
    plot(t, pRef, '--', 'LineWidth', 1.0);
    ylabel('NED position (m)'); grid on
    legend('N','E','D','N_{ref}','E_{ref}','D_{ref}','Location','eastoutside');
    title(strrep(name,'_','\_'));

    subplot(3,1,2);
    plot(t, rad2deg(X(:,7:9)), 'LineWidth', 1.3); hold on
    set(gca,'ColorOrderIndex',1);
    plot(t, rad2deg(aRef), '--', 'LineWidth', 1.0);
    ylabel('Attitude (deg)'); grid on
    legend('\phi','\theta','\psi','\phi_{ref}','\theta_{ref}','\psi_{ref}','Location','eastoutside');

    subplot(3,1,3);
    plot(t, Om, 'LineWidth', 1.2);
    xlabel('Time (s)'); ylabel('\Omega (rad/s)'); grid on
    legend('\Omega_1','\Omega_2','\Omega_3','\Omega_4','Location','eastoutside');
    xlim([0 stopTime]);

    saveas(gcf, fullfile('results',[name '.png']));
end

function A = extract_ts(ts)
    if ts.IsTimeFirst
        A = reshape(ts.Data, numel(ts.Time), []);
    else
        A = reshape(ts.Data, [], numel(ts.Time)).';
    end
end
