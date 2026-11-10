# Control de las 5 jornadas. Aqui viven las variables de estado de la planta
# (agua, botellones, maquina, costos, totales) y se les aplica lo que calculan
# los demas modulos.
#
# Fases de cada jornada:
#   Planificacion -> Incidencia -> Decision -> Produccion ->
#   Actualizacion -> Control de calidad -> Reporte
import configuracion
import validaciones
import planificacion
import mantenimiento
import incidencias
import produccion
import calidad
import costos
import reportes


def ejecutar(planta, supervisor, esc):
    # datos del escenario elegido
    nombre_esc = configuracion.nombre_escenario(esc)
    demanda = configuracion.demanda_escenario(esc)
    horas_base = configuracion.horas_escenario(esc)
    maquina = configuracion.maquina_escenario(esc)
    agua = configuracion.agua_escenario(esc)
    botellones = configuracion.botellones_escenario(esc)
    tasa_base = configuracion.tasa_escenario(esc)
    rend = configuracion.rendimiento_escenario(esc)
    prob = configuracion.prob_escenario(esc)

    # totales para el informe final
    tot_plan = 0
    tot_real = 0
    tot_def = 0
    tot_desperdicio = 0.0
    tot_agua = 0.0
    tot_horas = 0.0
    tot_perdidas = 0.0
    tot_programadas = 0.0
    tot_costo = 0.0
    dias_sin_recursos = 0
    ayer = 0

    print("")
    print("======================================================")
    print("INICIO DE LA SIMULACION")
    print("Planta:", planta)
    print("Supervisor:", supervisor)
    print("Escenario:", nombre_esc)
    print("Demanda por jornada:", demanda, "botellones")
    print("======================================================")

    for dia in range(1, configuracion.JORNADAS + 1):
        horas_perdidas = 0.0   # por mantenimiento e incidencias
        costo = 0.0
        tasa_extra = 0.0       # defectos extra por decisiones del dia

        # vuelven los botellones
        if dia > 1:
            retorno = produccion.botellones_retornados(ayer)
            botellones += retorno
            print("")
            print("Retornaron", retorno, "botellones vacios.")

        reportes.panel_inicio(planta, supervisor, nombre_esc, dia, agua,
                              botellones, maquina, horas_base, costo, tot_costo)

        # ========== FASE 1: PLANIFICACION ==========
        # mantenimiento: correctivo obligatorio o preventivo opcional
        if mantenimiento.fuera_de_servicio(maquina):
            print("")
            print("La maquina esta FUERA DE SERVICIO: correctivo obligatorio.")
            print("  costo: $" + str(configuracion.COSTO_CORRECTIVO),
                  "| tiempo:", configuracion.HORAS_CORRECTIVO, "horas")
            maquina = mantenimiento.estado_tras_correctivo(maquina)
            horas_perdidas += configuracion.HORAS_CORRECTIVO
            costo += configuracion.COSTO_CORRECTIVO
        elif mantenimiento.pedir_preventivo(maquina):
            maquina = mantenimiento.estado_tras_preventivo(maquina)
            horas_perdidas += configuracion.HORAS_MANT
            costo += configuracion.COSTO_MANT
            print("Mantenimiento preventivo aplicado.")
        horas = horas_base - horas_perdidas

        # plan de la jornada (entre 80 % y 110 % de la demanda)
        minimo = produccion.plan_minimo(demanda)
        maximo = produccion.plan_maximo(demanda)
        print("")
        print("Demanda de la jornada:", demanda, "botellones")
        plan = validaciones.pedir_numero(
            "Cantidad a producir (" + str(minimo) + " a " + str(maximo) + "): ",
            minimo, maximo)

        # lo que hace falta para el plan
        agua_neces = produccion.agua_necesaria(plan, rend)
        agua_comprar = produccion.agua_a_comprar(agua_neces, agua)
        bot_comprar = produccion.botellones_a_comprar(plan, botellones)
        horas_neces = produccion.horas_necesarias(plan, maquina)
        planificacion.mostrar_plan(plan, agua, agua_neces, agua_comprar,
                                   botellones, bot_comprar, horas, horas_neces,
                                   rend)

        # compras (no se puede pasar del tanque ni de 500 botellones)
        agua_comprar = produccion.limitar_compra_agua(agua_comprar, agua)
        bot_comprar = produccion.limitar_compra_botellones(bot_comprar)
        litros = planificacion.pedir_agua(agua, agua_comprar)
        agua += litros
        costo += costos.costo_agua(litros)
        comprados = planificacion.pedir_botellones(bot_comprar)
        botellones += comprados
        costo += costos.costo_botellones(comprados)

        limite = produccion.limite_produccion(plan, agua, rend, maquina, horas,
                                              botellones)
        print("Produccion maxima con los recursos actuales:", limite, "botellones.")
        if plan > limite:
            print("ADVERTENCIA: el plan de", plan, "supera el limite.")

        # ========== FASE 2 y 3: INCIDENCIA Y DECISION ==========
        if incidencias.sale_incidencia(prob):
            codigo = incidencias.escoger_incidencia()
            incidencias.mostrar_evento(codigo)
            opcion = validaciones.pedir_numero("  Seleccione una opcion (1-3): ", 1, 3)

            # la decision cambia varias variables de la planta
            horas_perdidas += incidencias.efecto_horas(codigo, opcion)
            costo += incidencias.efecto_costo(codigo, opcion)
            maquina = mantenimiento.limitar_estado(
                maquina + incidencias.efecto_estado(codigo, opcion))
            tasa_extra += incidencias.efecto_tasa(codigo, opcion)
            incidencias.mostrar_consecuencias(codigo, opcion)

            horas = horas_base - horas_perdidas
            if horas < 0:
                horas = 0.0
            reportes.panel_estado(plan, 0, agua, botellones, 0.0, horas, 0.0,
                                  horas_perdidas, 0, 100.0, tot_costo + costo,
                                  0.0, maquina)
        else:
            print("")
            print("No se presentaron incidencias en esta jornada.")

        # ========== FASE 4: PRODUCCION ==========
        if mantenimiento.fuera_de_servicio(maquina):
            print("La maquina esta fuera de servicio: no hay produccion.")
            producidos = 0
        else:
            producidos = produccion.limite_produccion(plan, agua, rend, maquina,
                                                      horas, botellones)
        sin_recursos = producidos < plan and produccion.limitado_por_recursos(
            plan, agua, rend, botellones)

        # ========== FASE 5: ACTUALIZACION ==========
        tasa = calidad.tasa_defectos(tasa_base, maquina, tasa_extra)
        agua_usada = produccion.agua_consumida(producidos, rend)
        defectuosos = calidad.unidades_defectuosas(producidos, tasa)
        desperdicio = produccion.desperdicio_litros(producidos, defectuosos)
        horas_usadas = produccion.horas_utilizadas(producidos, maquina, horas)

        agua -= agua_usada
        if agua < 0:
            agua = 0.0
        botellones -= producidos
        if botellones < 0:
            botellones = 0
        maquina = mantenimiento.aplicar_desgaste(maquina, producidos)

        costo += costos.costo_horas_usadas(horas_usadas)
        costo += costos.costo_tiempo_perdido(horas_perdidas)
        costo += costos.costo_defectos(defectuosos)

        # ========== FASE 6: CONTROL DE CALIDAD E INDICADORES ==========
        calidad_pct = calidad.porcentaje_calidad(producidos, defectuosos)
        cumplimiento = produccion.porcentaje(producidos, plan)
        eficiencia = produccion.porcentaje(producidos,
                                           configuracion.CAPACIDAD * horas_base)
        desperdicio_pct = produccion.porcentaje(
            desperdicio, producidos * configuracion.LITROS)
        estado = reportes.estado_jornada(cumplimiento, calidad_pct,
                                         desperdicio_pct, eficiencia, sin_recursos)

        # ========== FASE 7: REPORTE ==========
        reportes.panel_estado(plan, producidos, agua, botellones, desperdicio,
                              horas, horas_usadas, horas_perdidas, defectuosos,
                              calidad_pct, tot_costo + costo, eficiencia, maquina)
        reportes.evaluacion_jornada(dia, cumplimiento, calidad_pct, desperdicio_pct,
                                    eficiencia, agua_usada, estado)

        # sumo para el informe
        tot_plan += plan
        tot_real += producidos
        tot_def += defectuosos
        tot_desperdicio += desperdicio
        tot_agua += agua_usada
        tot_horas += horas_usadas
        tot_perdidas += horas_perdidas
        tot_programadas += horas_base
        tot_costo += costo
        if sin_recursos:
            dias_sin_recursos += 1
        ayer = producidos

        if dia < configuracion.JORNADAS:
            validaciones.pausa()

    # ========== INFORME FINAL ==========
    pendiente = tot_plan - tot_real
    if pendiente < 0:
        pendiente = 0
    cumpl_global = produccion.porcentaje(tot_real, tot_plan)
    calidad_global = calidad.porcentaje_calidad(tot_real, tot_def)
    eficiencia_global = produccion.porcentaje(
        tot_real, configuracion.CAPACIDAD * tot_programadas)
    desperdicio_global = produccion.porcentaje(
        tot_desperdicio, tot_real * configuracion.LITROS)
    final = reportes.resultado(cumpl_global, calidad_global, dias_sin_recursos,
                               tot_real)

    reportes.informe(planta, supervisor, nombre_esc, tot_plan, tot_real, pendiente,
                     tot_def, tot_desperdicio, desperdicio_global, tot_agua,
                     tot_horas, tot_perdidas, calidad_global, eficiencia_global,
                     cumpl_global, tot_costo, final)
