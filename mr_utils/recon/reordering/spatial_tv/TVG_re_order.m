function TV_update = TVG_re_order(out_img,beta_sqrd,sort_order_real_x,sort_order_real_y)

% re-ordering in x an y

x_ordered_img=zeros(size(out_img));
y_ordered_img=zeros(size(out_img));

[sx sy]=size(out_img);

for i=1:sy
    a_temp=squeeze(out_img(:,i));
    b_temp=squeeze(sort_order_real_x(:,i));
    y_ordered_img(:,i)=a_temp(b_temp);
end

for i=1:sx
    a_temp=squeeze(out_img(i,:));
    b_temp=squeeze(sort_order_real_y(i,:));
    x_ordered_img(i,:)=a_temp(b_temp);
end

% Computing numerator terms

xpy_img = intshft(x_ordered_img,[0 -1]); 
T1_num = xpy_img - x_ordered_img;
xmy_img = intshft(x_ordered_img,[0 1]); 
T2_num = x_ordered_img - xmy_img;

xyp_img = intshft(y_ordered_img,[-1 0]); 
T3_num = xyp_img - y_ordered_img;
xym_img = intshft(y_ordered_img,[1 0]); 
T4_num = y_ordered_img - xym_img;

xmyp_img_new = intshft(y_ordered_img,[-1 1]);
xmym_img_new = intshft(y_ordered_img,[1 1]);

xpym_img_new = intshft(x_ordered_img,[1 -1]);
xmym_img_new2 = intshft(x_ordered_img,[1 1]);

% Computing denominator terms
T1_den = sqrt(beta_sqrd + abs(T1_num).^2 + (abs((xyp_img - xym_img)/2)).^2);
T2_den = sqrt(beta_sqrd + abs(T2_num).^2 + (abs((xmyp_img_new - xmym_img_new)/2)).^2);
T3_den = sqrt(beta_sqrd + abs(T3_num).^2 + (abs((xpy_img - xmy_img)/2)).^2);
T4_den = sqrt(beta_sqrd + abs(T4_num).^2 + (abs((xpym_img_new - xmym_img_new2)/2)).^2);

% Computing the terms
T1 = T1_num./T1_den;
T2 = T2_num./T2_den;
T3 = T3_num./T3_den;
T4 = T4_num./T4_den;

TV_update_x = T1-T2;
TV_update_y = T3-T4;

TV_update_y_new=zeros(size(TV_update_x));
TV_update_x_new=zeros(size(TV_update_x));


for i=1:sy
    b_temp(sort_order_real_x(:,i))=TV_update_y(:,i);
    TV_update_y_new(:,i)=b_temp;
end

for i=1:sx
    a_temp(sort_order_real_y(i,:))=TV_update_x(i,:);
    TV_update_x_new(i,:)=a_temp;
end

TV_update = TV_update_y_new + TV_update_x_new;

return;

