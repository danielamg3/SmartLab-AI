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

## Día 2 (26 de agosto de 2026) 

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
## Día 3 (27 de agosto de 2026) 

Hoy tocaba la parte más visual, ver la temperatura en un gráfico que se actualiza solo, sin tener que hacer nada. Quería que los datos que llegan de Arduino se pintaran en una ventana, punto a punto, como si fuera un electrocardiograma pero de temperatura.

Lo primero que había que hacer era instalar matplotlib. Para hacer gráficos en Python necesito una librería llamada **`matplotlib`**. Es una herramienta que le dice a Python cómo dibujar líneas, puntos, ejes y todo eso. Pero esta librería no viene instalada por defecto. Hay que descargarla e instalarla. Para eso, usé la terminal.

La terminal es una ventana donde se escriben órdenes directamente al ordenador, sin botones ni ventanas bonitas. Parece complicada, pero es muy útil para instalar cosas o ejecutar programas.
Escribí esto:

```cpp
pip3 install matplotlib
```
pip3 es el "gestor de paquetes" de Python. Es como una tienda de aplicaciones, pero para código.
install le dice que quiero instalar algo.
matplotlib es el nombre de la librería.

Luego creé un nuevo script en VS Code llamado grafico_tiempo_real.py. Voy a explicar sus partes más importantes de forma sencilla:

1. Importar las librerías
```cpp
import serial
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
```
Cada import es como pedir prestada una herramienta:
serial → para hablar con Arduino.
csv → para guardar datos en el archivo.
datetime → para poner la fecha y hora.
matplotlib → para dibujar el gráfico.
animation → para que el gráfico se mueva solo.
os → para crear carpetas si no existen.

2. Conectar con Arduino
```cpp
puerto = '/dev/cu.usbmodem14101'
arduino = serial.Serial(puerto, 9600, timeout=1)
```
Aquí le digo a Python: "Conéctate al mismo puerto USB donde está Arduino". El número 9600 es la velocidad a la que hablan.

3. Las listas para guardar los datos
```cpp
tiempos = []
temperaturas = []
```
Son como dos cajas vacías. Una guardará los segundos desde que empieza el programa, y la otra guardará la temperatura en ese momento. Así podemos dibujar los pares (tiempo, temperatura).

4. La función que se repite cada segundo
```cpp
def actualizar(frame):
    linea = arduino.readline().decode('utf-8').strip()
    ...
```
Esta función se ejecuta automáticamente cada segundo. Hace lo siguiente:
Lee una línea del puerto serie (el número que envía Arduino).
Si la línea tiene un número, lo convierte a temperatura.
Guarda la fecha y hora.
Añade el dato a las listas tiempos y temperaturas.
Limpia el gráfico y lo vuelve a dibujar con los nuevos puntos.

5. La animación
```cpp
ani = animation.FuncAnimation(fig, actualizar, interval=1000)
```
Esta línea es la magia. Le dice a Python: "Ejecuta la función actualizar cada 1000 milisegundos (1 segundo) y actualiza el gráfico".

Al ejecutar el script, la terminal mostraba:
```cpp
⚠️ Dato no válido: Valor: 526 | Temp: 20.7 C
⚠️ Dato no válido: Sistema iniciado
```
¿Qué pasaba? El script esperaba recibir un número limpio, como 20.7, pero Arduino estaba enviando texto extra: Valor: 526 | Temp: 20.7 C. Cuando Python intentaba convertir esa línea a número, no podía y daba error.
Por eso modifiqué el código de Arduino para que solo enviara el número, sin texto. Así:
```cpp
Serial.println(temperatura, 1);
```
Con eso, Arduino solo envía 20.7 y Python lo entiende perfectamente. Después de arreglar eso, ejecuté el script y vi:
```cpp
 2026-08-28 12:15:00 → 20.7 °C
 2026-08-28 12:15:01 → 20.8 °C
```
Y en una ventana nueva, el gráfico se dibujaba solo, punto a punto, mostrando cómo cambiaba la temperatura.
Incluso probé a tocar el termistor y vi cómo subía en el gráfico.

Hoy he aprendido a instalar librerías con pip, es normal y seguro. Es la forma estándar de añadir funcionalidades a Python. 
El formato de los datos es clave. Si Arduino envía texto extra, Python no puede interpretarlo. Para comunicar dos programas, hay que ponerse de acuerdo en el formato.
matplotlib permite hacer gráficos en tiempo real con muy poco código. Es una herramienta muy potente para visualizar datos.

