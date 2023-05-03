import numpy as np
import sounddevice as sd
import scipy.signal as signal
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from scipy.signal import zpk2tf

opcion = 0
while opcion != 6:
    # Menú de opciones
    print("Seleccione una opción:")
    print("1. Grabar")
    print("2. Reproducir")
    print("3. Graficar")
    print("4. Graficar densidad")
    print("5. Graficar con Transformada Z")
    print("6. Salir")

    opcion = int(input("Ingrese su elección: "))

    if opcion == 1:
        # Grabación de audio
        try:
            duracion = int(input("Ingrese la duración de la grabación en segundos: "))
            print("Comenzando la grabación...")
            fs = 48000  # frecuencia de muestreo
            grabacion = sd.rec(duracion * fs, channels=1)
            sd.wait()
            print("Grabación finalizada.")
            data = grabacion[:, 0]
            wav.write('audio.wav', fs, data)
            print("Archivo de audio grabado correctamente.")
        except:
            print("Error al grabar el audio.")

    elif opcion == 2:
        # Reproducción de audio
        try:
            fs, data = wav.read('audio.wav')
            sd.play(data, fs)
            sd.wait()
        except:
            print("Error al reproducir el audio.")

    elif opcion == 3:
        # Gráfico de audio
        try:
            fs, data = wav.read('audio.wav')
            tiempo = np.linspace(0, len(data)/fs, len(data))
            plt.plot(tiempo, data)
            plt.xlabel('Tiempo (s)')
            plt.ylabel('Amplitud')
            plt.title('Audio')
            plt.show()
        except:
            print("Error al graficar el audio.")

    elif opcion == 4:
        # Graficando espectro de frecuencia
        try:
            print("Graficando espectro de frecuencia...")
            fs, audio = wav.read('audio.wav')  # Lee la señal desde el archivo .wav
            N = len(audio)  # Número de muestras de la señal
            f, Sxx = signal.welch(audio, fs, window='hann', nperseg=N, scaling='density')  # Densidad espectral de potencia
            plt.plot(f, 10*np.log10(Sxx))  # Grafica el espectro de frecuencia en dB
            plt.xlabel('Frecuencia (Hz)')
            plt.ylabel('Densidad espectral de potencia (dB/Hz)')
            plt.title('Espectro de frecuencia de la señal grabada')
            plt.show()
        except:
            print("Error al graficar el audio.")

    elif opcion == 5:
        try:
            fs, x = wav.read('audio.wav')
            x = np.mean(x, axis=1)
            b, a = [1.0, -1.0], [1.0, 0.0]

        # Graficar la señal original y la señal con la transformada Z aplicada
            plt.figure(figsize=(8, 10))
            plt.subplot(2, 1, 1)
            plt.plot(np.arange(len(x))/fs, x)
            plt.xlabel('Tiempo (s)')
            plt.ylabel('Amplitud')
            plt.title('Señal original')

            y = signal.lfilter(b, a, x)
            plt.subplot(2, 1, 2)
            plt.plot(np.arange(len(y))/fs, y)
            plt.xlabel('Tiempo (s)')
            plt.ylabel('Amplitud')
            plt.title('Señal con Transformada Z aplicada')

            plt.tight_layout()
            plt.show()
        except:
            print("Error al graficar la señal con la Transformada Z aplicada.")
                     
    elif opcion == 6:
        # Salir
        print("Saliendo del programa...")

    else:
        print("Opción no válida.")

