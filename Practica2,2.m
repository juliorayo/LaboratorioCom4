t=-0.04:0.001:0.04;
x=20*exp(j*(80*pi*t-0.4*pi));
plot3(t, real(x), imag(x)); grid
title('20*e^{j*(80\pit-0.4\pi)}')
xlabel('Tiempo, s'); ylabel('Real'); zlabel('Imag')



