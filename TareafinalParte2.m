clc
clear
pkg load signal;
pkg load symbolic;
pkg load optim;
[x, fs]=audioread('x2_U017.wav');

lx=length(x);

[y, fs]=audioread('y2_U017.wav');

ly=length(y);

n=0:lx-1;
figure(5);
subplot(2,1,1);
stem(n,x);
title('X[n]');
subplot(2,1,2);
stem(n,y);
title('Y[n]');

[b,a]=CalculoCoef2(x,y);