Mañana, en el Día 4, añadiré más datos al gráfico o mejoraré su formato.

---
## Día 4 (28 de agosto de 2026) 

Hoy tocaba mejorar el aspecto visual del gráfico en tiempo real y, sobre todo, organizar el proyecto de una vez por todas. Llevaba días con carpetas duplicadas, rutas que no funcionaban y nombres en inglés y español mezclados. Hoy hem puesto orden.

He modificado el script `grafico_tiempo_real.py` para que el gráfico sea más profesional y fácil de interpretar.

Cambios aplicados:
- Tamaño más grande (`figsize=(10, 6)`) para que se vea mejor.
- Título descriptivo: "Temperatura en tiempo real - BioLab AI".
- Color naranja (`#FF6B35`) para la línea, más visible que el azul por defecto.
- Línea de referencia a 25 °C (temperatura ambiente típica) en rojo discontinuo.
- Leyenda que explica qué significa cada línea.
- Cuadrícula más suave (`linestyle='--'`) para no saturar la vista.

Código principal de la mejora:

```cpp
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title('🌡️ Temperatura en tiempo real - BioLab AI', fontsize=14, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_ylim([15, 35])
ax.axhline(y=25, color='red', linestyle=':', linewidth=1, label='Referencia 25°C')
ax.legend(loc='upper right')
ax.plot(tiempos, temperaturas, marker='o', linestyle='-', color='#FF6B35', linewidth=2, label='Temperatura')
Guardado automático de imágenes
```
He añadido una funcionalidad muy útil: cada 60 segundos, el gráfico se guarda automáticamente como imagen en la carpeta Gráficas/. Así tengo un registro visual de cómo evoluciona la temperatura sin tener que hacer capturas de pantalla manuales.

Código añadido:

```cpp
# Variables para el guardado automático
ultimo_guardado = time.time()
intervalo_guardado = 60  # segundos

# Dentro de la función actualizar:
if ahora_guardado - ultimo_guardado >= intervalo_guardado:
    timestamp = ahora.strftime('%Y%m%d_%H%M%S')
    nombre_imagen = f'grafico_{timestamp}.png'
    ruta_imagen = os.path.join(ruta_graficas, nombre_imagen)
    fig.savefig(ruta_imagen, dpi=150, bbox_inches='tight')
    print(f"📸 Imagen guardada en: {ruta_imagen}")
    ultimo_guardado = ahora_guardado
```
Cada imagen se guarda con un nombre único (ej: grafico_20260828_121530.png) y buena resolución (dpi=150).

El gran problema de hoy ha sido organizar las carpetas. Tenía carpetas duplicadas (datos y Datos, assets y Assets), rutas relativas que no funcionaban (../../) y nombres en inglés y español mezclados. He decidido la siguiente estructura:

```cpp
SmartLab-AI/
├── README.md                      
├── Diario/
│   ├── semana_1.md                
│   └── semana_2.md                
├── Código/
│   ├── arduino/
│   │   ├── temp/ voltj thermistor
│   │   ├── temp/humd DHT11
│   │   └── temp + LCD
│   └── python/
│       ├── leer_arduino.py        
│       ├── guardar_datos.py
│       ├── calculadora.py
│       ├── Texto de Terminal.txt
│       └── grafico_tiempo_real.py 
├── Datos/
│   └── temperaturas.csv           
├── Gráficas/
│   ├── grafico_20260828_121530.png  
│   └── ... (más imágenes)
└── Assets/                        
    ├── DHT11 2 16/8 .HEIC
    ├── TERMISTOR + LCD 2 17/8 .HEIC
    └── ...
```
Para evitar problemas con las rutas, he cambiado todos los scripts para que usen rutas absolutas en lugar de relativas. Así siempre funcionan, independientemente de dónde se ejecuten.

He modificado el código de Arduino para que mida la temperatura cada 5 segundos en lugar de cada 2. Es más razonable porque la temperatura ambiente no cambia tan rápido y así el archivo CSV no crece excesivamente.

