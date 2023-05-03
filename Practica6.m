% Comprueba si estamos ejecutando en MATLAB o en Octave
if (exist("OCTAVE_VERSION", 'builtin') ~= 0)
    % Estamos en Octave
    pkg load signal;
end

% Menú principal
opcion = 0;
while opcion ~= 5
    % Menú de opciones
    disp('Seleccione una opción:');
    disp('1. Grabar');
    disp('2. Reproducir');
    disp('3. Graficar');
    disp('4. Graficar densidad');
    disp('5. Nuevo');
    disp('6. Salir');

    opcion = input('Ingrese su elección: ');

    switch opcion
        case 1
            % Grabación de audio
            try
                duracion = input('Ingrese la duración de la grabación en segundos: ');
                disp('Comenzando la grabación...');
                recObj = audiorecorder;
                recordblocking(recObj, duracion);
                disp('Grabación finalizada.');
                data = getaudiodata(recObj);
                audiowrite('audio.wav', data, recObj.SampleRate);
                disp('Archivo de audio grabado correctamente.');
            catch
                disp('Error al grabar el audio.');
            end

        case 2
            % Reproducción de audio
            try
                [data, fs] = audioread('audio.wav');
                sound(data, fs);
            catch
                disp('Error al reproducir el audio.');
            end

        case 3
            % Gráfico de audio
            try
                [data, fs] = audioread('audio.wav');
                tiempo = linspace(0, length(data)/fs, length(data));
                plot(tiempo, data);
                xlabel('Tiempo (s)');
                ylabel('Amplitud');
                title('Audio');
            catch
                disp('Error al graficar el audio.');
            end

        case 4
            % Graficando espectro de frecuencia
            try
                disp('Graficando espectro de frecuencia...');
                [audio, Fs] = audioread('audio.wav'); % Lee la señal desde el archivo .wav
                N = length(audio); % Número de muestras de la señal
                f = linspace(0, Fs/2, N/2+1); % Vector de frecuencias
                ventana = hann(N); % Ventana de Hann para reducir el efecto de las discontinuidades al calcular la FFT
                Sxx = pwelch(audio, ventana, 0, N, Fs); % Densidad espectral de potencia
                plot(f, 10*log10(Sxx(1:N/2+1))); % Grafica el espectro de frecuencia en dB
                xlabel('Frecuencia (Hz)');
                ylabel('Densidad espectral de potencia (dB/Hz)');
                title('Espectro de frecuencia de la señal grabada');
            catch
                disp('Error al graficar el audio.');
            end

        case 5
            try
                pkg load signal

                [y, fs] = audioread('audio.wav');

                dct_y = dct(y);

                umbral = 0.1;

                dct_y_comprimido = dct_y .* (abs(dct_y) > umbral);

                y_comprimido = idct(dct_y_comprimido);

                t = (0:length(y)-1)/fs;
                t_comp = (0:length(y_comprimido)-1)/fs;

                subplot(2,1,1);
                plot(t, y);
                title('Archivo de audio inicial');
                xlabel('Tiempo (s)');
                ylabel('Amplitud');

                subplot(2,1,2);
                plot(t_comp, y_comprimido);
                title('Archivo de audio comprimido');
                xlabel('Tiempo (s)');
                ylabel('Amplitud');

            catch
                disp('Error al graficar el audio');
            end

        case 6
            % Salir
            disp('Saliendo del programa...');

        otherwise
            disp('Opción no válida.');
    end
end
