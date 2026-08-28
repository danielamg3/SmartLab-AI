import serial
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# Configuración del puerto serie
puerto = '/dev/cu.usbmodem14101'  # Cambia por el tuyo

# Intentar conectar con Arduino
try:
    arduino = serial.Serial(puerto, 9600, timeout=1)
    time.sleep(2)
    print("✅ Conectado a Arduino")
except Exception as e:
    print(f"❌ No se pudo conectar al puerto {puerto}")
    print(f"Error: {e}")
    exit()

# Ruta del archivo CSV
nombre_archivo = '../../datos/temperaturas.csv'
os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)

# Listas para almacenar los datos del gráfico
tiempos = []
temperaturas = []
tiempo_inicio = time.time()

# Configurar el gráfico
fig, ax = plt.subplots()
ax.set_xlabel('Tiempo (segundos)')
ax.set_ylabel('Temperatura (°C)')
ax.set_title('Temperatura en tiempo real')
ax.grid(True)
ax.set_ylim([15, 35])

# Función que se ejecuta en cada iteración
def actualizar(frame):
    global tiempos, temperaturas, tiempo_inicio
    
    linea = arduino.readline().decode('utf-8').strip()
    
    if linea:
        try:
            # Intentar convertir a número
            temperatura = float(linea)
            ahora = datetime.now()
            fecha = ahora.strftime('%Y-%m-%d')
            hora = ahora.strftime('%H:%M:%S')
            
            print(f"🌡️ {fecha} {hora} → {temperatura} °C")
            
            # Guardar en CSV
            with open(nombre_archivo, mode='a', newline='') as archivo:
                escritor = csv.writer(archivo)
                if archivo.tell() == 0:
                    escritor.writerow(['Fecha', 'Hora', 'Temperatura_C'])
                escritor.writerow([fecha, hora, temperatura])
            
            # Actualizar listas para el gráfico
            tiempo_actual = time.time() - tiempo_inicio
            tiempos.append(tiempo_actual)
            temperaturas.append(temperatura)
            
            # Limitar a los últimos 30 puntos
            if len(tiempos) > 30:
                tiempos.pop(0)
                temperaturas.pop(0)
            
            # Actualizar el gráfico
            ax.clear()
            ax.plot(tiempos, temperaturas, marker='o', linestyle='-', color='b')
            ax.set_xlabel('Tiempo (segundos)')
            ax.set_ylabel('Temperatura (°C)')
            ax.set_title('Temperatura en tiempo real')
            ax.grid(True)
            ax.set_ylim([15, 35])
            
        except ValueError:
            # Ignorar líneas que no sean números (como "Sistema iniciado")
            pass
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

# Crear la animación
ani = animation.FuncAnimation(fig, actualizar, interval=1000)

# Mostrar el gráfico
plt.show()

# Al cerrar, cerrar conexión
arduino.close()
print("🔌 Conexión cerrada")