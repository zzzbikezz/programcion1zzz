# Todo lo que se muestra como reporte: paneles, evaluacion e informe final.
import configuracion
import mantenimiento


def panel_inicio(planta, supervisor, esc, dia, agua, botellones, maquina, horas,
                 costo, total):
    print("")
    print("======================================================")
    print("PLANTA:", planta)
    print("SUPERVISOR:", supervisor)
    print("ESCENARIO:", esc)
    print("JORNADA", dia, "DE", configuracion.JORNADAS)
    print("------------------------------------------------------")
    print("Agua cruda:", round(agua), "L")
    print("Botellones vacios:", botellones)
    print("Estado de la maquina:", maquina, "%")
    print("Horas disponibles:", round(horas, 1))
    print("Costo de la jornada: $" + str(round(costo, 2)))
    print("Costo acumulado: $" + str(round(total, 2)))
    print("======================================================")


def panel_estado(plan, realizada, agua, botellones, desperdicio, horas_disp,
                 horas_usadas, horas_perdidas, defectuosos, calidad, costo_total,
                 eficiencia, maquina):
    # panel "ESTADO DE LA PLANTA" (se muestra tras cada decision y cada jornada)
    print("")
    print("========================================")
    print("        ESTADO DE LA PLANTA")
    print("========================================")
    print("Produccion planificada:", plan, "botellones")
    print("Produccion realizada:  ", realizada, "botellones")
    print("Produccion pendiente:  ", plan - realizada, "botellones")
    print("")
    print("Agua cruda:            ", round(agua), "L")
    print("Botellones vacios:     ", botellones)
    print("Desperdicio:           ", round(desperdicio), "L")
    print("")
    print("Horas disponibles:     ", round(horas_disp, 1))
    print("Horas utilizadas:      ", round(horas_usadas, 1))
    print("Horas perdidas:        ", round(horas_perdidas, 1))
    print("")
    print("Productos defectuosos: ", defectuosos)
    print("Calidad:               ", round(calidad, 1), "%")
    print("")
    print("Costo acumulado:        $" + str(round(costo_total, 2)))
    print("Eficiencia:            ", round(eficiencia, 1), "%")
    print("")
    print("Estado de la planta:   ", mantenimiento.clasificar_estado(maquina),
          "(" + str(maquina) + " %)")
    print("========================================")


def estado_jornada(cumplimiento, calidad, desperdicio_pct, eficiencia, sin_recursos):
    # el primer if que se cumple decide el estado (el orden importa)
    if sin_recursos:
        return "RECURSOS INSUFICIENTES (agua o botellones no alcanzaron)"
    elif cumplimiento < configuracion.CUMPLIMIENTO_MEDIO:
        return "JORNADA NO CUMPLIDA (produccion insuficiente)"
    elif calidad < configuracion.CALIDAD_MEDIA:
        return "JORNADA NO CUMPLIDA (calidad critica)"
    elif desperdicio_pct > configuracion.DESPERDICIO_ALTO:
        return "JORNADA NO CUMPLIDA (desperdicio excesivo)"
    elif eficiencia < configuracion.EFICIENCIA_MEDIA:
        return "JORNADA NO CUMPLIDA (eficiencia baja)"
    elif cumplimiento < configuracion.CUMPLIMIENTO_OK:
        return "JORNADA EN RIESGO (cumplimiento parcial)"
    elif calidad < configuracion.CALIDAD_OK:
        return "JORNADA EN RIESGO (calidad en atencion)"
    elif desperdicio_pct > configuracion.DESPERDICIO_OK:
        return "JORNADA EN RIESGO (desperdicio elevado)"
    elif eficiencia < configuracion.EFICIENCIA_OK:
        return "JORNADA EN RIESGO (eficiencia media)"
    else:
        return "JORNADA SUPERADA"


def evaluacion_jornada(dia, cumplimiento, calidad, desperdicio_pct, eficiencia,
                       agua_usada, estado):
    print("")
    print("------------------------------------------------------")
    print("EVALUACION DE LA JORNADA", dia)
    print("------------------------------------------------------")
    print("Agua cruda consumida:", round(agua_usada), "L")
    print("Cumplimiento:", round(cumplimiento, 1), "%")
    print("Calidad:", round(calidad, 1), "%")
    print("Desperdicio:", round(desperdicio_pct, 1), "%")
    print("Eficiencia:", round(eficiencia, 1), "%")
    print("------------------------------------------------------")
    print("ESTADO:", estado)
    print("------------------------------------------------------")


def resultado(cumplimiento, calidad, dias_sin_recursos, tot_real):
    # resultado general de la planta (el orden de los if importa)
    if tot_real <= 0:
        return "PLAN DE PRODUCCION NO CUMPLIDO"
    if calidad < configuracion.CALIDAD_MEDIA:
        return "RESULTADO CRITICO POR CALIDAD"
    if dias_sin_recursos >= 2:
        return "RESULTADO CRITICO POR FALTA DE RECURSOS"
    if cumplimiento >= configuracion.CUMPLIMIENTO_OK:
        if calidad >= configuracion.CALIDAD_OK:
            return "PLAN DE PRODUCCION CUMPLIDO"
    if cumplimiento >= configuracion.CUMPLIMIENTO_MEDIO:
        return "CUMPLIMIENTO PARCIAL DEL PLAN"
    return "PLAN DE PRODUCCION NO CUMPLIDO"


def informe(planta, supervisor, esc, tot_plan, tot_real, pendiente,
            tot_def, tot_desperdicio, desperdicio_pct,
            tot_agua, tot_horas, tot_perdidas,
            calidad, eficiencia, cumplimiento, tot_costo, final):
    print("")
    print("======================================================")
    print("INFORME FINAL DE LA SIMULACION")
    print("======================================================")
    print("Planta:", planta)
    print("Supervisor:", supervisor)
    print("Escenario:", esc)
    print("------------------------------------------------------")
    print("Produccion total planificada:", tot_plan, "botellones")
    print("Produccion total realizada:", tot_real, "botellones")
    print("Produccion pendiente:", pendiente, "botellones")
    print("Total de defectuosos:", tot_def, "botellones")
    print("Desperdicio acumulado:", round(tot_desperdicio), "L ("
          + str(round(desperdicio_pct, 1)) + " %)")
    print("Agua cruda consumida:", round(tot_agua), "L")
    print("Horas utilizadas:", round(tot_horas, 1))
    print("Horas perdidas:", round(tot_perdidas, 1))
    print("Cumplimiento global:", round(cumplimiento, 1), "%")
    print("Calidad final:", round(calidad, 1), "%")
    print("Eficiencia final:", round(eficiencia, 1), "%")
    print("Costo acumulado: $" + str(round(tot_costo, 2)))
    print("------------------------------------------------------")
    print("RESULTADO:", final)
    print("======================================================")
