nombre = input("Hola, ¿Cómo te llamas? ")
print(f"🎮 Bienvenido a tu primera calculadora {nombre}")

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