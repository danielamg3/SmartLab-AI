import serial
import time
import csv
from datetime import datetime

puerto = '/dev/cu.usbmodem14101'

try:
    arduino = serial.Serial(puerto, 9600, timeout=1)
    time.sleep(2)
    print("✅ Conectado a Arduino")
except Exception as e:
    print(f"❌ No se pudo conectar al puerto {puerto}")
    print(f"Error: {e}")
    exit()

# Ruta del archivo CSV (relativa a la carpeta donde está este script)
nombre_archivo = '/Users/daniela/Documents/GitHub/SmartLab-AI/datos/temperaturas.csv'# Crear la carpeta 'datos' si no existe (en la raíz del proyecto)
import os
os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)

# Abrir el archivo en modo "append"
with open(nombre_archivo, mode='a', newline='') as archivo:
    escritor = csv.writer(archivo)
    # Si el archivo está vacío, escribir cabecera
    if archivo.tell() == 0:
        escritor.writerow(['Fecha', 'Hora', 'Temperatura_C'])
        print("📄 Archivo CSV creado con cabecera")

print("📡 Guardando datos de temperatura en CSV... (presiona Ctrl+C para salir)")

while True:
    try:
        linea = arduino.readline().decode('utf-8').strip()
        if linea:
            temperatura = float(linea)
            ahora = datetime.now()
            fecha = ahora.strftime('%Y-%m-%d')
            hora = ahora.strftime('%H:%M:%S')
            
            print(f"{fecha} {hora} → {temperatura} °C")
            
            with open(nombre_archivo, mode='a', newline='') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow([fecha, hora, temperatura])
                
    except KeyboardInterrupt:
        print("\n⏹️ Programa terminado por el usuario")
        print(f"📁 Los datos se han guardado en: {nombre_archivo}")
        break
    except ValueError:
        print(f"⚠️ Dato no válido: {linea}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")