Código final del día
```cppp
python
import serial
import time
import csv
from datetime import datetime
import os

usuario = "daniela"
ruta_proyecto = f"/Users/{usuario}/Documents/GitHub/SmartLab-AI"
ruta_datos = os.path.join(ruta_proyecto, "Datos")
os.makedirs(ruta_datos, exist_ok=True)
nombre_archivo = os.path.join(ruta_datos, "temperaturas.csv")

puerto = '/dev/cu.usbmodem14101'

try:
    arduino = serial.Serial(puerto, 9600, timeout=1)
    time.sleep(2)
    print("✅ Conectado a Arduino")
except Exception as e:
    print(f"❌ No se pudo conectar al puerto {puerto}")
    print(f"Error: {e}")
    exit()

if not os.path.exists(nombre_archivo):
    with open(nombre_archivo, mode='w', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(['Fecha', 'Hora', 'Temperatura_C'])

print("📡 Guardando datos...")
while True:
    try:
        linea = arduino.readline().decode('utf-8').strip()
        if linea:
            temperatura = float(linea)
            ahora = datetime.now()
            fecha = ahora.strftime('%Y-%m-%d')
            hora = ahora.strftime('%H:%M:%S')
            print(f"🌡️ {fecha} {hora} → {temperatura} °C")
            with open(nombre_archivo, mode='a', newline='') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow([fecha, hora, temperatura])
    except KeyboardInterrupt:
        print("\n⏹️ Programa terminado")
        break
Script grafico_tiempo_real.py (con mejoras y guardado automático):

python
import serial
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

usuario = "daniela"
ruta_proyecto = f"/Users/{usuario}/Documents/GitHub/SmartLab-AI"
ruta_datos = os.path.join(ruta_proyecto, "Datos")
ruta_graficas = os.path.join(ruta_proyecto, "Gráficas")
os.makedirs(ruta_datos, exist_ok=True)
os.makedirs(ruta_graficas, exist_ok=True)

nombre_archivo_csv = os.path.join(ruta_datos, "temperaturas.csv")
puerto = '/dev/cu.usbmodem14101'

try:
    arduino = serial.Serial(puerto, 9600, timeout=1)
    time.sleep(2)
    print("✅ Conectado a Arduino")
except Exception as e:
    print(f"❌ No se pudo conectar al puerto {puerto}")
    print(f"Error: {e}")
    exit()

tiempos = []
temperaturas = []
tiempo_inicio = time.time()

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlabel('Tiempo (segundos)', fontsize=12)
ax.set_ylabel('Temperatura (°C)', fontsize=12)
ax.set_title('🌡️ Temperatura en tiempo real - BioLab AI', fontsize=14, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_ylim([15, 35])
ax.axhline(y=25, color='red', linestyle=':', linewidth=1, label='Referencia 25°C')
ax.legend(loc='upper right')

ultimo_guardado = time.time()
intervalo_guardado = 60

def actualizar(frame):
    global tiempos, temperaturas, tiempo_inicio, ultimo_guardado
    linea = arduino.readline().decode('utf-8').strip()
    if linea:
        try:
            temperatura = float(linea)
            ahora = datetime.now()
            fecha = ahora.strftime('%Y-%m-%d')
            hora = ahora.strftime('%H:%M:%S')
            print(f"🌡️ {fecha} {hora} → {temperatura} °C")
            with open(nombre_archivo_csv, mode='a', newline='') as archivo:
                escritor = csv.writer(archivo)
                if archivo.tell() == 0:
                    escritor.writerow(['Fecha', 'Hora', 'Temperatura_C'])
                escritor.writerow([fecha, hora, temperatura])
            tiempo_actual = time.time() - tiempo_inicio
            tiempos.append(tiempo_actual)
            temperaturas.append(temperatura)
            if len(tiempos) > 30:
                tiempos.pop(0)
                temperaturas.pop(0)
            ax.clear()
            ax.plot(tiempos, temperaturas, marker='o', linestyle='-', color='#FF6B35', linewidth=2, label='Temperatura')
            ax.set_xlabel('Tiempo (segundos)', fontsize=12)
            ax.set_ylabel('Temperatura (°C)', fontsize=12)
            ax.set_title('🌡️ Temperatura en tiempo real - BioLab AI', fontsize=14, fontweight='bold')
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_ylim([15, 35])
            ax.axhline(y=25, color='red', linestyle=':', linewidth=1, label='Referencia 25°C')
            ax.legend(loc='upper right')
            plt.tight_layout()
            ahora_guardado = time.time()
            if ahora_guardado - ultimo_guardado >= intervalo_guardado:
                timestamp = ahora.strftime('%Y%m%d_%H%M%S')
                nombre_imagen = f'grafico_{timestamp}.png'
                ruta_imagen = os.path.join(ruta_graficas, nombre_imagen)
                fig.savefig(ruta_imagen, dpi=150, bbox_inches='tight')
                print(f"📸 Imagen guardada en: {ruta_imagen}")
                ultimo_guardado = ahora_guardado
        except ValueError:
            pass
        except Exception as e:
            print(f"❌ Error: {e}")

ani = animation.FuncAnimation(fig, actualizar, interval=1000)
plt.show()
arduino.close()
```

