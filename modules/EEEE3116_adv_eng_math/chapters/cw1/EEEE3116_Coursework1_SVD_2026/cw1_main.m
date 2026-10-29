function R = cw1_main(studentID)
%CW1_MAIN  EEEE3116 Coursework 1 - Is lighting low-dimensional?
%   Run from the folder that contains faces/ :   R = cw1_main(20512345);
%   Read it: each step is labelled with the equation it
%   implements, and your handwritten analysis refers to these results.
%   Do not rename the file, the function or the fields of R.

    P = cw_params(studentID);
    A = load_faces({'N1','N2','N3','N4','N5','N6'});    % 16384 x 6, one photo per column

    R = struct('studentID', studentID, 'T', P.cw1.T);

    % Step 1: economy SVD  A = U*S*V'   (U: 16384x6, S: 6x6, V: 6x6)
    [U, S, V] = svd(A, 'econ');
    sigma = diag(S)';                                  % singular values, largest first
    R.sigma  = sigma;

    % Step 2: cumulative energy  sum_{i<=k} sigma_i^2 / sum_i sigma_i^2,  and k_T
    R.energy = cumsum(sigma.^2) / sum(sigma.^2);
    R.kT     = find(R.energy >= P.cw1.T/100, 1);

    % Step 3: rank-k approximation A_k = U_k S_k V_k' and its relative error,
    %         measured directly and predicted from the singular values alone
    R.relerr = zeros(1, 6);  R.relerr_pred = zeros(1, 6);
    for k = 1:6
        Ak = U(:,1:k) * S(1:k,1:k) * V(:,1:k)';
        R.relerr(k)      = norm(A - Ak, 'fro') / norm(A, 'fro');
        R.relerr_pred(k) = sqrt(sum(sigma(k+1:end).^2) / sum(sigma.^2));
    end

    % Step 4: project the held-out photos onto span(U_k):  p = U_k*U_k'*x
    %         relative residual = ||x - p|| / ||x||
    X = load_faces({'H1', 'E1'});                      % new lighting, and a smile
    R.res_H1 = zeros(1, 5);  R.res_E1 = zeros(1, 5);
    for k = 1:5
        Uk = U(:, 1:k);
        x = X(:,1);  R.res_H1(k) = norm(x - Uk*(Uk'*x)) / norm(x);
        x = X(:,2);  R.res_E1(k) = norm(x - Uk*(Uk'*x)) / norm(x);
    end

    save('results_cw1.mat', 'R');
    save('svd_cw1.mat', 'U', 'S');                     % used by cw1_figures.m
    fprintf('results_cw1.mat and svd_cw1.mat saved (k_T = %d). Now run cw1_figures(%d).\n', R.kT, studentID);
end
