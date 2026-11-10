# Control de calidad: defectos y porcentaje de calidad.
import configuracion


def tasa_defectos(tasa_base, maquina, tasa_extra):
    # mientras mas gastada la maquina, mas defectos salen
    tasa = tasa_base + ((100 - maquina) / 100) * configuracion.TASA_MAQUINA
    tasa += tasa_extra
    if tasa > configuracion.TASA_MAXIMA:
        tasa = configuracion.TASA_MAXIMA
    return tasa


def unidades_defectuosas(producidos, tasa):
    return round(producidos * tasa)


def porcentaje_calidad(producidos, defectuosos):
    if producidos <= 0:
        return 0.0
    return (producidos - defectuosos) / producidos * 100


def nivel_calidad(calidad):
    if calidad >= configuracion.CALIDAD_OK:
        return "Aceptable"
    elif calidad >= configuracion.CALIDAD_MEDIA:
        return "De atencion"
    else:
        return "Critico"