Hoy he aprendido que usar rutas absolutas evita problemas de que el script no encuentre las carpetas.
Las carpetas deben tener nombres claros y consistentes (todo en español o todo en inglés, pero sin mezclar).
Guardar imágenes automáticamente es muy útil para documentar la evolución del proyecto.
Un intervalo de 5 segundos es más adecuado para temperatura ambiente que uno de 2 segundos.
La organización del proyecto es tan importante como el código; un proyecto limpio es más fácil de mantener y compartir.

Mañana revisaré todo lo hecho esta semana, prepararé el terreno para la Semana 3 (Machine Learning) y subiré todos los cambios a GitHub con un resumen claro, tardaré bastante poco, pero mejor porque es sábado.

---

## Día 5 (29 de agosto de 2026) 

Hoy es el último día de la Semana 2. El objetivo es:
- Revisar que todo funciona correctamente.
- Organizar los archivos y subirlos a GitHub.
- Hacer un resumen de lo aprendido esta semana.
- Preparar todo para la Semana 3.

Antes de dar por cerrada la semana, he ejecutado todos los scripts para asegurarme de que funcionan:

| Script | Función | Estado |
| :--- | :--- | :--- |
| `leer_arduino.py` | Lee y muestra la temperatura en la terminal |  Funciona |
| `guardar_datos.py` | Guarda los datos en `Datos/temperaturas.csv` |  Funciona |
| `grafico_tiempo_real.py` | Muestra gráfico en tiempo real y guarda imágenes en `Gráficas/` |  Funciona |

Comprobaciones adicionales:
- El código de Arduino está subido y mide cada 5 segundos.
- Las rutas absolutas funcionan correctamente.
- No hay carpetas duplicadas ni archivos sueltos.

Resumen de la Semana 2:

| Día | Logros |
| :---: | :--- |
| Día 1 | Conexión Arduino-Python con `pyserial`. Lectura de datos en la terminal. |
| Día 2 | Guardado de datos en archivo CSV con fecha y hora. |
| Día 3 | Gráfico en tiempo real con `matplotlib`. |
| Día 4 | Mejora del gráfico (colores, título, leyenda). Guardado automático de imágenes cada 60 segundos. Organización definitiva de carpetas con rutas absolutas. |
| Día 5 | Revisión final y preparación para la Semana 3. |

La próxima semana empezaremos a predecir la temperatura utilizando los datos que hemos recogido.
Primero haré una pequeña introducción de "Machine Learning" con `scikit-learn`. Luego prepararé los datos (cargar CSV, limpiar y dividir en entrenamiento/prueba). Entrenaré un modelo de regresión lineal para predecir la temperatura futura. evaluaré el modelo y visualizar las predicciones. E integraré el modelo con el sistema actual y documentar.

Usaré: 
- `pandas` → para manejar los datos.
- `scikit-learn` → para el modelo de Machine Learning.
- `matplotlib` → para visualizar predicciones.

He subido todos los cambios a GitHub con el siguiente mensaje de commit:
```cpp
Semana 2 completada:
- Conexión Arduino-Python con pyserial
- Guardado de datos en CSV
- Gráfico en tiempo real con matplotlib
- Guardado automático de imágenes
- Organización definitiva de carpetas con rutas absolutas
```

Esta semana ha sido especialmente intensa porque he aprendido a conectar Python con Arduino usando pyserial y manejar el puerto serie. Guardar datos en CSV con fecha y hora para llevar un registro histórico. Crear gráficos en tiempo real con matplotlib y actualizarlos automáticamente.
Guardar imágenes automáticamente para documentar el proyecto. Organizar un proyecto de software con carpetas claras y rutas absolutas, evitando duplicados y confusiones.

El proyecto ya tiene una base sólida, sensor funcionando, datos guardados, gráficos visuales y todo bien documentado. La próxima semana será el momento de dar el salto a la inteligencia artificial. El lunes empezaremos la Semana 3 con la instalación de pandas y scikit-learn, y la carga de los datos de temperatura para empezar a entrenar nuestro primer modelo de Machine Learning.
