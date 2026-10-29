function prepare_photos(rot, box)
%PREPARE_PHOTOS  Run ONCE (Coursework 1) to build your face set for CW1 and CW2.
%   1. Put your 13 photos in a folder called raw, named exactly
%      N1 ... N6, E1 ... E4, H1, S2 and C  (.jpg, .jpeg or .png; convert HEIC to JPG first)
%   2. Run  prepare_photos     (or prepare_photos(1) if the photos appear
%      rotated: the number is how many 90-degree anticlockwise turns to apply)
%   3. Drag ONE box around your face on photo N1 (it is made square); the same crop is used for
%      all photos, so the camera must not move between shots.
%   If dragging does not work (e.g. on some MATLAB Online setups), read the face
%   position off the axes of the N1 figure and give it directly:
%      prepare_photos(0, [x y side])   x,y = top-left corner, side = square size (pixels)
%   Output: folder faces/ with N1.png ... S2.png (128x128 grayscale) and C.png

    if nargin < 1 || isempty(rot), rot = 0; end
    L = [face_labels(), {'C'}];
    I = cell(size(L));
    for i = 1:numel(L)
        f = [dir(fullfile('raw', [L{i} '.jp*g'])); dir(fullfile('raw', [L{i} '.JP*G'])); dir(fullfile('raw', [L{i} '.png'])); dir(fullfile('raw', [L{i} '.PNG']))];
        if isempty(f), error('Missing raw/%s.jpg (or .png)', L{i}); end
        x = imread(fullfile(f(1).folder, f(1).name));
        if size(x,3) == 4, x = x(:,:,1:3); end
        if size(x,3) == 1, x = repmat(x, [1 1 3]); end
        x = rot90(im2uint8(x), rot);
        if max(size(x,1), size(x,2)) > 2000             % shrink large phone photos
            x = imresize(x, 2000 / max(size(x,1), size(x,2)));
        end
        I{i} = x;
    end
    sz = cellfun(@(x) size(x,1)*1e5 + size(x,2), I(1:12));
    if any(sz ~= sz(1)), error('All 12 face photos must have the same size (same camera, same setting).'); end

    figure; imshow(I{1}); axis on;
    if nargin >= 2 && ~isempty(box)
        r = round([box(1) box(2) box(3) box(end)]);
    else
        title('Drag a box around your face (N1) and release the mouse; it will be made square');
        try
            r = round(getrect);
        catch
            title('Read the top-left corner (x, y) and the size of a square around your face from the axes');
            error('prepare:nodrag', ['Mouse selection is not available here. Read the face position from ' ...
                  'the axes of the figure and run, for example:  prepare_photos(%d, [x y side])'], rot);
        end
    end
    [H, W, ~] = size(I{1});
    side = min([r(3), r(4), H, W]);                     % force a square inside the photo
    if side < 64
        error('The square is too small (%d pixels). Run prepare_photos again and drag a larger square.', side);
    end
    r(1) = min(max(r(1), 1), W - side + 1);
    r(2) = min(max(r(2), 1), H - side + 1);
    r(3:4) = side - 1;                                  % imcrop returns side x side pixels
    if ~exist('faces', 'dir'), mkdir('faces'); end
    for i = 1:12
        g = rgb2gray(imresize(imcrop(I{i}, r), [128 128]));
        imwrite(g, fullfile('faces', [L{i} '.png']));
    end
    c = I{13}; c = imresize(c, 480/max(size(c,1), size(c,2)));
    imwrite(c, fullfile('faces', 'C.png'));

    figure; montage(fullfile('faces', strcat(L(1:12), '.png')), 'Size', [2 6]);
    title('Check: same position in every photo?  Top: N1-N6   Bottom: E1-E4, H1, S2');
end
