# Planificacion de la jornada: compras y verificacion de que el plan sea viable.
import configuracion
import validaciones
import produccion


def pedir_agua(agua_actual, recomendado):
    # cuanto espacio queda en el tanque
    espacio = int(configuracion.TANQUE - agua_actual)
    print("")
    if espacio <= 0:
        print("  el tanque esta lleno")
        return 0.0
    print("  precio del agua: $" + str(configuracion.PRECIO_AGUA) + " el litro")
    print("  espacio en el tanque:", espacio, "L")
    print("  recomendado comprar:", recomendado, "L")
    return float(validaciones.pedir_numero("  Litros a comprar: ", 0, espacio))


def pedir_botellones(recomendado):
    print("")
    print("  precio del botellon vacio: $" + str(configuracion.PRECIO_BOTELLON))
    print("  recomendado comprar:", recomendado, "botellones")
    return validaciones.pedir_numero("  Botellones a comprar: ", 0,
                                     configuracion.COMPRA_MAX_BOTELLONES)


def mostrar_plan(plan, agua, agua_neces, agua_comprar, botellones, bot_comprar,
                 horas, horas_neces, rend):
    # muestra lo que tiene y lo que necesita, y avisa si el plan no es viable
    print("")
    print("PLANIFICACION DE LA JORNADA")
    print("Cantidad a producir:", plan, "botellones")
    print("Agua: tiene", round(agua), "L | necesita", round(agua_neces),
          "L | recomendado comprar", agua_comprar, "L")
    print("Botellones: tiene", botellones, "| necesita", plan,
          "| recomendado comprar", bot_comprar)
    print("Horas: tiene", round(horas, 1), "h | necesita",
          round(horas_neces, 1), "h")

    if horas_neces > horas:
        print("ADVERTENCIA: faltan", round(horas_neces - horas, 1),
              "horas. El plan se vera limitado.")
    if agua_comprar > produccion.espacio_tanque(agua):
        print("ADVERTENCIA: el tanque no alcanza para todo el plan.")
        print("Plan maximo con el tanque lleno:",
              produccion.max_por_agua(configuracion.TANQUE, rend), "botellones")
    if bot_comprar > configuracion.COMPRA_MAX_BOTELLONES:
        print("ADVERTENCIA: solo puede comprar",
              configuracion.COMPRA_MAX_BOTELLONES, "botellones por jornada.")
