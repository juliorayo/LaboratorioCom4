import numpy as np
import matplotlib.pyplot as plt  
from scipy import signal
from scipy.io import wavfile
from scipy.signal import residue, lfilter, freqz, zpk2tf
from scipy.optimize import least_squares

def CalculoCoef2(x, y):
    lx = len(x)
    lx = 5000
    q = np.arange(1, lx+1)
    n = np.arange(1, len(x)+1)

    # Determinación de sistema de ecuaciones simultaneas para dos variables con 
    # mayor número de ecuaciones
    c1 = np.zeros(lx)
    c2 = np.zeros(lx)
    b1 = np.zeros(lx)
    
    for i in range(2000, lx-1):
        c1[i] = x[i-2000]
        c2[i] = -y[i-750]
        b1[i] = y[i] - x[i]

    C1 = c1.reshape(-1, 1)
    C2 = c2.reshape(-1, 1)
    B = b1.reshape(-1, 1)  # Arreglo de matriz de resultados
    D = np.hstack((C1, C2))  # Arreglo de matriz co coeficientes
    R = np.linalg.lstsq(D, B, rcond=None)[0]    # Función que resuelve los mínimos cuadrados
    print('El valor para cada uno de los coeficientes es: ')
    print('A=', R[0][0])
    print('B=', R[1][0])
  
 # Comparación evaluando coeficientes
    print('Comparación de valores para las posiciones entre [2001] y [2016] \n Primera columna: Función encontrada Segunda Fila: Función origianal Tercera fila: Ruido s[n]')
    
    m = np.zeros(16)
    l = np.zeros(16)
    s = np.zeros(16)
    for j in range(2001, 2017):
        m[j-2001] = x[j-1] + R[0,0]*x[j-2001-1] + R[1,0]*y[j-750-1]
        l[j-2001] = y[j-1]
        s[j-2001] = l[j-2001] - m[j-2001]
    
    M = np.transpose([m])
    L = np.transpose([l])
    S = np.transpose([s])

    Comparacion = np.column_stack((M, L, S))
    print(Comparacion)

    b = np.zeros(96000)
    a = np.zeros(96000)
    b[0] = 1
    b[1999] = R[0,0]
    a[0] = 1
    a[749] = R[1,0]

    print('\n Coeficientes de fracciones parciales: \n')
    r, p, k = signal.residuez(np.squeeze(b), np.squeeze(a))
    r = np.transpose(r)
    p = np.transpose(p)

    HH = np.zeros(len(x))
    for i in range(len(x)):
        z = i+1
        HH[i] = np.sum(r/(1-np.multiply(p, z**(-1.0)))) + k[0] + k[1]*z**(-1.0)

    
    #Analisis Espectral
    f = 1/10 #Frecuencia de 0.1Hz
    N1 = 30 # Numero de muestras
    N2 = 120
    #Analisis Espectral para X
    #Transformadas:
    X1 = np.abs(np.fft.fft(x, N1))
    X2 = np.abs(np.fft.fft(x, N2))
    
    # Rango normalizado para transformadas:
    F1x = [(i/N1) for i in range(N1)]
    F2x = [(i/N2) for i in range(N2)]

    # Analisis Espectral para Y
    # Transformadas:
    Y1 = abs(np.fft.fft(y, N1))
    Y2 = abs(np.fft.fft(y, N2))

    # Rango normalizado para transformadas
    F1y = np.arange(N1)/N1
    F2y = np.arange(N2)/N2

    # Grafica de funciones
    # Funciones X y Y
    plt.figure(1)
    plt.subplot(4,2,1)
    plt.stem(n,x)
    plt.title('X[n]')

    plt.subplot(4,2,2)
    plt.stem(n,y)
    plt.title('Y[n]')

    # Grafica del espectro
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
    plt.subplots_adjust(hspace=1.50)
    plt.subplots_adjust(wspace=0.20)
    plt.show()

    # Compute frequency response
    plt.figure(2)
    w, h = signal.freqz(b, a)

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1)

    # Plot amplitude response in first subplot
    ax1.plot(w, abs(h))
    ax1.set_title('Respuesta en Amplitud de H(z)')

    # Plot phase response in second subplot
    ax2.plot(w, np.angle(h))
    ax2.set_title('Respuesta en Fase de H(z)')

    # Show the plot
    plt.show()

    # Respuesta al impulso
    plt.figure(3)
    y = signal.lfilter(b,a,q)
    plt.plot(q,y)
    plt.title('Respuesta al impulso y al escalón unitario')
    plt.show()

    # Polos y ceros
    plt.figure(4)
    zeros, poles, _ = signal.tf2zpk(b,a)
    plt.plot(np.real(zeros),np.imag(zeros),'o', color='red')
    plt.plot(np.real(poles),np.imag(poles),'x', color='blue')
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.title('Diagrama de Polos y Ceros')
    plt.show()
    exit(0)

def problema2():
    # Se lee el archivo de audio x, almacenado en la actual carpeta de trabajo
    fs, x = wavfile.read('x2_U017.wav')
    lx = len(x) # Cálculo del tamaño del vector de audio

    # Se lee el archivo de audio y, almacenado en la actual carpeta de trabajo
    fs, y = wavfile.read('y2_U017.wav')
    ly = len(y) # Cálculo del tamaño del vector de audio

    # Grafica de los vectores
    n = np.arange(lx)
    fig, axs = plt.subplots(2, 1)
    fig.suptitle('Vectores de audio')
    axs[0].stem(n, x)
    axs[0].set_title('X[n]')
    axs[1].stem(n, y)
    axs[1].set_title('Y[n]')
    plt.show()

    # Cálculo de los coeficientes b y a
    b, a = CalculoCoef2(x, y)

problema2()

