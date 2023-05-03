import numpy as np
import matplotlib.pyplot as plt  
from scipy import signal
from scipy.io import wavfile
from scipy.signal import residue, lfilter, freqz, zpk2tf
from scipy.optimize import least_squares


def CalculoCoef3(x, y, lx):
    n = np.arange(len(x))
    m = int(input('Ingrese el valor límite para los coeficientes b (M): '))
    k = int(input('Ingrese el valor límite para los coeficientes a (N): '))

    # Determinación de número de incógnitas
    M = m + 2
    m = m + 2
    k = m + k - 1
    q = np.arange(1, 3001)

    w = np.arange(lx)

    if k > len(q):
        print('ERROR: el valor de N y M es mayor que la longitud del vector')
    else:
        # Creación de coeficientes del sistema de ecuaciones
        C = np.zeros((len(q), k))
        b1 = np.zeros(len(q))

        for j in range(len(q)):
            l = 1
            for i in range(k):
                if i < M:
                    C[j, i] = x[m-i]
                if i >= M-1:
                    C[j, i] = -y[m-l-1]
                    l += 1
            b1[j] = y[m-1]
            m += 1
        
        B = b1.reshape(-1, 1)
        
        R = np.linalg.lstsq(C, B, rcond=None)[0]  # Solución a través de mínimos cuadrados
        print('El valor para cada uno de los coeficientes es: [b_0; b_1.......;b_M; a_0;.......a_N]')
        print(R.T)
    
    # Arreglo de vectores para gráficos
    M -= 1
    b = R[:M].flatten()
    a = np.concatenate(([1], R[M:].flatten()))
    
    # Encontrando el valor de H
    r, p, k = signal.residuez(np.squeeze(b), np.squeeze(a))
    r = np.transpose(r)
    p = np.transpose(p)
    h = np.polyval(b, 1j*p) / np.polyval(a, 1j*p)
    
    HH = np.zeros(len(q), dtype=np.complex64)
    for i in range(len(q)):
        z = q[i]
        HH[i] = np.sum(r / (1 - p*z**(-1.0))) + k*np.sum([1, z**(-1.0)])
    
    # Análisis Espectral
    f = 0.1  # Frecuencia de 0.1 Hz
    N1 = 30  # Número de muestras
    N2 = 120
    
    # Análisis Espectral para X
    # Transformadas:
    X1 = np.abs(np.fft.fft(x, N1))
    X2 = np.abs(np.fft.fft(x, N2))
    
    # Rango normalizado para transformadas:
    F1x = np.arange(N1) / N1
    F2x = np.arange(N2) / N2
    
    # Análisis Espectral para Y
    # Transformadas:
    Y1 = np.abs(np.fft.fft(y, N1))
    Y2 = np.abs(np.fft.fft(y, N2))
    
    # Rango normalizado para transformadas:
    F1y = np.arange(N1) / N1
    F2y = np.arange(N2) / N2

    # Gráfica de funciones
    
    # Funciones X y Y
    plt.figure(1)

    plt.subplot(4,2,1)
    plt.stem(n,x)
    plt.title('X[n]')

    plt.subplot(4,2,2)
    plt.stem(n,y)
    plt.title('Y[n]')

    # Grafica del espectro:
    plt.subplot(4,2,3)
    plt.stem(F1x,X1,'.')
    plt.title('Espectro par X[n] con N=30')

    plt.subplot(4,2,4)
    plt.stem(F2x,X2,'.')
    plt.title('Espectro par X[n] con N=120')

    plt.subplot(4,2,5)
    plt.stem(F1y,Y1,'.')
    plt.title('Espectro par Y[n] con N=30')

    plt.subplot(4,2,6)
    plt.stem(F2y,Y2,'.')
    plt.title('Espectro par Y[n] con N=120')

    # Parte real e imaginaria
    plt.subplot(4,2,7)
    plt.stem(q,np.real(HH))
    plt.title('Parte real H[Z]')

    plt.subplot(4,2,8)
    plt.stem(q,np.imag(HH))
    plt.title('Parte imaginaria H[Z]')
    plt.subplots_adjust(hspace=1.50)
    plt.subplots_adjust(wspace=0.20)
    plt.show()
    
    # Respuesta en amplitud y frecuencia
    plt.figure(2)
    w, h = freqz(b, a)
    plt.plot(w/np.pi, np.abs(h))
    plt.title('Respuesta en Amplitud y Fase de H(z)')
    plt.show()

    # Respuesta al impulso
    plt.figure(3)
    y = lfilter(b,a,q)
    plt.plot(q,y)
    plt.title('Respuesta al impulso y al escalón unitario')
    plt.show()

    # Polos y ceros

    z, p = zpk2tf(b, a, 1)
    
    k = 1
    
    fig, ax = plt.subplots()

    uc = plt.Circle((0,0), radius=1, fill=False)
    ax.add_artist(uc)

    # Set the limits of the plot to be the same in both the x and y directions
    plt.axis('equal')

    # graficar ceros y polos en el plano complejo
    zplane_plot = ax.scatter(np.real(z), np.imag(z), marker='o', s=50, facecolors='none', edgecolors='b')
    pole_plot = ax.scatter(np.real(p), np.imag(p), marker='x', s=50, color='r')

    # agregar leyenda
    plt.legend([zplane_plot, pole_plot], ['Zeros', 'Polos'])

    # agregar título y mostrar gráfico
    plt.title('Diagrama de Polos y Ceros')
    plt.show()

def problema3():
    # Se lee el archivo de audio x, almacenado en la actual carpeta de trabajo
    fs, x = wavfile.read('x2_U017.wav')
    lx = len(x)  # Cálculo del tamaño del vector de audio

    # Se lee el archivo de audio y, almacenado en la actual carpeta de trabajo
    fs, y = wavfile.read('y2_U017.wav')
    ly = len(y)  # Cálculo del tamaño del vector de audio

    # Grafica de los vectores
    n = np.arange(lx)
    fig, axs = plt.subplots(2, 1)
    axs[0].stem(n, x)
    axs[0].set_title('X[n]')
    axs[1].stem(n, y)
    axs[1].set_title('Y[n]')
    plt.show()

    # Para la solución del problema
    CalculoCoef3(x,y,lx)


problema3()

 

