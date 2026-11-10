def pedir_numero(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje))
            if valor < minimo or valor > maximo:
                print("  Error: debe escribir un numero entre", minimo, "y", maximo)
                continue
            return valor
        except ValueError:
            print("  Error: debe escribir un numero entero.")


def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if len(texto) >= 3:
            return texto
        print("  Error: debe escribir al menos 3 caracteres.")


def preguntar(mensaje):
    while True:
        respuesta = input(mensaje + " (S/N): ").strip().lower()
        if respuesta == "s" or respuesta == "si" or respuesta == "sí":
            return True
        if respuesta == "n" or respuesta == "no":
            return False
        print("  Error: responda S para si o N para no.")


def pausa():
    input("\nPresione ENTER para continuar...")
