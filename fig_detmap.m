% Max Jaderberg 2014
% Produces text/no-text saliency map
close all;
addpath(genpath('./'));
image_folder = 'resized/'; %resized image folder
highlighted_folder = 'highlighted/';
images = dir(image_folder);
exts = {'.jpg', '.png'};
exts = char(exts);

for k = 1:length(images)
    imfn = images(k).name;
    imfn = fullfile(image_folder, imfn);
    [pathstr, image_name, ext] = fileparts(imfn);
    isImage = strmatch(ext, exts, 'exact');
    [m,n] = size(isImage);
    if m == 0 | isImage < 1
        continue;
    end
    im = imread(imfn);

    [w, h, d] = size(im);
    w %298
    h %500
    try
        img = single(rgb2gray(im));
    catch
        img = single(im);
    end

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
    figure;
%     % imshow(h,[0 255]);
%     %set(gca,'LooseInset',get(gca,'TightInset'));
%     set( gca, 'Position', get( gca, 'OuterPosition' ) - ...
%     get( gca, 'TightInset' ) * [-1 0 1 0; 0 -1 0 1; 0 0 1 0; 0 0 0 1] );
%     %iptsetpref('ImshowBorder','tight');
%     %set(gca,'position',[0 0 1 1],'units','normalized');
    imshowc(max(nn.Xout(:,:,2:end), [], 3));   
    saveas(gcf, [highlighted_folder spotted_name], 'png');
    % overwrite the image with the white space 
    RemoveWhiteSpace([], 'file', [highlighted_folder spotted_name '.png'], 'width', w, 'height',h);
    IM = imread([highlighted_folder spotted_name '.png']);
%     [W, H, D] = size(IM);
%     W %298
%     H %500
    
%     IM2 = imclearborder(IM);
%     imwrite(IM2,[highlighted_folder spotted_name '.png']);
end
% % exit