
  delay(1000);void setup() {
  Serial.begin(9600);
  Serial.println("¡Termistor conectado! Temperatura aproximada:");
}

void loop() {
  int valor = analogRead(A0);
  float voltaje = valor * (5.0 / 1023.0);
  float temperatura = (voltaje - 0.5) * 10.0;   // ¡Tu ajuste genial!
  
  Serial.print("Valor: ");
  Serial.print(valor);
  Serial.print(" | Voltaje: ");
  Serial.print(voltaje, 3);
  Serial.print("V | Temperatura aprox: ");
  Serial.print(temperatura, 1);
  Serial.println(" °C");
  
}