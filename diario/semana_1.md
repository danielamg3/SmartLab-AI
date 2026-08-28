# Semana 1: Hardware Básico y Primeros Pasos

*Objetivo de la semana:* Conectar el sensor de temperatura DHT11 y mostrar los datos en la pantalla LCD.

---

## Día 1 (5 de agosto de 2026)

He instalado **Python** y el **IDE de Arduino** en mi Mac. He hecho mi primera **calculadora en Python**. Hacía suma, resta, multiplicación, división (con control de división entre 0) y potencia. Aquí está el código:

```cpp
nombre = input("Hola, ¿Cómo te llamas? ")
print(f"Bienvenido a tu primera calculadora {nombre}")

numero1 = float(input("Escribe el primer número: "))
numero2 = float(input("Escribe el segundo número: "))

print("La suma es:", numero1 + numero2)
print("La resta es:", numero1 - numero2)
print("La multiplicación es:", numero1 * numero2)

if numero2 != 0:
    print("La división es:", numero1 / numero2)
else:
    print("No se puede dividir entre 0")

print("La potencia es:", numero1 ** numero2)
```


He pedido ayuda a la IA para definir mi proyecto final: BioLab AI. Será un sistema para monitorear plantas usando inteligencia artificial y Arduino. He entendido cómo funciona un repositorio en GitHub y he organizado mi proyecto en carpetas desde la interfaz web: README.md, diario/, codigo/, datos/, assets/.

Me ha gustado ver que mi primer programa en Python funcionó a la primera. Lo más nuevo para mí ha sido GitHub, entender que es como una "nube" para guardar código y documentación. Estoy contenta porque empiezo con buen pie el proyecto.

El plan para el próximo día es conectar el sensor DHT11 de mi kit Elegoo y leer la temperatura en el Monitor Serie del IDE de Arduino.

---

## Día 2 (16 de agosto de 2026) 

Hoy empecé el día con la intención de conectar el **sensor DHT11** que viene en mi kit Elegoo. Este sensor mide temperatura y humedad, y es muy popular en proyectos de Arduino.

La conexión del DHT11 era correcta:
- VCC → 5V
- GND → GND
- OUT → Pin digital 2

**Código que usé:**
```cpp

#include <DHT.h>

#define DHTPIN 7        // 
#define DHTTYPE DHT11   // Tipo de sensor

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  Serial.println("¡Sensor DHT11 listo!");
}

void loop() {
  // Leer temperatura y humedad
  float temperatura = dht.readTemperature();
  float humedad = dht.readHumidity();

  // Comprobar si la lectura es válida
  if (isnan(temperatura) || isnan(humedad)) {
    Serial.println("Error al leer el sensor");
  } else {
    Serial.print("Temperatura: ");
    Serial.print(temperatura);
    Serial.print("°C | Humedad: ");
    Serial.print(humedad);
    Serial.println("%");
  }

  delay(2000); // Esperar 2 segundos entre lecturas
}
```

El problema era que el Monitor Serie mostraba Error al leer el sensor o T: nan H: nan. El código era correcto, la librería estaba instalada, pero el sensor no respondía.

El sensor DHT11 podría estar dañado (a veces vienen defectuosos de fábrica).Los cables jumper podrían no hacer buen contacto, o el pin digital 2 podría tener algún problema.

Probé a cambiar el pin a 3, revisé las conexiones varias veces, pero el error seguía. Decidí dejar el DHT11 y probar otro sensor. El termistor (NTC)

Mi kit Elegoo incluye un termistor NTC (Negative Temperature Coefficient). Es un componente pequeño con dos patas, parecido a una lágrima negra. Su resistencia cambia con la temperatura: cuando hace más calor, su resistencia disminuye. Este no necesita librerías complejas, solo requiere una lectura analógica (analogRead()) y además es muy fiable y difícil de romper.

Para medir la temperatura con un termistor, usamos un divisor de tensión. El termistor y la resistencia de 10kΩ forman un divisor de tensión. El voltaje en A0 cambia según la resistencia del termistor, que a su vez cambia con la temperatura.

**Primer código que probé:**

```cpp
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
```

El Monitor Serie mostraba valores como 223°C, que es una temperatura imposible para una habitación. La fórmula (voltaje - 0.5) * 100.0 es correcta para el sensor LM35, que da 10mV por grado Celsius. Pero el termistor NO funciona así. La relación entre voltaje y temperatura no es lineal, así que esa fórmula no se puede aplicar directamente.

Lo que hice fue cambiar el valor 100.0 por 10.0 al ver que la temperatura era 10 veces mayor de lo esperado (223°C en lugar de 22°C).0 por 10.0. Este ajuste no es exacto, pero es suficiente para empezar. Más adelante puedo usar la ecuación de Steinhart-Hart para obtener mediciones más precisas, pero por ahora, ver números entre 20-30°C es un gran avance.

Y entonces el Monitor Serie enseñó:

```cpp
Valor: 560 | Voltaje: 2.74V | Temperatura aprox: 22.4 °C
```

¿Qué significan los números que vemos?
-Valor (560): Es la lectura cruda del conversor analógico-digital (ADC). Va de 0 a 1023, donde 0 es 0V y 1023 es 5V.
-Voltaje (2.74V): Es la tensión en el pin A0. Se calcula como valor * (5.0 / 1023.0).
-Temperatura (22.4°C): Es el resultado de nuestra fórmula ajustada. No es exacta, pero nos da una idea de la temperatura ambiente.

