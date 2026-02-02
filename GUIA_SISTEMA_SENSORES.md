# 🔧 Sistema de Monitoreo de Sensores - Guía de Implementación

## ✅ Estado Actual

### Completado:
1. ✅ Modelos de base de datos creados (`SensorConfig` y `MonitoreoSensores`)
2. ✅ Migraciones aplicadas
3. ✅ 23 sensores poblados desde el Excel en la tabla `SensorConfig`

### Pendiente:
1. ⏳ Vistas y APIs
2. ⏳ URLs
3. ⏳ Template HTML
4. ⏳ JavaScript
5. ⏳ Generación de PDF
6. ⏳ Botón en menú

---

## 📋 Próximos Pasos

### 1. Crear Vistas en `incidencias/views.py`

Agregar al final del archivo:

```python
# === SISTEMA DE SENSORES (IDEAL CONTROL) ===

@login_required
def vista_monitoreo_sensores(request):
    """Vista principal del formulario de monitoreo de sensores"""
    centros = Centro.objects.all().order_by('nombre')
    
    contexto = {
        'centros': centros,
        'fecha_hoy': datetime.now().date(),
    }
    
    return render(request, 'monitoreo_sensores.html', contexto)


@login_required
def api_obtener_sistemas(request):
    """API para obtener sistemas disponibles por centro"""
    centro_id = request.GET.get('centro_id')
    
    if not centro_id:
        return JsonResponse({'error': 'Centro no especificado'}, status=400)
    
    try:
        # Obtener sistemas únicos para este centro
        sistemas = SensorConfig.objects.filter(
            centro_id=centro_id,
            activo=True
        ).values_list('sistema', flat=True).distinct().order_by('sistema')
        
        return JsonResponse({
            'sistemas': list(sistemas)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def api_obtener_sensores(request):
    """API para obtener sensores de un sistema específico"""
    centro_id = request.GET.get('centro_id')
    sistema = request.GET.get('sistema')
    
    if not centro_id or not sistema:
        return JsonResponse({'error': 'Parámetros incompletos'}, status=400)
    
    try:
        sensores = SensorConfig.objects.filter(
            centro_id=centro_id,
            sistema=sistema,
            activo=True
        ).values(
            'id',
            'equipo',
            'tipo_medicion',
            'limite_min',
            'limite_max'
        ).order_by('orden', 'equipo')
        
        return JsonResponse({
            'sensores': list(sensores)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def api_guardar_monitoreo(request):
    """API para guardar el monitoreo completo de sensores"""
    try:
        data = json.loads(request.body)
        
        fecha = data.get('fecha')
        turno = data.get('turno')
        responsable = data.get('responsable')
        registros = data.get('registros', [])
        
        if not all([fecha, turno, responsable, registros]):
            return JsonResponse({'error': 'Datos incompletos'}, status=400)
        
        # Guardar cada registro
        registros_guardados = 0
        for reg in registros:
            MonitoreoSensores.objects.update_or_create(
                fecha=fecha,
                turno=turno,
                centro_id=reg['centro_id'],
                sensor_id=reg['sensor_id'],
                defaults={
                    'estado': reg['estado'],
                    'observacion': reg.get('observacion', ''),
                    'responsable': responsable
                }
            )
            registros_guardados += 1
        
        return JsonResponse({
            'success': True,
            'mensaje': f'{registros_guardados} sensores registrados correctamente',
            'registros_guardados': registros_guardados
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

### 2. Agregar URLs en `incidencias/urls.py`

Agregar estas rutas:

```python
# Sistema de Sensores
path('monitoreo-sensores/', views.vista_monitoreo_sensores, name='monitoreo_sensores'),
path('api/sensores/sistemas/', views.api_obtener_sistemas, name='api_obtener_sistemas'),
path('api/sensores/sensores/', views.api_obtener_sensores, name='api_obtener_sensores'),
path('api/sensores/guardar/', views.api_guardar_monitoreo, name='api_guardar_monitoreo'),
```

### 3. Crear Template `templates/monitoreo_sensores.html`

Ver archivo adjunto `monitoreo_sensores.html` (demasiado largo para incluir aquí)

### 4. Crear JavaScript `static/js/monitoreo_sensores.js`

Ver archivo adjunto `monitoreo_sensores.js` (demasiado largo para incluir aquí)

### 5. Agregar Botón en el Menú

En `templates/reporte.html`, agregar en la sección de botones:

```html
<a href="{% url 'monitoreo_sensores' %}" class="action-primary" style="background: #17a2b8;">
    🔧 Sistema de Sensores
</a>
```

---

## 🎯 Flujo de Trabajo del Sistema

1. Usuario abre "Sistema de Sensores"
2. Selecciona **Fecha**, **Turno**, **Responsable**
3. Selecciona **Centro** → carga sistemas disponibles
4. Selecciona **Sistema** → carga sensores de ese sistema
5. Para cada sensor, marca: **NORMAL / ALTO / BAJO**
6. Agrega observación si es necesario
7. Hace clic en "Agregar a Reporte" → se guarda en sesión
8. Repite para otros centros/sistemas
9. Al final, hace clic en "Guardar Reporte Completo"
10. Sistema genera PDF como la imagen del usuario

---

## 📊 Generación de PDF

El PDF debe tener:
- **Título**: "REPORTE DIARIO TURNO [TURNO] [FECHA]"
- **Subtítulo**: "INFORME DE ALERTAS - SISTEMAS DE MONITOREO"
- **Tabla** con columnas:
  - FECHA
  - PISCICULTURA
  - SISTEMA
  - EQUIPO
  - TIPO DE MEDICIÓN
  - INCIDENCIA (descripción del límite)
  - TOTAL ALTO
  - TOTAL BAJO

---

## 🚀 Para Continuar

1. Crea los archivos de template y JavaScript
2. Agrega las vistas y URLs
3. Prueba el flujo completo
4. Implementa la generación de PDF
5. Pobla más sensores desde el Excel si es necesario

---

**Fecha**: 27-01-2026
**Sistema**: Monitoreo de Sensores - Ideal Control
**Estado**: Base de datos lista, pendiente implementación de interfaz
