# Incidencias: sorteo, textos y EFECTO de cada decision.
# Los numeros de cada opcion estan en las funciones efecto_*; el texto que se
# muestra en pantalla se arma con esos mismos numeros (asi nunca se contradicen).
#
# Incidencias: 1 falla de la llenadora, 2 contaminacion,
#              3 sensor descalibrado, 4 corte electrico.
import random
import configuracion


def sale_incidencia(prob):
    numero = random.randint(1, 100)
    return numero <= prob


def escoger_incidencia():
    return random.randint(1, 4)


def nombre_incidencia(codigo):
    if codigo == 1:
        return "FALLA DE LA LLENADORA"
    elif codigo == 2:
        return "CONTAMINACION MICROBIOLOGICA"
    elif codigo == 3:
        return "SENSOR DE LLENADO DESCALIBRADO"
    else:
        return "CORTE ELECTRICO"


def descripcion_incidencia(codigo):
    if codigo == 1:
        return "La llenadora se detuvo por una averia."
    elif codigo == 2:
        return "El laboratorio detecto un resultado fuera de norma."
    elif codigo == 3:
        return "Los botellones no se llenan con la cantidad exacta."
    else:
        return "Un corte de energia detuvo la linea de llenado."


def nombre_opcion(codigo, opcion):
    if codigo == 1:
        if opcion == 1:
            return "Reparar de inmediato"
        elif opcion == 2:
            return "Continuar produciendo"
        else:
            return "Correctivo programado"
    elif codigo == 2:
        if opcion == 1:
            return "Reprocesar el lote"
        elif opcion == 2:
            return "Descartar el lote"
        else:
            return "Revisar y continuar"
    elif codigo == 3:
        if opcion == 1:
            return "Recalibrar el sensor"
        elif opcion == 2:
            return "Continuar"
        else:
            return "Cambiar el sensor"
    else:
        if opcion == 1:
            return "Usar el generador"
        elif opcion == 2:
            return "Esperar la reparacion"
        else:
            return "Adelantar el preventivo"


# ---------- efectos de cada decision ----------
def efecto_horas(codigo, opcion):
    # horas que se pierden
    if codigo == 1:
        if opcion == 1:
            return 2.0
        elif opcion == 2:
            return 0.0
        else:
            return configuracion.HORAS_CORRECTIVO
    elif codigo == 2:
        if opcion == 1:
            return 1.0
        elif opcion == 2:
            return 0.0
        else:
            return 0.5
    elif codigo == 3:
        if opcion == 1:
            return 1.0
        elif opcion == 2:
            return 0.0
        else:
            return 2.0
    else:
        if opcion == 1:
            return 0.5
        elif opcion == 2:
            return 3.0
        else:
            return 2.0


def efecto_costo(codigo, opcion):
    # dinero que se gasta
    if codigo == 1:
        if opcion == 1:
            return configuracion.COSTO_REPARACION
        elif opcion == 2:
            return 0.0
        else:
            return configuracion.COSTO_CORRECTIVO
    elif codigo == 2:
        if opcion == 1:
            return 150.0
        elif opcion == 2:
            return 200.0
        else:
            return 80.0
    elif codigo == 3:
        if opcion == 1:
            return 100.0
        elif opcion == 2:
            return 0.0
        else:
            return 250.0
    else:
        if opcion == 1:
            return 180.0
        elif opcion == 2:
            return 0.0
        else:
            return 200.0


def efecto_estado(codigo, opcion):
    # puntos que gana (+) o pierde (-) la maquina
    if codigo == 1:
        if opcion == 1:
            return 40
        elif opcion == 2:
            return -10
        else:
            return 25
    elif codigo == 3:
        if opcion == 3:
            return 10
        return 0
    elif codigo == 4:
        if opcion == 1:
            return -3
        elif opcion == 3:
            return 15
        return 0
    return 0


def efecto_tasa(codigo, opcion):
    # defectos extra (0.05 = 5 %)
    if codigo == 1:
        if opcion == 2:
            return 0.05
        return 0.0
    elif codigo == 2:
        if opcion == 1:
            return 0.01
        elif opcion == 2:
            return 0.06
        else:
            return 0.03
    elif codigo == 3:
        if opcion == 2:
            return 0.06
        return 0.0
    return 0.0


# ---------- textos ----------
def numero(valor):
    # 2.0 se muestra como 2 y 0.5 como 0.5
    if valor == int(valor):
        return str(int(valor))
    return str(valor)


def unir(texto, nuevo):
    if texto == "":
        return nuevo
    return texto + ", " + nuevo


def resumen_efectos(codigo, opcion):
    texto = ""
    horas = efecto_horas(codigo, opcion)
    costo = efecto_costo(codigo, opcion)
    estado = efecto_estado(codigo, opcion)
    tasa = efecto_tasa(codigo, opcion)
    if horas != 0:
        texto = unir(texto, "-" + numero(horas) + " h")
    if costo != 0:
        texto = unir(texto, "-$" + numero(costo))
    if estado > 0:
        texto = unir(texto, "+" + str(estado) + " estado")
    elif estado < 0:
        texto = unir(texto, str(estado) + " estado")
    if tasa != 0:
        texto = unir(texto, "+" + numero(round(tasa * 100)) + " % defectos")
    return texto


def mostrar_evento(codigo):
    print("")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("  INCIDENCIA:", nombre_incidencia(codigo))
    print(" ", descripcion_incidencia(codigo))
    print("  1)", nombre_opcion(codigo, 1) + ":", resumen_efectos(codigo, 1))
    print("  2)", nombre_opcion(codigo, 2) + ":", resumen_efectos(codigo, 2))
    print("  3)", nombre_opcion(codigo, 3) + ":", resumen_efectos(codigo, 3))
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


def mostrar_consecuencias(codigo, opcion):
    print("")
    print("Decision tomada:", nombre_opcion(codigo, opcion))
    print("Consecuencias:", resumen_efectos(codigo, opcion))
