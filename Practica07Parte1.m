%Elaboración del Sistema 1:

function [y, yfinal, porcentajes] = AnalisisFrecuencia(x)
    % Cargar el archivo de audio
    [x, fs] = audioread('audio.wav');

    % Definir las características del filtro pasa banda
    f1 = 2000; % Frecuencia de corte inferior en Hz
    f2 = 5000; % Frecuencia de corte superior en Hz
    N = 1001; % Longitud del filtro (debe ser un número impar)

    % Diseñar el filtro pasa banda utilizando el método de ventana
    b = fir1(N-1, [f1, f2]/(fs/2), 'bandpass');

    % Aplicar el filtro a la señal de entrada
    y = filter(b, 1, x);

    % Calcular la energía de la señal original
    E_original = sum(abs(x).^2);

    % Calcular la energía de la señal filtrada
    E_filtrada = sum(abs(y).^2);

    % Calcular el porcentaje de energía en relación con la señal original
    Porcentaje = (E_filtrada / E_original) * 100;

    % Calcular la transformada de Fourier de la señal filtrada
    Y = fft(y);

    % Obtener el espectro de frecuencias
    espectro = abs(Y).^2;

    % Definir los límites de frecuencia para las 5 bandas
    frecuencia_min = 0; % Frecuencia mínima en Hz
    frecuencia_max = fs/2; % Frecuencia máxima en Hz
    num_bandas = 5; % Número de bandas
    ancho_banda = (frecuencia_max - frecuencia_min) / num_bandas;

    % Inicializar vectores para almacenar la energía y el porcentaje de energía para cada banda
    energia_bandas = zeros(1, num_bandas);
    porcentaje_energia_bandas = zeros(1, num_bandas);

    % Calcular la energía para cada banda
    for i = 1:num_bandas
        % Calcular los índices de frecuencia correspondientes a la banda actual
        indice_min = round((i-1) * ancho_banda * length(espectro) / frecuencia_max) + 1;
        indice_max = round(i * ancho_banda * length(espectro) / frecuencia_max);

        % Calcular la energía para la banda actual
        energia_bandas(i) = sum(espectro(indice_min:indice_max));

        % Calcular el porcentaje de energía para la banda actual con respecto a la energía entre 2KHz y 5KHz
        porcentaje_energia_bandas(i) = (energia_bandas(i) / E_filtrada) * 100;
    end

    % Mostrar las gráficas de la señal original, la señal filtrada y las señales de cada banda
    subplot(3, 2, 1);
    plot(x);
    title('Señal Original');
    xlabel('Tiempo');
    ylabel('Amplitud');

    subplot(3, 2, 2);
    plot(y);
    title('Señal Filtrada');
    xlabel('Tiempo');
    ylabel('Amplitud');

     % Graficar las señales de cada banda y sus respectivos espectros de frecuencia
    for i = 1:num_bandas
        subplot(3, 2, 2 + i);
        plot(y_bandas(i, :));
        title(['Señal de la Banda ' num2str(i)]);
        xlabel('Tiempo');
        ylabel('Amplitud');

        subplot(3, 2, 4 + i);
        plot((i-1)*ancho_banda:(i*ancho_banda-1), espectro((i-1)*ancho_banda+1:i*ancho_banda));
        title(['Espectro de Frecuencia - Banda ' num2str(i)]);
        xlabel('Frecuencia');
        ylabel('Amplitud');
    end

    % Crear el filtro para las 4 bandas finales
    f3 = 0; % Frecuencia de corte inferior para las 4 bandas finales en Hz
    f4 = 2000; % Frecuencia de corte superior para las 4 bandas finales en Hz
    b2 = fir1(N-1, [f3, f4]/(fs/2), 'bandpass');

    % Filtrar la señal original con el filtro de las 4 bandas finales
    yfinal = filter(b2, 1, x);

    % Calcular la energía de la señal final
    E_final = sum(abs(yfinal).^2);

    % Calcular el porcentaje de energía con respecto a la señal filtrada
    porcentaje_final = (E_final / E_filtrada) * 100;

    % Mostrar las gráficas utilizando el fvtool
    figure;
    fvtool(b, 1, b2, 1);
    legend('Filtro 2KHz-5KHz', 'Filtro 0Hz-2KHz');

    % Almacenar las señales y finalizar
    audiowrite('salida_total.wav', y, fs);
    audiowrite('salida_final.wav', yfinal, fs);

    % Devolver las señales y porcentajes de energía
    y = y_bandas;
    porcentajes = porcentaje_energia_bandas;
end
