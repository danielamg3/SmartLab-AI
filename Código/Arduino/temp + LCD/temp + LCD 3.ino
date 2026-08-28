#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
const int pinTermistor = A0;

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("BioLab AI");
  lcd.setCursor(0, 1);
  lcd.print("Temp: ");
}

void loop() {
  int valor = analogRead(pinTermistor);
  float voltaje = valor * (5.0 / 1023.0);
  float temperatura = (voltaje - 0.5) * 10.0;
  
  // Mostrar en LCD
  lcd.setCursor(6, 1);
  lcd.print("    ");
  lcd.setCursor(6, 1);
  lcd.print(temperatura, 1);
  lcd.print(" C");
  
  // Enviar SOLO el número por el puerto serie
  Serial.println(temperatura, 1);
  
  delay(1000);
}