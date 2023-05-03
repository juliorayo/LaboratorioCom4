function y = Ecualizador(Ganancias, 'G:/Prácticas Lab Com 4/audio.wav')
    % Cargar el archivo de audio
    [x, fs] = audioread('audio.wav');

    % Definir las frecuencias centrales de las 10 bandas
    frecuencias_centrales = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000];

    % Crear los filtros digitales para cada banda utilizando las funciones de MATLAB
    filtros = cell(1, 10);
    for i = 1:10
        f1 = frecuencias_centrales(i) / (fs/2);
        f2 = f1 * 2;
        filtros{i} = designfilt('bandpassiir', 'FilterOrder', 8, 'HalfPowerFrequency1', f1, 'HalfPowerFrequency2', f2);
    end

    % Aplicar las ganancias a los filtros
    for i = 1:10
        filtros{i}.Gain = Ganancias(i);
    end

    % Aplicar los filtros a la señal de entrada
    y = zeros(size(x));
    for i = 1:10
        y = y + filter(filtros{i}, x);
    end

    % Normalizar la señal de salida para evitar saturación
    y = y / max(abs(y));

    % Mostrar las respuestas de cada filtro y la respuesta del sistema en general
    figure;
    for i = 1:10
        subplot(5, 2, i);
        freqz(filtros{i});
        title(['Respuesta del Filtro - Banda ' num2str(i)]);
    end

    subplot(5, 2, 11);
    freqz(sum(cat(1, filtros{:})));
    title('Respuesta del Sistema');

    % Mostrar las gráficas de las señales de entrada y salida y sus respectivos espectros
    figure;
    subplot(2, 2, 1);
    plot(x);
    title('Señal de Entrada');
    xlabel('Tiempo');
    ylabel('Amplitud');

    subplot(2, 2, 2);
    plot(y);
    title('Señal de Salida');
    xlabel('Tiempo');
    ylabel('Amplitud');

    subplot(2, 2, 3);
    spectrogram(x, hann(256), 128, 512, fs, 'yaxis');
    title('Espectro de Frecuencia - Señal de Entrada');
    colorbar('off');

    subplot(2, 2, 4);
    spectrogram(y, hann(256), 128, 512, fs, 'yaxis');
    title('Espectro de Frecuencia - Señal de Salida');
    colorbar('off');

    % Almacenar la señal de salida en formato WAV
    audiowrite('salida_ecualizada.wav', y, fs);
end
