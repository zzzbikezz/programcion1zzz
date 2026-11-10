# Reglas para calcular los costos de la operacion (en dolares).
import configuracion


def costo_agua(litros):
    return litros * configuracion.PRECIO_AGUA


def costo_botellones(cantidad):
    return cantidad * configuracion.PRECIO_BOTELLON


def costo_horas_usadas(horas):
    return horas * configuracion.COSTO_HORA


def costo_tiempo_perdido(horas):
    return horas * configuracion.COSTO_PERDIDA


def costo_defectos(defectuosos):
    return defectuosos * configuracion.COSTO_DEFECTO
