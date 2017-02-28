% Max Jaderberg 2014
% Produces text/no-text saliency map
close all;
addpath(genpath('./'));
image_folder = 'resized/'; %resized image folder
% output_folder = 'highlighted/'
images = dir(image_folder);
exts = {'.jpg', '.png'};
exts = char(exts);

for k = 1:length(images)
    imfn = images(k).name;
    imfn = fullfile(image_folder, imfn);
    [pathstr, name, ext] = fileparts(imfn);
    isImage = strmatch(ext, exts, 'exact');
    [m,n] = size(isImage);
    if m == 0 | isImage < 1
        continue;
    end
    im = imread(imfn);
    class(im)
    [w, h, d] = size(im);
    w %452
    h %466
    img = single(rgb2gray(im));

    %% pad
    img = padarray(img, [11 11]);

    %% preprocess
    winsz = 24;
    mu = (1/winsz^2) * conv2(img, ones(winsz, winsz, 'single'), 'same');
    x_ = (img - mu).^2;
    stdim = sqrt((1/winsz^2) * conv2(x_, ones(winsz, winsz, 'single'), 'same'));
    data = img - mu;
    eps = 1;
    data = data ./ (stdim + eps);

    %% load model
    nn = cudaconvnet_to_mconvnet('models/detnet_layers.mat');

    %% process
    % size(data)

    %% this is the problem
    %% because of input image size
    nn = nn.forward(nn, struct('data', data));
    %% end this is the problem

    %% fig
    spotted_name = imfn(9:(end-4));
    close all;
    h = max(nn.Xout(:,:,2:end), [], 3);
    [n_w, n_h, n_d] = size(h);
    n_w %
    n_h %
%     figure;
%     set(gca,'LooseInset',get(gca,'TightInset'));
    h = imshowc(max(nn.Xout(:,:,2:end), [], 3));
    h = h.CData;
    class(h)
%     saveas(gcf, ['highlighted/' spotted_name '_highlighted'], 'png')
    imwrite(h,['highlighted/' spotted_name '_highlighted.png']);
end
% % exit