Para comprobar que el sensor responde, hice dos pruebas:

-Tocar el termistor con los dedos: La temperatura subió unos grados (el calor de mi mano calienta el sensor).
-Soplar sobre el termistor: La temperatura bajó ligeramente (el aire fresco enfría el sensor).
¡Ambas pruebas funcionaron! Eso significa que el sensor responde a los cambios de temperatura.

Hoy he aprendido que, a veces, cuando no tenemos la fórmula exacta, podemos ajustar un valor hasta que los números tengan sentido. No es perfecto, pero nos permite avanzar. Después de varias horas y muchos errores (DHT11, puerto USB ocupado, fórmulas incorrectas), finalmente hemos conseguido ver una temperatura en el Monitor Serie.

Ahora que tenemos un sensor de temperatura funcionando, el siguiente paso es conectar la pantalla LCD para mostrar los datos sin necesidad del ordenador. También quiero empezar a guardar los datos en un archivo CSV para hacer gráficos con Python.

---
## Día 3 (17 de agosto de 2026) 

Hoy el objetivo era conectar la pantalla LCD para ver la temperatura sin depender del ordenador. Pero antes, tuve que ir a comprar un **potenciómetro de 10kΩ** porque el mío no aparecía por ningún lado (supongo que se perdió en algún proyecto anterior). 

Una vez en casa, me puse a conectar la pantalla. Ya sabía cómo se conectaba porque en clase de tecnología habíamos usado varias veces pantallas LCD, así que no fue ningún misterio. La LCD que tengo es la clásica de 16 pines (sin módulo I2C), así que hay que conectar muchos cables, pero con el esquema que preparé fue rápido.

Este es el código que subí al Arduino. Combina la lectura del termistor con la pantalla LCD.

```cpp
#include <LiquidCrystal.h>  // Librería para controlar la LCD

// Definir los pines de la LCD (RS, E, D4, D5, D6, D7)
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

const int pinTermistor = A0;  // Termistor conectado al pin analógico A0

void setup() {
  // Iniciar la comunicación serie (por si quiero ver datos en el ordenador)
  Serial.begin(9600);
  
  // Iniciar la LCD: 16 columnas, 2 filas
  lcd.begin(16, 2);
  
  // Encender la luz de fondo (por si acaso)
  lcd.backlight();
  
  // Mostrar mensaje de bienvenida en la primera fila
  lcd.setCursor(0, 0);
  lcd.print("BioLab AI");
  
  // Mostrar "Temp:" en la segunda fila
  lcd.setCursor(0, 1);
  lcd.print("Temp: ");
  
  Serial.println("Sistema iniciado");
}

void loop() {
  // 1. Leer el valor analógico del termistor (0 a 1023)
  int valor = analogRead(pinTermistor);
  
  // 2. Convertir ese valor a voltaje (0 a 5V)
  float voltaje = valor * (5.0 / 1023.0);
  
  // 3. Convertir voltaje a temperatura (ajuste empírico)
  //    La fórmula (voltaje - 0.5) * 10.0 es una aproximación
  //    que funciona para este termistor en concreto.
  float temperatura = (voltaje - 0.5) * 10.0;
  
  // 4. Mostrar en el Monitor Serie (para depurar si algo falla)
  Serial.print("Valor: ");
  Serial.print(valor);
  Serial.print(" | Temp: ");
  Serial.print(temperatura, 1);
  Serial.println(" C");
  
  // 5. Mostrar en la LCD
  lcd.setCursor(6, 1);   // Columna 6, fila 1 (después de "Temp: ")
  lcd.print("    ");     // Borrar caracteres anteriores (por si la temperatura baja)
  lcd.setCursor(6, 1);
  lcd.print(temperatura, 1);  // Mostrar con 1 decimal
  lcd.print(" C");
  
  delay(1000);  // Actualizar cada segundo
}
```

Después de cargar el código y comprobar que funcionaba con el ordenador (se veía la temperatura en la LCD y en el Monitor Serie), decidí probar si el sistema funcionaba sin el ordenador, solo con una pila de 9V conectada al Arduino, y funcionó perfectamente. La pantalla se encendió y mostraba la temperatura sin necesidad de USB. Esto es importante porque significa que el proyecto puede ser autónomo y funcionar con baterías. Aprovechando que ya tenía la LCD funcionando, terminé de modificar el archivo README.md. Además, creé la carpeta assets y subí las primeras imágenes.

Un potenciómetro es clave para el contraste, sin él, la pantalla no se veía nada. El proyecto ya es autónomo, al funcionar con pila, puedo llevarlo a cualquier sitio sin depender del ordenador. Ahora cualquiera que vea mi repositorio puede entender mejor el proyecto. 

¡Y así, en solo 3 días, hemos completado la Semana 1! Lo que estaba planeado para 7 días lo he hecho en menos de la mitad. He instalado el entorno, conectado el termistor, ajustado la fórmula, montado la pantalla LCD, organizado el repositorio, subido imágenes y documentado cada paso. El proyecto ya tiene vida propia y funciona de forma autónoma. Ahora toca dar el salto: vamos a conectar Arduino con Python para empezar a guardar datos, hacer gráficos y preparar el terreno para la inteligencia artificial. Semana 2, ¡allá vamos!

