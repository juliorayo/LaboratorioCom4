import numpy as np
from scipy import signal
import scipy.signal as sig
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Menú principal
opcion = 0
while opcion != 6:
    # Menú de opciones
    print('Seleccione una opción:')
    print('1. Grabar')
    print('2. Reproducir')
    print('3. Graficar')
    print('4. Graficar densidad')
    print('5. Grafica RFI')
    print('6. Salir')

    opcion = int(input('Ingrese su elección: '))

    if opcion == 1:
        # Grabación de audio
        try:
            duracion = int(input('Ingrese la duración de la grabación en segundos: '))
            print('Comenzando la grabación...')
            fs = 44100
            data = sd.rec(int(duracion*fs), samplerate=fs, channels=1)
            sd.wait()
            print('Grabación finalizada.')
            wavfile.write('audio.wav', fs, data)
            print('Archivo de audio grabado correctamente.')
        except:
            print('Error al grabar el audio.')

    elif opcion == 2:
        # Reproducción de audio
        try:
            fs, data = wavfile.read('audio.wav')
            sd.play(data, fs)
            sd.wait()
        except:
            print('Error al reproducir el audio.')

    elif opcion == 3:
        # Gráfico de audio
        try:
            fs, data = wavfile.read('audio.wav')
            tiempo = np.linspace(0, len(data)/fs, len(data))
            plt.plot(tiempo, data)
            plt.xlabel('Tiempo (s)')
            plt.ylabel('Amplitud')
            plt.title('Audio')
            plt.show()
        except:
            print('Error al graficar el audio.')

    elif opcion == 4:
        # Graficando espectro de frecuencia
        try:
            print('Graficando espectro de frecuencia...')
            fs, audio = wavfile.read('audio.wav') # Lee la señal desde el archivo .wav
            N = len(audio) # Número de muestras de la señal
            f, Sxx = sig.welch(audio, fs=fs, nperseg=N, scaling='density') # Densidad espectral de potencia
            plt.plot(f, 10*np.log10(Sxx)) # Grafica el espectro de frecuencia en dB
            plt.xlabel('Frecuencia (Hz)')
            plt.ylabel('Densidad espectral de potencia (dB/Hz)')
            plt.title('Espectro de frecuencia de la señal grabada')
            plt.show()
        except:
            print('Error al graficar el audio.')

    elif opcion == 5:
    # Gráfica RFI y RII del audio
    # Cargar el archivo de audio
            fs, input_signal = wavfile.read('audio.wav')

            fc = 1000
            bw = 500
            Wn = np.array([fc-bw/2, fc+bw/2])/(fs/2)
            b, a = signal.butter(2, Wn, 'bandpass')

            fn = 1200
            Wn_notch = fn/(fs/2)
            b_notch, a_notch = signal.iirnotch(Wn_notch, 0.1)
            b_total = np.convolve(b, b_notch)
            a_total = np.convolve(a, a_notch)

            filtered_signal_RFI = signal.lfilter(b_total, a_total, input_signal)

            fc = 1000
            gain = 20
            Wn = fc/(fs/2)
            b, a = signal.cheby1(3, gain, Wn, 'high')

            filtered_signal_RII = signal.lfilter(b, a, filtered_signal_RFI)

            t = np.arange(len(input_signal))/fs

            # Graficar las tres señales en una figura
            fig, axs = plt.subplots(3, 1, figsize=(8, 10))

            axs[0].plot(t, input_signal)
            axs[0].set_xlabel('Tiempo (s)')
            axs[0].set_ylabel('Amplitud')
            axs[0].set_title('Señal original')

            axs[1].plot(t, filtered_signal_RFI)
            axs[1].set_xlabel('Tiempo (s)')
            axs[1].set_ylabel('Amplitud')
            axs[1].set_title('Señal con filtro RFI')

            axs[2].plot(t, filtered_signal_RII)
            axs[2].set_xlabel('Tiempo (s)')
            axs[2].set_ylabel('Amplitud')
            axs[2].set_title('Señal con filtro RII')

            plt.tight_layout()
            plt.show()
        
    elif opcion == 6:
        # Salir
            print("Saliendo del programa...")

    else:
        print("Opción no válida.")
