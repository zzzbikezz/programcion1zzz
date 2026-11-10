# Simulador de Gestión y Control de una Planta de Producción — Planta de agua (botellones de 19 L)

Proyecto I de Programación I (UNIMAR). Aplicación de línea de comandos en Python que simula
**5 jornadas** de una planta que llena botellones de agua. El usuario es el supervisor:
planifica la producción, compra agua y botellones, decide sobre el mantenimiento y resuelve
incidencias. Cada decisión cambia variables de la planta y el resultado final depende de ellas.

No se usan listas, tuplas, diccionarios, conjuntos, clases, archivos ni librerías externas
(solo `random` de la biblioteca estándar para sortear incidencias).

## Integrantes y responsabilidades
| Integrante | Módulos |
|---|---|
| Jonas | `main.py`, `configuracion.py`, `validaciones.py` |
| Leonardo | `simulacion.py` |
| Rafael | `produccion.py`, `planificacion.py`, `mantenimiento.py` |
| Bill | `incidencias.py` |
| Jesenia | `reportes.py`, `calidad.py`, `costos.py` |

## Cómo ejecutar
```
cd src
python main.py
```

## Módulos y responsabilidades
| Módulo | Responsabilidad |
|---|---|
| `main.py` | Coordina el flujo general: presentación, datos iniciales, simulación y reinicio |
| `configuracion.py` | Constantes, datos de cada escenario y pantallas de inicio |
| `validaciones.py` | Lectura y validación de datos (`while` + `try-except`) |
| `simulacion.py` | Controla las 5 jornadas y guarda las variables de estado |
| `planificacion.py` | Compras de agua y botellones y verificación de que el plan sea viable |
| `produccion.py` | Reglas matemáticas: límites, consumo de agua, horas y desperdicio |
| `mantenimiento.py` | Estado de la máquina: preventivo, correctivo y desgaste |
| `incidencias.py` | Sorteo de incidencias, alternativas y efecto de cada decisión |
| `calidad.py` | Tasa de defectos, defectuosos y nivel de calidad |
| `costos.py` | Reglas de costo |
| `reportes.py` | Paneles, evaluación de cada jornada e informe final |

## Flujo de cada jornada
Planificación → Incidencia → Decisión → Producción → Actualización → Control de calidad → Reporte.
(La incidencia se resuelve antes de producir para que la decisión afecte la producción del día.)

## Escenarios
| | Demanda | Horas | Máquina | Agua (L) | Botellones | Defectos base | Rendimiento | Prob. incidencia |
|---|---|---|---|---|---|---|---|---|
| 1 Producción estable | 900 | 8 | 90 % | 28000 | 1200 | 2 % | 0.72 | 50 % |
| 2 Alta demanda | 1100 | 8 | 85 % | 24000 | 1000 | 3 % | 0.70 | 75 % |
| 3 Producción crítica | 750 | 6 | 70 % | 14000 | 600 | 5 % | 0.65 | 95 % |

El *rendimiento* es la fracción del agua cruda que termina en producto (el resto se pierde en el proceso).

## Reglas de la simulación
- El plan de cada jornada debe estar entre el **80 % y el 110 %** de la demanda.
- Capacidad por hora = 150 × (estado de la máquina / 100).
- Agua necesaria = plan × 19 / rendimiento.
- **Producción real = mínimo entre**: plan, agua disponible (× rendimiento / 19), capacidad de la máquina × horas disponibles, y botellones vacíos disponibles.
- Si la máquina está por debajo de 20 % está fuera de servicio: no produce.
- Compras: agua a $0.03/L (hasta llenar el tanque de 35000 L) y botellones a $6 (máximo 500 por jornada).
- Al día siguiente vuelve el 85 % de los botellones producidos, vacíos.
- Desgaste: la máquina pierde 1 punto por cada 300 botellones producidos.

### Mantenimiento
| Tipo | Cuándo | Tiempo | Costo | Efecto |
|---|---|---|---|---|
| Preventivo | Opcional, al planificar | 1.5 h | $200 | +25 de estado |
| Correctivo | Obligatorio si el estado < 20 | 3 h | $350 | El estado queda al menos en 60 |

### Incidencias (3 alternativas cada una; todas modifican variables)
1. Falla de la llenadora · 2. Contaminación microbiológica · 3. Sensor de llenado descalibrado · 4. Corte eléctrico.
Los efectos (horas, costo, estado de la máquina y defectos extra) están definidos en `incidencias.py`
y el texto que ve el usuario se genera a partir de esos mismos valores.

## Fórmulas e indicadores
- **Tasa de defectos** = defectos base + (100 − estado)/100 × 5 % + defectos extra de decisiones (tope 25 %)
- **Defectuosos** = producidos × tasa (redondeado)
- **Calidad (%)** = (producidos − defectuosos) / producidos × 100
- **Cumplimiento (%)** = producidos / planificados × 100
- **Eficiencia (%)** = producidos / (150 × horas base de la jornada) × 100
- **Desperdicio (L)** = defectuosos × 19 + producidos × 19 × 0.5 % (derrame)
- **Desperdicio (%)** = desperdicio / (producidos × 19) × 100
- **Horas utilizadas** = producidos / capacidad por hora
- **Horas perdidas** = horas de mantenimiento + horas perdidas por incidencias
- **Costo** = agua + botellones comprados + horas usadas × $40 + horas perdidas × $25 + defectuosos × $1.50 + mantenimiento + costo de las decisiones

### Niveles
- Calidad: ≥ 95 Aceptable · 90–94.9 De atención · < 90 Crítico
- Estado de la jornada (el primer caso que se cumple): recursos insuficientes → cumplimiento < 80 / calidad < 90 / desperdicio > 10 / eficiencia < 55 (jornada no cumplida) → cumplimiento < 95 / calidad < 95 / desperdicio > 5 / eficiencia < 70 (en riesgo) → jornada superada.

### Resultado final
1. Sin producción o cumplimiento bajo → plan no cumplido
2. Calidad final < 90 % → crítico por calidad
3. 2 o más jornadas sin recursos → crítico por falta de recursos
4. Cumplimiento ≥ 95 % y calidad ≥ 95 % → plan cumplido
5. Cumplimiento ≥ 80 % → cumplimiento parcial
6. Cualquier otro caso → plan no cumplido
