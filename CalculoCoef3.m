function[b,a] = CalculoCoef3(x,y,lx)
clc

n=1:length(x);
size(n);
m=input('Ingrese el valor limite para los coeficientes b(M): ');
k=input('Ingrese el valor limite para los coeficientes a (N): ');

M=m+2;
m=m+2;
k=m+k-1;
q=lx-k;
q=1:3000;

w=0:lx-1;

if k>q
  fprintf('ERROR El valor de N y M es mayor que la longitud del vector \n');
else


  for j=1:length(q)
    l=1;
    for i=1:k
      if i<M
        C(j,i)=x(m-i);
    endif
    if i>M-1
      C(j,i)=-y(m-l-1);
      l=l+1;
    endif
  endfor
  b1(j) = y(m-1);
  m=m+l;
endfor

B = transpose(b1);

R=lsqlin(C,B,[],[]);
fprintf('El valor para cada uno de los coeficientes es: [b_o;b_1.......;b_M; a_o;......a_N] \n');
disp(R);
endif

R=transpose(R);

for i=1:M-1
  b(i)=R(1,i);
endfor

a(1)=1;
for j=M:k
  a(j-M+2)=R(1,j);
endfor

syms z;
disp('asdf')
[r,p,k]=residuez(b,a)

h=sum(r./(l-p*z^(-1)))+sum(k*[1 ; z^(-1)]);

for i=l:length(q)
  z=i;
  HH(i)=sum(r./(1-p*z^(-1)))+sum(k*[l ; z^(-1)]);
endfor


f=1/10;
N1=30;
N2=120;

X1=abs(fft(x,N1));
X2=abs(fft(x,N2));

F1x=[(0:N1-l)/N1];
F2x=[(0:N2-l)/N2];

Y1=abs(fft(y,N1));
Y2=abs(fft(y,N2));

F1y=[(0:N1-l)/N1];
F2y=[(0:N2-l)/N2];

figure(1)
subplot(4,2,1)
stem(n,x)
title('X[n]')

subplot(4,2,2)
stem(n,y)
title('Y[n]')

subplot(4,2,3)
stem(F1x,X1,'.')
title('Espectro par X[n] con N=30')

subplot(4,2,4)
stem(F2x,X2,'.')
title('Espectro par X[n] con N=120')

subplot(4,2,5)
stem(F1y,Y1,'.')
title('Espectro por Y[n] con N=30')

subplot(4,2,6)
stem(F2y,X2,'.')
title('Espectro par Y[n] con N=120')

subplot(4,2,7)
stem(q,real(HH))
title('Parte real H[Z]')

subplot(4,2,8)
stem(q,imag(HH))
title('Parte imaginaria H[Z]')

figure(2)
freqz(b,a)
title('Respuesta en Amplitud y Fase H[Z]')

figure(3)
zplane(b,a)
title('Diagrama de Polos y Ceros')

