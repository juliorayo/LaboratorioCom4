% Comprueba si estamos ejecutando en MATLAB o en Octave
if (exist("OCTAVE_VERSION", 'builtin') ~= 0)
    % Estamos en Octave
    pkg load signal;
end

% Menú principal
opcion = 0;
while opcion ~= 6
    % Menú de opciones
    disp('Seleccione una opción:');
    disp('1. Grabar');
    disp('2. Reproducir');
    disp('3. Graficar');
    disp('4. Graficar densidad');
    disp('5. Grafica RFI');
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
            % Cargar el archivo de audio
            try
            [input_signal, fs] = audioread('audio.wav');
            fc = 1000;
            bw = 500;
            Wn = [fc-bw/2, fc+bw/2]/(fs/2);
            [b,a] = butter(2, Wn);
            fn = 1200;
            Wn_notch = fn/(fs/2);
            [b_notch, a_notch] = pei_tseng_notch(Wn_notch, 0.1);
            b_total = conv(b, b_notch);
            a_total = conv(a, a_notch);
            filtered_signal_RFI = filter(b_total, a_total, input_signal);

            fc = 1000;
            gain = 20;

            Wn = fc/(fs/2);

            [b, a] = cheby1(3, gain, Wn, 'high');

            filtered_signal_RII = filter(b, a, filtered_signal_RFI);

            t = 0:1/fs:(length(input_signal)-1)/fs;
            figure();
            plot(t, input_signal);
            xlabel('Tiempo (s)');
            ylabel('Amplitud');
            title('Señal original');

            t = 0:1/fs:(length(filtered_signal_RFI)-1)/fs;
            figure();
            plot(t, filtered_signal_RFI);
            xlabel('Tiempo(s)');
            ylabel('Amplitud');
            title('Señal filtrada con filtro RFI');

            t = 0:1/fs:(length(filtered_signal_RII)-1)/fs;
            figure();
            plot(t, filtered_signal_RII);
            xlabel('Tiempo (s)');
            ylabel('Amplitud');
            title('Señal filtrada con filtro RII');

            end

        case 6
            % Salir
            disp('Saliendo del programa...');

        otherwise
            disp('Opción no válida.');
    end
end
