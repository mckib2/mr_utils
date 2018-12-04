% Program to reconstruct undersampled data with spatial Total Variation constraint and reordering

% Ref: G.Adluru, E.V.R. DiBella. "Reordering for improved constrained reconstruction from undersampled k-space data".
% International Journal of Biomedical Imaging vol. 2008, Article ID 341684, 12 pages, 2008. doi:10.1155/2008/341684.

% Written by: Ganesh Adluru

weight_fidelity = 1;
weight_TV = 0.002;   % regularization parameter
beta_sqrd = 0.00000001;
noi = 5000; % number of iterations

load Coil1_data.mat % fully sampled k-space data
load mask.mat       % undersampling mask

reduced_k_space = Coil1.*mask;

measuredImgDomain = ifft2(reduced_k_space);
img_est = measuredImgDomain;
W_img_est = ifft2(fft2(img_est).*mask);

% prior_data = ifft2(Coil1);  % using fully sampled data as a prior here
% prior_data = ifft2(Coil1.*mask); % using undersampled data as prior here

load tv_prior.mat
prior_data = tv_prior;

fig = figure,imagesc(abs(prior_data)),colormap gray,brighten(0.5),title('Prior');
waitfor(fig)

[sort_order_real_x,sort_order_imag_x,sort_order_real_y,sort_order_imag_y] = sort_real_imag_parts_space(prior_data*1000);

% gradient descent minimization

for iter_no = 1:noi

  if ~mod(iter_no,10)
      fprintf("Status: [%d%%]",round(iter_no/noi*100))
  end

  fidelity_update = weight_fidelity*(measuredImgDomain - W_img_est);

  % Spatial re-ordering - TV
  TV_term_reorder_update_real = TVG_re_order(real(img_est),beta_sqrd,sort_order_real_x,sort_order_real_y);
  TV_term_reorder_update_imag = TVG_re_order(imag(img_est),beta_sqrd,sort_order_imag_x,sort_order_imag_y);
  TV_term_reorder_update = weight_TV*0.5*(TV_term_reorder_update_real + sqrt(-1)*TV_term_reorder_update_imag);

  % Computing spatial regul - TV
  TV_term_update = TVG(img_est,beta_sqrd)*weight_TV*0.5;

  img_est = img_est + fidelity_update + TV_term_update + TV_term_reorder_update;
  W_img_est = ifft2(fft2(img_est).*mask);

end

figure,imagesc(abs(ifft2(Coil1))),colormap gray,brighten(0.5),title('Ground truth')
figure,imagesc(abs(img_est)),colormap gray,brighten(0.5),title('Reconstructed image')
figure,imagesc(abs(measuredImgDomain)),colormap gray,brighten(0.5),title('Undersampled image')
fig = figure,imagesc(abs(prior_data)),colormap gray,brighten(0.5),title('Prior image');

waitfor(fig)

% Write the images when
imwrite(abs(ifft2(Coil1)),'Ground truth.png')
imwrite(abs(img_est),'Reconstructed image.png')
imwrite(abs(measuredImgDomain),'Undersampled image.png')
imwrite(abs(prior_data),'Prior image.png')
