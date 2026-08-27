# Semana 2: Puente Arduino-Python

*Objetivo de la semana:* Conectar Arduino con Python para leer datos de temperatura, guardarlos en un archivo CSV y hacer gráficos.

---

## Día 1 (25 de agosto de 2026) 

el objetivo de hoy era conseguir que Python leyera los datos de temperatura que envía Arduino a través del puerto USB, y mostrarlos en la terminal.
Lo primero fue modificar el código de Arduino para que solo enviara el número de temperatura, sin texto extra. Así Python podría leerlo fácilmente.

Escribí un script en Python usando la librería pyserial para leer el puerto serie. Pero al ejecutarlo, me encontré con varios problemas. El primer problema era que el archivo estaba vacío Al ejecutar python3 leer_arduino.py, el error era:

```cpp
can't find '__main__' module in '.../leer_arduino.py'
```
Abrí el archivo con el editor nano en la terminal y pegué el código completo. Luego lo guardé correctamente con Ctrl + O → Enter → Ctrl + X.
El segundo problema era que el puerto estaba ocupado, después de arreglar el archivo, al ejecutar el script aparecía:

```cpp
❌ No se pudo conectar al puerto /dev/cu.usbmodem14101
Error: [Errno 16] Resource busy
```
Esto era porque el Monitor Serie del IDE de Arduino estaba abierto, y ocupa el puerto USB. Cerré el Monitor Serie y ejecuté el script de nuevo.
Y luego el nombre del puerto en el script no coincidía En el script, el puerto estaba escrito como:
```cpp
python
puerto = '/dev/cu.usbmodem14101'
```
Y después de todo eso conseguí que funcionara, por fin, vi en la terminal:
```cpp
✅ Conectado a Arduino
📡 Leyendo datos de temperatura... (presiona Ctrl+C para salir)
🌡️ Temperatura: 22.4 °C
🌡️ Temperatura: 22.5 °C
🌡️ Temperatura: 22.3 °C
...
```
Ya tengo datos de temperatura en Python. Esto abre la puerta a guardarlos en un archivo, hacer gráficos y, más adelante, usar inteligencia artificial.
Código final de leer_arduino.py
```cpp
python
import serial
import time

puerto = '/dev/cu.usbmodem14101'

try:
    arduino = serial.Serial(puerto, 9600, timeout=1)
    time.sleep(2)
    print("✅ Conectado a Arduino")
except Exception as e:
    print(f"❌ No se pudo conectar al puerto {puerto}")
    print(f"Error: {e}")
    exit()

print("📡 Leyendo datos de temperatura... (presiona Ctrl+C para salir)")
while True:
    try:
        linea = arduino.readline().decode('utf-8').strip()
        if linea:
            temperatura = float(linea)
            print(f"🌡️ Temperatura: {temperatura} °C")
    except KeyboardInterrupt:
        print("\n⏹️ Programa terminado por el usuario")
        break
    except ValueError:
        print(f"⚠️ Dato no válido: {linea}")
```
Hoy he aprendido que el puerto USB solo puede ser usado por un programa a la vez. Si el Monitor Serie del IDE de Arduino está abierto, Python no puede conectarse. El nombre del puerto debe ser exacto y llevar comillas en el script de Python. Los archivos de Python necesitan el código completo para ejecutarse. Si el archivo está vacío, Python no encuentra el __main__. El editor nano en la terminal es útil, pero hay que recordar guardar con Ctrl + O y salir con Ctrl + X.

Mañana, guardaré estos datos en un archivo CSV para poder hacer gráficos con Python. ¡El proyecto empieza a tomar forma!

---

## Día 2 (26 de agosto de 2026) - 

El objetivo de hoy es modificar el script de Python para que guarde los datos de temperatura en un archivo CSV con fecha y hora, y que el archivo se almacene en una carpeta organizada dentro del proyecto.

Al ejecutar el script `guardar_datos.py`, aparecía un error:
```cpp
FileNotFoundError: [Errno 2] No such file or directory: './datos/temperaturas.csv'
```
Esto era porque la carpeta `datos` no existía en la raíz del proyecto, y la ruta relativa en el script no era correcta. Creé la carpeta `datos` manualmente en la raíz del proyecto (desde VS Code). Luego ajusté la ruta en el script para que apuntara a `../../datos/temperaturas.csv` (subiendo dos niveles desde la carpeta `Python` hasta la raíz del proyecto).

Al principio , el script usaba `'../datos/temperaturas.csv'`, pero el script está en `SmartLab-AI/Código/Python/`, y `'../'` solo sube a `SmartLab-AI/Código/`, donde no está `datos`. Cambié la ruta a `'../../datos/temperaturas.csv'` para que suba hasta la raíz `SmartLab-AI/`, donde está la carpeta `datos`.

### Código final de `guardar_datos.py`

```cpp
import serial
import time
import csv
from datetime import datetime
import os

puerto = '/dev/cu.usbmodem14101'

try:
    arduino = serial.Serial(puerto, 9600, timeout=1)
    time.sleep(2)
    print("✅ Conectado a Arduino")
except Exception as e:
    print(f"❌ No se pudo conectar al puerto {puerto}")
    print(f"Error: {e}")
    exit()

# Ruta del archivo CSV (sube dos niveles hasta la raíz del proyecto)
nombre_archivo = '../../datos/temperaturas.csv'

# Crear la carpeta 'datos' si no existe (por si acaso)
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
```

Después de ejecutar el script y dejar que guardara varios datos, abrí el archivo temperaturas.csv y vi:
```cpp
csv
Fecha,Hora,Temperatura_C
2026-08-26,16:13:58,20.3
2026-08-26,16:13:59,20.3
2026-08-26,16:14:00,20.3
2026-08-26,16:14:01,20.3
2026-08-26,16:14:02,20.3
2026-08-26,16:14:03,20.3
2026-08-26,16:14:04,20.3
```
Ya tengo un registro histórico de temperaturas. Ahora puedo usarlo para hacer gráficos, análisis o incluso entrenar modelos de IA.
Hoy he aprendido que las rutas relativas son útiles, pero hay que entender bien la estructura de carpetas. Subir dos niveles (../../) fue la clave para llegar a la raíz del proyecto.
Crear la carpeta datos manualmente (o con os.makedirs) evita errores de FileNotFoundError.
El archivo CSV es un formato excelente para guardar datos estructurados porque es legible por humanos y fácil de procesar con Python, Excel y otras herramientas.

Mañana, haré un gráfico en tiempo real con matplotlib para visualizar los datos de temperatura mientras se recogen. ¡El proyecto se pone más interesante!

---
