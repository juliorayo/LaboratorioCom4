% Menú para grabar y reproducir una señal de voz
while true
 disp('Seleccione una opción:')
 disp('1. Grabar señal de voz')
 disp('2. Reproducir última señal de voz grabada')
 disp('3. Salir')
 opcion = input('Ingrese el número de la opción: ');

 switch opcion
 case 1
 disp('Grabando señal de voz...')
 try
 % Configuración de la grabación
 duracion_grabacion = 5; % duración de la grabación en segundos
 frecuencia_muestreo = 8000; % frecuencia de muestreo en Hz
 num_bits = 16; % número de bits por muestra
 num_canales = 1; % número de canales de grabación (mono)

 % Grabación de la señal de voz
 grabacion = audiorecorder(frecuencia_muestreo, num_bits, num_canales);
 recordblocking(grabacion, duracion_grabacion);
 senal_grabada = getaudiodata(grabacion);
 disp('Señal de voz grabada exitosamente')
 catch
 disp('Error al grabar señal de voz')
 end
 case 2
 if exist('senal_grabada', 'var')
 disp('Reproduciendo señal de voz...')
 sound(senal_grabada, frecuencia_muestreo)
 else
 disp('No hay señal de voz grabada')
 end
 case 3
 disp('Saliendo del programa')
 break
 otherwise
 disp('Opción inválida')
 end
end
