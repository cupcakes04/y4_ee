function [A, L] = load_faces(labels, folder)
%LOAD_FACES  Load face photos as columns of a matrix.
%   [A, L] = load_faces({'N1','N2'})   returns A (16384 x numel(labels)), values in [0,1]
    if nargin < 2, folder = 'faces'; end
    A = zeros(128*128, numel(labels));
    for i = 1:numel(labels)
        x = im2double(imread(fullfile(folder, [labels{i} '.png'])));
        if size(x,3) == 3, x = rgb2gray(x); end
        A(:, i) = x(:);
    end
    L = labels;
end
