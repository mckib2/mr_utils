function img_est = recon_tcr_reorder(prior,reduced_k_space,mask_k_space_sparse,noi,weight_fidelity,weight_temporal,beta_sqrd,use_reorder)

[sort_order_real sort_order_imag] = sort_real_imag_parts(prior,use_reorder);

measuredImgDomain = zeros(size(reduced_k_space));
for i = 1:size(measuredImgDomain,3)
    measuredImgDomain(:,:,i) = single(fftshift(ifft2((reduced_k_space(:,:,i)))));
end

reduced_data = abs(measuredImgDomain);

save('reduced_data.mat','reduced_data')

img_est = measuredImgDomain;
W_img_est = measuredImgDomain;

[rows cols pages] = size(img_est);
R = repmat((1:rows)',[1 cols pages]);
C = repmat(1:cols,[rows 1 pages]);

nIdx_real = R + (C-1)*rows + (sort_order_real-1)*rows*cols;
nIdx_imag = R + (C-1)*rows + (sort_order_imag-1)*rows*cols;

unsort_real_data = single(zeros(size(img_est)));
unsort_imag_data = single(zeros(size(img_est)));

temporal_term_update_real = single(zeros(size(img_est)));
temporal_term_update_imag = single(zeros(size(img_est)));

for iter_no = 1:noi

    if ~mod(iter_no,10)
        fprintf("Status: [%d%%]\r",round(iter_no/noi*100))
    end

    fidelity_update = weight_fidelity*(measuredImgDomain - W_img_est);

    % computing TV term update for real and imag parts with reordering

    real_current_data = real(img_est);
    imag_current_data = imag(img_est);

    real_smooth_data = real_current_data(nIdx_real);
    imag_smooth_data = imag_current_data(nIdx_imag);

    % real part

    temp_a = diff(real_smooth_data,1,3);
    temp_b = temp_a./(sqrt(beta_sqrd + (abs(temp_a).^2)));
    temp_c = diff(temp_b,1,3);

    temporal_term_update_real(:,:,1) = temp_b(:,:,1);
    temporal_term_update_real(:,:,2:end-1) = temp_c;
    temporal_term_update_real(:,:,end) = -temp_b(:,:,end);

    temporal_term_update_real = temporal_term_update_real*weight_temporal;

    unsort_real_data(nIdx_real) = temporal_term_update_real;

    % imag part

    temp_a = diff(imag_smooth_data,1,3);
    temp_b = temp_a./(sqrt(beta_sqrd+(abs(temp_a).^2)));
    temp_c = diff(temp_b,1,3);

    temporal_term_update_imag(:,:,1) = temp_b(:,:,1);
    temporal_term_update_imag(:,:,2:end-1) = temp_c;
    temporal_term_update_imag(:,:,end) = -temp_b(:,:,end);

    temporal_term_update_imag = temporal_term_update_imag*weight_temporal;

    unsort_imag_data(nIdx_imag) = temporal_term_update_imag;

    temporal_term_update = unsort_real_data+sqrt(-1)*unsort_imag_data;
    img_est = img_est+fidelity_update+temporal_term_update;
    W_img_est = ifft2(fft2(img_est).*mask_k_space_sparse);

end

recon_data = img_est;

save('recon_data_reorder.mat','recon_data')
