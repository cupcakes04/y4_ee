function cw1_figures(studentID)
%CW1_FIGURES  Tables and figures for your Coursework 1 results page.
%   Run AFTER cw1_main(studentID), from the folder that contains faces/.
%   %   Output: table1_cw1.csv, table2_cw1.csv, fig1_cw1.png, fig2_cw1.png, fig3_cw1.png
%   -> paste them onto ONE page in Word/Excel/PowerPoint and mark k_T in Table 1.

    S1 = load('results_cw1.mat', 'R');  R = S1.R;
    if R.studentID ~= studentID, error('results_cw1.mat belongs to another ID.'); end
    F = load('svd_cw1.mat', 'U', 'S');  U = F.U;
    Nlab = {'N1','N2','N3','N4','N5','N6'};
    A = load_faces(Nlab);
    X = load_faces({'H1', 'E1'});

    % ---------------- Tables (CSV files you can open in Excel) ----------------
    write_csv('table1_cw1.csv', {'k','sigma_k','cumulative_energy','relerr_measured','relerr_from_sigma'}, ...
              [(1:6)', R.sigma(:), R.energy(:), R.relerr(:), R.relerr_pred(:)]);
    write_csv('table2_cw1.csv', {'k','residual_H1','residual_E1'}, ...
              [(1:5)', R.res_H1(:), R.res_E1(:)]);
    fprintf('Your k_T = %d (energy target %.1f %%)\n', R.kT, R.T);

    % ---------------- Figure 1: N photos (top) and u1..u4 (bottom) ----------------
    f1 = figure('Name', 'Figure 1', 'Position', [50 50 1400 520]);
    for i = 1:6
        subplot(2, 6, i); imshow(reshape(A(:,i), 128, 128)); title(Nlab{i});
    end
    for i = 1:4
        subplot(2, 6, 6 + i);
        imshow(reshape(U(:,i), 128, 128), []);   % [] rescales: u_i has negative values

        title(sprintf('u_%d', i));
    end
    print(f1, '-dpng', '-r150', 'fig1_cw1.png');

    % ---------------- Figure 2: singular values and residual curves ----------------
    f2 = figure('Name', 'Figure 2', 'Position', [50 50 1100 420]);
    subplot(1, 2, 1); semilogy(1:6, R.sigma, 'o-', 'LineWidth', 1.5); grid on;
    xlabel('k'); ylabel('\sigma_k (log scale)'); title('Singular values');
    subplot(1, 2, 2); plot(1:5, R.res_H1, 'o-', 1:5, R.res_E1, 's-', 'LineWidth', 1.5); grid on;
    xlabel('k'); ylabel('relative residual'); legend('H1 (new lighting)', 'E1 (smile)');
    title('Held-out photos vs k');
    print(f2, '-dpng', '-r150', 'fig2_cw1.png');

    % ---------------- Figure 3: residual images at k = 3 ----------------
    f3 = figure('Name', 'Figure 3', 'Position', [50 50 900 420]);
    names = {'H1 (new lighting)', 'E1 (smile)'};
    for j = 1:2
        x = X(:, j);
        p = U(:,1:3) * (U(:,1:3)' * x);          % projection onto span(u1, u2, u3)
        r = x - p;                               % what the lighting subspace cannot explain

        subplot(1, 2, j); imshow(reshape(r, 128, 128), []); colorbar;
        title({'Residual x - p (k = 3)', names{j}});
    end
    print(f3, '-dpng', '-r150', 'fig3_cw1.png');
    fprintf('Saved table1_cw1.csv, table2_cw1.csv, fig1_cw1.png, fig2_cw1.png, fig3_cw1.png\n');
end

function write_csv(file, header, M)
    fid = fopen(file, 'w');
    fprintf(fid, '%s\n', strjoin(header, ','));
    fprintf(fid, [repmat('%.6g,', 1, size(M,2)-1) '%.6g\n'], M');
    fclose(fid);
end
