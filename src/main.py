# Proyecto I - Programacion I
# Simulador de la planta de botellones
# main.py solo coordina el flujo general; las reglas estan en los otros modulos.

import configuracion
import validaciones
import simulacion


def nueva_simulacion():
    print("")
    print("¿Desea ejecutar una nueva simulacion?")
    print("1. Si")
    print("2. No")
    return validaciones.pedir_numero("Seleccione una opcion: ", 1, 2) == 1


def main():
    configuracion.inicio()
    continuar = True
    while continuar:
        planta = configuracion.nombre_planta()
        supervisor = configuracion.nombre_supervisor()
        esc = configuracion.pedir_escenario()
        simulacion.ejecutar(planta, supervisor, esc)
        continuar = nueva_simulacion()
    print("")
    print("fin simulacion")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("")
        print("Simulacion interrumpida por el usuario.")
