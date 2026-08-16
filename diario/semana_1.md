# Semana 1: Hardware Básico y Primeros Pasos

*Objetivo de la semana:* Conectar el sensor de temperatura DHT11 y mostrar los datos en la pantalla LCD.

---

## Día 1 (5 de agosto de 2026)

**Lo que he hecho hoy:**
- He instalado Python y el IDE de Arduino.
- He ejecutado mi primera calculadora en Python con suma, resta, multiplicación, división y potencia.
- He pedido ayuda a la IA para definir mi proyecto final: **BioLab AI** (un sistema para monitorear plantas con IA y Arduino).
- Entendí cómo funciona un repositorio en GitHub y cómo organizar mi proyecto en carpetas desde la interfaz web.

**Próximo paso (mañana):**
- Conectar el sensor DHT11 de mi kit Elegoo y leer la temperatura en el Monitor Serie del IDE de Arduino.

---

## Día 2 (16 de agosto de 2026) - ¡Por fin tenemos datos!

Hoy empecé el día con la intención de conectar el **sensor DHT11** que viene en mi kit Elegoo. Este sensor mide temperatura y humedad, y es muy popular en proyectos de Arduino.
La conexión del DHT11 era correcta:
- VCC → 5V
- GND → GND
- OUT → Pin digital 2

**Código que usé:**
```cpp
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  Serial.println("¡Sensor DHT11 listo!");
}

void loop() {
  float temperatura = dht.readTemperature();
  float humedad = dht.readHumidity();
  
  if (isnan(temperatura) || isnan(humedad)) {
    Serial.println("Error al leer el sensor");
  } else {
    Serial.print("Temperatura: ");
    Serial.print(temperatura);
    Serial.print("°C | Humedad: ");
    Serial.print(humedad);
    Serial.println("%");
  }
  delay(2000);
}

El problema era que el Monitor Serie mostraba Error al leer el sensor o T: nan H: nan. El código era correcto, la librería estaba instalada, pero el sensor no respondía.

El sensor DHT11 podría estar dañado (a veces vienen defectuosos de fábrica).Los cables jumper podrían no hacer buen contacto, o el pin digital 2 podría tener algún problema.

Probé a cambiar el pin a 3, revisé las conexiones varias veces, pero el error seguía. Decidí dejar el DHT11  y probar otro sensor. El termistor (NTC)

Mi kit Elegoo incluye un termistor NTC (Negative Temperature Coefficient). Es un componente pequeño con dos patas, parecido a una lágrima negra. Su resistencia cambia con la temperatura: cuando hace más calor, su resistencia disminuye.

Este no necesita librerías complejas, solo requiere una lectura analógica (analogRead()) y además es muy fiable y difícil de romper.

Para medir la temperatura con un termistor, usamos un divisor de tensión. El termistor y la resistencia de 10kΩ forman un divisor de tensión. El voltaje en A0 cambia según la resistencia del termistor, que a su vez cambia con la temperatura.

Primer código que probé:

cpp
void setup() {
  Serial.begin(9600);
  Serial.println("Termistor listo!");
}

void loop() {
  int valor = analogRead(A0);
  float voltaje = valor * (5.0 / 1023.0);
  float temperatura = (voltaje - 0.5) * 100.0;  // <-- ¡Aquí estaba el error!
  
  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.println(" °C");
  delay(1000);
}
¿Qué pasó? El Monitor Serie mostraba valores como 223°C, que es una temperatura imposible para una habitación. La fórmula (voltaje - 0.5) * 100.0 es correcta para el sensor LM35, que da 10mV por grado Celsius. Pero el termistor NO funciona así. La relación entre voltaje y temperatura no es lineal, así que esa fórmula no se puede aplicar directamente.

Lo que hice fue cambiar el valor 100.0 por 10.0 al ver que la temperatura era 10 veces mayor de lo esperado (223°C en lugar de 22°C).0 por 10.0. Este ajuste no es exacto, pero es suficiente para empezar. Más adelante puedo usar la ecuación de Steinhart-Hart para obtener mediciones más precisas, pero por ahora, ver números entre 20-30°C es un gran avance.


Y entonces el Monitor Serie mostró:

text
Valor: 560 | Voltaje: 2.74V | Temperatura aprox: 22.4 °C

¿Qué significan los números que vemos?
-Valor (560): Es la lectura cruda del conversor analógico-digital (ADC). Va de 0 a 1023, donde 0 es 0V y 1023 es 5V.
-Voltaje (2.74V): Es la tensión en el pin A0. Se calcula como valor * (5.0 / 1023.0).
-Temperatura (22.4°C): Es el resultado de nuestra fórmula ajustada. No es exacta, pero nos da una idea de la temperatura ambiente.

Para comprobar que el sensor responde, hice dos pruebas:

-Tocar el termistor con los dedos: La temperatura subió unos grados (el calor de mi mano calienta el sensor).
-Soplar sobre el termistor: La temperatura bajó ligeramente (el aire fresco enfría el sensor).
¡Ambas pruebas funcionaron! Eso significa que el sensor responde a los cambios de temperatura.

Hoy he aprendido que, a veces, cuando no tenemos la fórmula exacta, podemos ajustar un valor hasta que los números tengan sentido. No es perfecto, pero nos permite avanzar.
Después de varias horas y muchos errores (DHT11, puerto USB ocupado, fórmulas incorrectas), finalmente hemos conseguido ver una temperatura en el Monitor Serie.

Ahora que tenemos un sensor de temperatura funcionando, el siguiente paso es conectar la pantalla LCD para mostrar los datos sin necesidad del ordenador. También quiero empezar a guardar los datos en un archivo CSV para hacer gráficos con Python.

Archivos guardados hoy

codigo/arduino/termistor_simple.ino - Código final del termistor.
diario/semana_1.md - Esta entrada del diario. 

