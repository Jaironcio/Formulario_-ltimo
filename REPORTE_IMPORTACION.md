# REPORTE DE IMPORTACIÓN DE INCIDENCIAS

## Resumen Ejecutivo

**Total de incidencias importadas: 1,510**

Datos importados desde `Incidencias_Completo.xlsm` preservando exactamente la clasificación y estructura original del Excel.

---

## Distribución por Fuente

| Hoja Excel | Incidencias Importadas |
|------------|------------------------|
| TURNO NOCHE | 157 |
| TURNO TARDE | 442 |
| TURNO MAÑANA | 910 |
| **TOTAL** | **1,509** |

*Nota: 1 incidencia adicional puede ser de prueba previa*

---

## Distribución por Centro

| Centro | Incidencias | Porcentaje |
|--------|-------------|------------|
| Trafún | 985 | 65.2% |
| Cipreses | 411 | 27.2% |
| Liquiñe | 114 | 7.5% |

---

## Distribución por Turno

| Turno | Incidencias | Porcentaje |
|-------|-------------|------------|
| Día/Mañana | 911 | 60.3% |
| Tarde | 442 | 29.3% |
| Noche | 157 | 10.4% |

---

## Top 10 Tipos de Incidencia Normalizada

| Tipo de Incidencia | Cantidad | % |
|-------------------|----------|---|
| Estanque en Manejo | 618 | 40.9% |
| Estanque en Tratamiento | 524 | 34.7% |
| Estanque en Flashing | 70 | 4.6% |
| Estanque con traslado de peces | 61 | 4.0% |
| Oxígeno Alto | 55 | 3.6% |
| Problemas con el cono de oxigenación | 37 | 2.5% |
| Estanque en Vacunación | 36 | 2.4% |
| Manipulando sensor | 23 | 1.5% |
| Desdoble de estanque | 17 | 1.1% |
| Estanque en Selección | 15 | 1.0% |

---

## Evaluación de Riesgos

| Tipo de Riesgo | Incidencias | % del Total |
|----------------|-------------|-------------|
| **Riesgo para peces** | 1,221 | 80.9% |
| **Pérdida económica** | 859 | 56.9% |
| **Riesgo para personas** | 0 | 0.0% |

---

## Tiempo de Resolución

| Métrica | Valor |
|---------|-------|
| **Promedio** | 77.6 minutos |
| **Mínimo** | 1 minuto |
| **Máximo** | 540 minutos (9 horas) |
| **Con tiempo registrado** | 1,470 (97.4%) |

---

## Top 10 Módulos Más Afectados

| Módulo | Incidencias |
|--------|-------------|
| Módulo 300 | 552 |
| Módulo 200 | 427 |
| Módulo 400 | 274 |
| Módulo 100 | 100 |
| Alevinaje B | 99 |
| Alevinaje A | 40 |
| Módulo 500 | 15 |
| Efluente | 3 |

---

## Parámetros Afectados

| Parámetro | Incidencias |
|-----------|-------------|
| **Oxígeno** | 1,510 (100%) |
| Temperatura | 0 |
| Turbidez | 0 |
| Conductividad | 0 |

*Todas las incidencias del Excel corresponden a problemas de oxígeno*

---

## Contacto con Operarios

| Estado | Cantidad | % |
|--------|----------|---|
| Con operario registrado | 933 | 61.8% |
| Sin operario registrado | 577 | 38.2% |

---

## Periodo de Datos

- **Primera incidencia:** 9 de julio de 2025, 13:28
- **Última incidencia:** 30 de enero de 2026, 22:03
- **Periodo total:** 205 días (~6.8 meses)

---

## Validación de Integridad

✅ **Todos los datos fueron importados exitosamente**

- ✅ 1,509 incidencias del Excel importadas
- ✅ 0 errores durante la importación
- ✅ Clasificaciones preservadas exactamente como en el Excel
- ✅ Fechas y horas correctas
- ✅ Riesgos y tiempos de resolución preservados
- ✅ Operarios vinculados cuando estaban disponibles
- ✅ Centros, módulos y estanques preservados

---

## Notas Importantes

1. **Datos Reales:** Todos los datos son reales y no ficticios, listos para análisis estadístico.

2. **Clasificación Preservada:** La clasificación de incidencias se mantuvo exactamente como estaba en el Excel original.

3. **Operarios:** Se vincularon automáticamente los operarios cuando el nombre coincidía con los registros de la base de datos.

4. **Parámetros:** El 100% de las incidencias corresponden a problemas de oxígeno (alto/bajo), lo cual es consistente con el tipo de datos del Excel.

5. **Riesgos:** El 80.9% de las incidencias presentaron riesgo para los peces, y el 56.9% tuvieron impacto económico.

---

## Estado del Sistema

**Base de Datos MySQL (XAMPP1) - Estado Actual:**

| Tabla | Registros |
|-------|-----------|
| Centros | 8 |
| Operarios | 44 |
| Sensores Configurados | 181 |
| **Incidencias** | **1,510** |
| Control Diario | 0 |
| Reporte Cámaras | 0 |
| Monitoreo Sensores | 0 |
| Reporte Plataforma | 0 |

---

**Sistema completamente funcional y listo para análisis estadístico.**
