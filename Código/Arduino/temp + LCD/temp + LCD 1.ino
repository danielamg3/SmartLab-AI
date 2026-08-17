#include <LiquidCrystal.h>

// Definir los pines de la LCD (cambia estos números si los has conectado diferente)
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);  // RS, E, D4, D5, D6, D7

const int pinTermistor = A0;  // Termistor en A0

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("BioLab AI");
  lcd.setCursor(0, 1);
  lcd.print("Temp: ");
  Serial.println("Sistema iniciado");
}

void loop() {
  // Leer termistor
  int valor = analogRead(pinTermistor);
  float voltaje = valor * (5.0 / 1023.0);
  float temperatura = (voltaje - 0.5) * 10.0;  // Ajuste empírico

  // Mostrar en Monitor Serie (para depuración)
  Serial.print("Valor: ");
  Serial.print(valor);
  Serial.print(" | Temp: ");
  Serial.print(temperatura, 1);
  Serial.println(" C");

  // Mostrar en LCD
  lcd.setCursor(6, 1);   // Columna 6, fila 1 (después de "Temp: ")
  lcd.print("    ");     // Borrar caracteres anteriores
  lcd.setCursor(6, 1);
  lcd.print(temperatura, 1);
  lcd.print(" C");

  delay(1000);
}