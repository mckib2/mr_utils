% To shift image 'm' by coordinates specified by 'sh'

function m2=intshft(m,sh)

[nx,ny]=size(m);

m3=m;
m2=m;

k1=abs(sh(1));
k2=abs(sh(2));

if(sh(1)>0 && sh(2)>0)
    m2(k1+1:nx,k2+1:ny)=m(1:nx-k1,1:ny-k2);
end


if(sh(1)<0 && sh(2)<0)
    m2(1:nx-k1,1:ny-k2)=m(k1+1:nx,k2+1:ny);
end

if(sh(1)>0 && sh(2)<0)
    m2(k1+1:nx,1:ny-k2)=m(1:nx-k1,k2+1:ny);
end

if(sh(1)<0 && sh(2)>0)
    m2(1:nx-k1,k2+1:ny)=m(k1+1:nx,1:ny-k2);
end

if(sh(1)==0 && sh(2)==0)
    m2=m3;
end

if(sh(1)<0 && sh(2)==0)
    m2(1:nx-k1,1:ny)=m(k1+1:nx,1:ny);
end

if(sh(1)>0 && sh(2)==0)
    m2(k1+1:nx,1:ny)=m(1:nx-k1,1:ny);
end

if(sh(1)==0 && sh(2)>0)
    m2(1:nx,k2+1:ny)=m(1:nx,1:ny-k2);
end

if(sh(1)==0 && sh(2)<0)
    m2(1:nx,1:ny-k2)=m(1:nx,k2+1:ny);
end

return;