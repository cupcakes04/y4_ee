test_idx = 4;

% Using formatted string for filename
mat_file = sprintf('results/test%d.mat', test_idx);
save(mat_file, 'out', 'm', 'T_cmd', 'w0', 'z0');

figure; 
plot(out.z_log.Time, out.z_log.Data); 
xlabel('Time (s)'); 
ylabel('Downward position z (m)'); 
grid on; 

% Using formatted string for plot image
png_file = sprintf('results/test%d_position.png', test_idx);
saveas(gcf, png_file);