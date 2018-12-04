% To determine the sort order for real and imag components

function [sort_order_real_x,sort_order_imag_x,sort_order_real_y,sort_order_imag_y]=sort_real_imag_parts_space(full_data_recon_complex)

[sx sy sz]=size(full_data_recon_complex);

real_full_data=real(full_data_recon_complex);
imag_full_data=imag(full_data_recon_complex);

sort_order_real_x=zeros(size(real_full_data));
sort_order_real_y=zeros(size(real_full_data));

sort_order_imag_x=zeros(size(imag_full_data));
sort_order_imag_y=zeros(size(imag_full_data));

for k=1:sz

    for i=1:sy
        [~, b_temp]=sort(squeeze(real_full_data(:,i,k)));
        sort_order_real_x(:,i,k)=b_temp;
        [~, b_temp]=sort(squeeze(imag_full_data(:,i,k)));
        sort_order_imag_x(:,i,k)=b_temp;
    end

    for i=1:sx
        [~, b_temp]=sort(squeeze(real_full_data(i,:,k)));
        sort_order_real_y(i,:,k)=b_temp;
        [~, b_temp]=sort(squeeze(imag_full_data(i,:,k)));
        sort_order_imag_y(i,:,k)=b_temp;
    end

end
