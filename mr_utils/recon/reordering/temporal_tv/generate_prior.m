function prior=generate_prior(reduced_k_space)

[sx sy sz]=size(reduced_k_space);

no_lines_first=8;
no_lines_last=8;

% center low res data
center_low_res_data = zeros(size(reduced_k_space));
center_low_res_data(:,1:no_lines_first,:) = reduced_k_space(:,1:no_lines_first,:);
center_low_res_data(:,end-no_lines_last:end,:) = reduced_k_space(:,end-no_lines_last:end,:);

temp_data=zeros(sx,40,sz);
temp_data(:,1:no_lines_first,:)=reduced_k_space(:,1:no_lines_first,:);
temp_data(:,end-no_lines_last:end,:)=reduced_k_space(:,end-no_lines_last:end,:);

filter_hamm=hamming(40);
filtered_temp=zeros(size(temp_data));
for i=1:sz
    for j=1:sx
        filtered_temp(j,:,i)=fftshift(filter_hamm').*squeeze(temp_data(j,:,i));
    end
end

new_center_data=zeros(size(center_low_res_data));
new_center_data(:,1:no_lines_first,:)=filtered_temp(:,1:no_lines_first,:);
new_center_data(:,end-no_lines_last:end,:)=filtered_temp(:,end-no_lines_last:end,:);

low_res_imgs=zeros(size(new_center_data));
for i=1:sz
    low_res_imgs(:,:,i)=fftshift(ifft2(new_center_data(:,:,i)));
end

prior=low_res_imgs;

return;
