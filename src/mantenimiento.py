# Estado de la maquina: preventivo, correctivo y desgaste.
import configuracion
import validaciones


def clasificar_estado(maquina):
    if maquina >= 80:
        return "Optimo"
    elif maquina >= 50:
        return "Regular"
    elif maquina >= configuracion.ESTADO_MIN:
        return "Deteriorada"
    else:
        return "Fuera de servicio"


def limitar_estado(maquina):
    if maquina > 100:
        return 100
    if maquina < 1:
        return 1
    return maquina


def fuera_de_servicio(maquina):
    return maquina < configuracion.ESTADO_MIN


def pedir_preventivo(maquina):
    print("")
    print("------------------------------------------------------")
    print("MANTENIMIENTO PREVENTIVO")
    print("  estado de la maquina:", maquina, "%")
    if maquina < 60:
        print("  ojo: la maquina esta muy desgastada")
    print("  costo: $" + str(configuracion.COSTO_MANT))
    print("  tiempo:", configuracion.HORAS_MANT, "horas")
    print("  recupera:", configuracion.BONO_MANT, "puntos de estado")
    print("------------------------------------------------------")
    return validaciones.preguntar("  ¿Desea realizar el mantenimiento?")


def estado_tras_preventivo(maquina):
    return limitar_estado(maquina + configuracion.BONO_MANT)


def estado_tras_correctivo(maquina):
    # el correctivo deja la maquina al menos en ESTADO_CORRECTIVO
    if maquina < configuracion.ESTADO_CORRECTIVO:
        return configuracion.ESTADO_CORRECTIVO
    return maquina


def aplicar_desgaste(maquina, producidos):
    return limitar_estado(maquina - int(producidos / configuracion.DESGASTE_CADA))
