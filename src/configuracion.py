import validaciones

# capacidad de la planta
CAPACIDAD = 150       # botellones por hora
LITROS = 19           # litros de un botellon
TANQUE = 35000        # litros que caben en el tanque
JORNADAS = 5
ESTADO_MIN = 20       # por debajo de esto la maquina no trabaja

# precios en dolares
PRECIO_AGUA = 0.03
PRECIO_BOTELLON = 6.00
COSTO_HORA = 40.00
COSTO_PERDIDA = 25.00
COSTO_DEFECTO = 1.50
COSTO_MANT = 200.00
HORAS_MANT = 1.5
BONO_MANT = 25
COSTO_REPARACION = 500.00
COSTO_CORRECTIVO = 350.00    # mantenimiento correctivo
HORAS_CORRECTIVO = 3.0
ESTADO_CORRECTIVO = 60       # estado minimo que deja el correctivo

# cosas del proceso
DERRAME = 0.005
RETORNO = 0.85
DESGASTE_CADA = 300          # cada 300 botellones la maquina pierde 1 punto
TASA_MAQUINA = 0.05          # defectos extra si la maquina esta al 0 %
TASA_MAXIMA = 0.25           # tope de defectos (25 %)
COMPRA_MAX_BOTELLONES = 500  # maximo a comprar por jornada
PLAN_MIN_PCT = 80            # el plan no puede ser menor al 80 % de la demanda
PLAN_MAX_PCT = 110           # ni mayor al 110 %

# notas para evaluar
CALIDAD_OK = 95
CALIDAD_MEDIA = 90
CUMPLIMIENTO_OK = 95
CUMPLIMIENTO_MEDIO = 80
EFICIENCIA_OK = 70
EFICIENCIA_MEDIA = 55
DESPERDICIO_OK = 5
DESPERDICIO_ALTO = 10


# ---------- datos de cada escenario ----------
def nombre_escenario(esc):
    if esc == 1:
        return "Produccion estable"
    elif esc == 2:
        return "Alta demanda"
    else:
        return "Produccion critica"


def demanda_escenario(esc):
    if esc == 1:
        return 900
    elif esc == 2:
        return 1100
    else:
        return 750


def horas_escenario(esc):
    if esc == 3:
        return 6.0
    return 8.0


def maquina_escenario(esc):
    if esc == 1:
        return 90
    elif esc == 2:
        return 85
    else:
        return 70


def agua_escenario(esc):
    if esc == 1:
        return 28000.0
    elif esc == 2:
        return 24000.0
    else:
        return 14000.0


def botellones_escenario(esc):
    if esc == 1:
        return 1200
    elif esc == 2:
        return 1000
    else:
        return 600


def tasa_escenario(esc):
    if esc == 1:
        return 0.02
    elif esc == 2:
        return 0.03
    else:
        return 0.05


def rendimiento_escenario(esc):
    if esc == 1:
        return 0.72
    elif esc == 2:
        return 0.70
    else:
        return 0.65


def prob_escenario(esc):
    if esc == 1:
        return 50
    elif esc == 2:
        return 75
    else:
        return 95


# ---------- pantallas de inicio ----------
def inicio():
    print("")
    print("planta de gestion de agua")
    print("--------------------------------------------")
    print("Botellones de agua 19L")
    print("--------------------------------------------")
    print("usted es el supervisor")
    print("se van a realizar 5 jornadas de produccion")
    print("--------------------------------------------")


def nombre_planta():
    return validaciones.pedir_texto("ingrese nombre de la planta: ")


def nombre_supervisor():
    return validaciones.pedir_texto("ingrese nombre del supervisor: ")


def pedir_escenario():
    print("")
    print("------------------------------------------------------")
    print("ESCENARIOS DE PRODUCCION")
    print("------------------------------------------------------")
    print("1) Produccion estable")
    print("   Demanda de", demanda_escenario(1), "botellones por jornada.")
    print("2) Alta demanda")
    print("   Demanda de", demanda_escenario(2), "botellones por jornada.")
    print("3) Produccion critica")
    print("   Solo 6 horas, maquina desgastada y pocos recursos.")
    print("------------------------------------------------------")
    return validaciones.pedir_numero("Seleccione un escenario (1-3): ", 1, 3)
