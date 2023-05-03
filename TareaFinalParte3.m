clc
clear
pkg load signal;
pkg load symbolic;
pkg load optim;

[x, fs]=audioread('x3_U017.wav');

lx=length(x);

[y, fs]=audioread('y3_U017.wav');

ly=length(y);

n=1:lx;
figure(1);
subplot(2,1,1);
stem(n,x);
title('X[n]');
subplot(2,1,2);
stem(n,y);
title('Y[n]');

[b,a] = CalculoCoef3(x,y,lx);
