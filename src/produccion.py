# Reglas matematicas de la produccion (agua, botellones, horas, maquina).
import configuracion


def porcentaje(parte, total):
    if total <= 0:
        return 0.0
    return parte / total * 100


def capacidad_por_hora(maquina):
    # botellones por hora segun el estado de la maquina
    return configuracion.CAPACIDAD * maquina / 100


# ---------- plan de la jornada ----------
def plan_minimo(demanda):
    return int(demanda * configuracion.PLAN_MIN_PCT / 100)


def plan_maximo(demanda):
    return int(demanda * configuracion.PLAN_MAX_PCT / 100)


def agua_necesaria(plan, rend):
    # litros de agua cruda para llenar 'plan' botellones
    return plan * configuracion.LITROS / rend


def agua_a_comprar(agua_neces, agua):
    faltante = agua_neces - agua
    if faltante <= 0:
        return 0
    return int(faltante) + 1


def botellones_a_comprar(plan, botellones):
    faltante = plan - botellones
    if faltante < 0:
        return 0
    return faltante


def horas_necesarias(plan, maquina):
    return plan / capacidad_por_hora(maquina)


def espacio_tanque(agua):
    espacio = int(configuracion.TANQUE - agua)
    if espacio < 0:
        return 0
    return espacio


def limitar_compra_agua(agua_comprar, agua):
    espacio = espacio_tanque(agua)
    if agua_comprar > espacio:
        return espacio
    return agua_comprar


def limitar_compra_botellones(bot_comprar):
    if bot_comprar > configuracion.COMPRA_MAX_BOTELLONES:
        return configuracion.COMPRA_MAX_BOTELLONES
    return bot_comprar


# ---------- limites de produccion ----------
def max_por_agua(agua, rend):
    return int(agua * rend // configuracion.LITROS)


def max_por_maquina(maquina, horas):
    return int(capacidad_por_hora(maquina) * horas)


def limite_produccion(plan, agua, rend, maquina, horas, botellones):
    # se produce lo menor entre: el plan, el agua, la maquina y los botellones
    limite = plan
    if limite > max_por_agua(agua, rend):
        limite = max_por_agua(agua, rend)
    if limite > max_por_maquina(maquina, horas):
        limite = max_por_maquina(maquina, horas)
    if limite > botellones:
        limite = botellones
    if limite < 0:
        limite = 0
    return limite


def limitado_por_recursos(plan, agua, rend, botellones):
    # True si el agua o los botellones no alcanzan para el plan
    return max_por_agua(agua, rend) < plan or botellones < plan


# ---------- calculos del dia ----------
def agua_consumida(producidos, rend):
    return producidos * configuracion.LITROS / rend


def desperdicio_litros(producidos, defectuosos):
    # los defectuosos se pierden completos + un pequeno derrame
    desperdicio = defectuosos * configuracion.LITROS
    desperdicio += producidos * configuracion.LITROS * configuracion.DERRAME
    return desperdicio


def horas_utilizadas(producidos, maquina, horas):
    usadas = producidos / capacidad_por_hora(maquina)
    if usadas > horas:
        usadas = horas
    return usadas


def botellones_retornados(ayer):
    # el 85 % de lo producido ayer vuelve vacio
    return int(ayer * configuracion.RETORNO)
