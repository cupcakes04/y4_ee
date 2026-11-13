%% Section 5: Nominal Hover Baseline Test
practical2_parameters
out = sim('Practical2_Quadrotor');
if ~exist('results','dir'), mkdir('results'); end
save('results/hover.mat','out','X0','Omega_cmd','m','J');

ts = out.X_log;
if ts.IsTimeFirst
    X = reshape(ts.Data,numel(ts.Time),[]);
else
    X = reshape(ts.Data,[],numel(ts.Time)).';
end

figure;
plot(ts.Time,X(:,1:3));
xlabel('Time (s)'); ylabel('NED position (m)');
legend('North','East','Down'); grid on;
title('Section 5: Nominal Hover Position (2 s)');
saveas(gcf,'results/hover_position.png');

