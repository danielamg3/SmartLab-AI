# Semana 2: Puente Arduino-Python

*Objetivo de la semana:* Conectar Arduino con Python para leer datos de temperatura, guardarlos en un archivo CSV y hacer gráficos.

---

## Día 1 (24 de agosto de 2026) - Primeros datos en Python (¡por fin!)

### 🎯 Objetivo del día

Conseguir que Python leyera los datos de temperatura que envía Arduino a través del puerto USB, y mostrarlos en la terminal.

---

### 🔧 Preparación del código de Arduino

Lo primero fue modificar el código de Arduino para que **solo enviara el número de temperatura**, sin texto extra. Así Python podría leerlo fácilmente.

**Código de Arduino (parte del `loop()`):**

```cpp
Serial.println(temperatura, 1);
El resto del código (LCD y lectura del termistor) se mantuvo igual.

🐍 El script de Python: primeros intentos (y fallos)

Escribí un script en Python usando la librería pyserial para leer el puerto serie. Pero al ejecutarlo, me encontré con varios problemas.

Problema 1: El archivo estaba vacío

Al ejecutar python3 leer_arduino.py, el error era:

text
can't find '__main__' module in '.../leer_arduino.py'
Causa: El archivo leer_arduino.py estaba vacío o no contenía código válido.

Solución: Abrí el archivo con el editor nano en la terminal y pegué el código completo. Luego lo guardé correctamente con Ctrl + O → Enter → Ctrl + X.

Problema 2: El puerto estaba ocupado

Después de arreglar el archivo, al ejecutar el script aparecía:

text
❌ No se pudo conectar al puerto /dev/cu.usbmodem14101
Error: [Errno 16] Resource busy
Causa: El Monitor Serie del IDE de Arduino estaba abierto, y ocupa el puerto USB.

Solución: Cerré el Monitor Serie (el botón de la lupa sin el recuadro azul) y ejecuté el script de nuevo.

Problema 3: El nombre del puerto en el script no coincidía

En el script, el puerto estaba escrito como:

python
puerto = '/dev/cu.usbmodem14101'
Pero a veces el puerto cambia. Para asegurarme, fui al IDE de Arduino → Herramientas → Puerto y copié el nombre exacto que aparecía. Lo pegué en el script entre comillas.

✅ ¡Funcionó!

Después de corregir todo, ejecuté el script y, por fin, vi en la terminal:

text
✅ Conectado a Arduino
📡 Leyendo datos de temperatura... (presiona Ctrl+C para salir)
🌡️ Temperatura: 22.4 °C
🌡️ Temperatura: 22.5 °C
🌡️ Temperatura: 22.3 °C
...
¡Ya tengo datos de temperatura en Python! Esto abre la puerta a guardarlos en un archivo, hacer gráficos y, más adelante, usar inteligencia artificial.

📝 Código final de leer_arduino.py

python
import serial
import time

# Cambia esto por el puerto que uses
# Para saber el puerto: en el IDE de Arduino -> Herramientas -> Puerto
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
📚 Lecciones aprendidas hoy

El puerto USB solo puede ser usado por un programa a la vez. Si el Monitor Serie del IDE de Arduino está abierto, Python no puede conectarse.
El nombre del puerto debe ser exacto y llevar comillas en el script de Python.
Los archivos de Python necesitan el código completo para ejecutarse. Si el archivo está vacío, Python no encuentra el __main__.
El editor nano en la terminal es útil, pero hay que recordar guardar con Ctrl + O y salir con Ctrl + X.
🚀 Próximo paso (Día 2)

Mañana, guardaré estos datos en un archivo CSV para poder hacer gráficos con Python. ¡El proyecto empieza a tomar forma!

text

---

### ✅ ¿Qué incluye esta entrada?

- El **objetivo del día**.
- Los **problemas** encontrados (archivo vacío, puerto ocupado, nombre del puerto incorrecto).
- Las **soluciones** aplicadas.
- El **código final** de Python.
- Una **captura simulada** de la salida correcta.
- Los **aprendizajes**.
- El **próximo paso**.

---

### 📝 Cómo añadirlo a tu diario

1. Abre `diario/semana_2.md` en tu editor.
2. Si ya tenías algo escrito para el Día 1, reemplázalo con esta entrada.
3. Si el archivo estaba vacío, pega todo el contenido.
4. Guarda y sube a GitHub con Commit + Push.

---

**¡Enhorabuena!** Has superado una de las partes más técnicas del proyecto. Mañana, a guardar datos en CSV. 🌡️🐍📊
