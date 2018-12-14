% To determine temporal sort order for real and imag components

function [sort_order_real sort_order_imag]=sort_real_imag_parts(data,use_reorder)

if (use_reorder == true)
    load('reordering.mat')
    sort_order_real = double(idx_real) + 1;
    sort_order_imag = double(idx_imag) + 1;
else
    real_data=real(data);
    imag_data=imag(data);

    [temp,sort_order_real]=sort(real_data,3);
    [temp,sort_order_imag]=sort(imag_data,3);
end

return;
