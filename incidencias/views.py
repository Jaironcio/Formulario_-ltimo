# incidencias/views.py (Versión Revertida a PCC)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Centro, Operario, Incidencia
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from django.views.decorators.csrf import csrf_exempt

# --- IMPORTACIONES ADICIONALES (Limpias) ---
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q, Avg # Quitamos 'F' que no se usa aquí
from django.db.models.functions import TruncDate 
from .serializers import IncidenciaSerializer 
# ---

# DATOS FIJOS DE MÓDULOS (Original)
DATOS_MODULOS_ESTANQUES = {
    "trafun": {
        "Módulo 400": ["401", "402", "403", "404", "405", "406", "407", "408", "409", "410"],
        "Módulo 300": ["301", "302", "303", "304", "305", "306", "307", "308", "309", "310", "311", "312"],
        "Módulo 200": ["201", "202", "203", "204", "205", "206", "207", "208", "209", "210", "211", "212"],
        "Alevinaje B": ["116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130"],
        "Alevinaje A": ["101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115"]
    },
    "liquine": {
        "Módulo 100": ["101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "140"],
        "Módulo 200": ["201", "202", "203", "204", "205", "206", "207"],
        "Módulo 300": ["301", "302", "303", "304", "305", "306", "307", "308", "309", "310", "311", "312", "313"],
        "Módulo 400": ["401", "402", "403", "404", "405", "406", "407", "408", "409"],
        "Módulo 500": ["501", "502", "503", "504", "505", "506", "507", "508"],
        "Alevinaje": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]
    },
    "cipreses": {
        "Módulo 100": ["101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116"],
        "Módulo 200": ["201", "202", "203", "204", "205", "206", "207", "208", "209", "210"],
        "Módulo 300": ["301", "302", "303", "304", "305", "306", "307", "308", "309", "310", "311", "312", "313", "314", "315", "316"],
        "Módulo 400": ["401", "402", "403", "404", "405", "406", "407", "408", "409", "410", "411", "412", "413", "414", "415"]
    },
    "santa_juana": {
        "Smolt 1": ["Estanque 1", "Estanque 2", "Estanque 3", "Estanque 4", "Estanque 5"],
        "Smolt 2": ["Estanque 6", "Estanque 7", "Estanque 8", "Estanque 9", "Estanque 10"],
        "Fry 1": ["Estanque A", "Estanque B", "Estanque C"],
        "Hatchery": ["Incubadora 1", "Incubadora 2", "Incubadora 3"],
    },
    "rahue": {}, "esperanza": {}, "hueyusca": {}, "pcc": {}
}

# --- VISTA 1: EL SELECTOR DE CENTROS (NUEVA PÁGINA DE INICIO) ---
# (Añade esta nueva función)
def vista_selector_centro(request):
    """
    Renderiza la nueva página principal para elegir entre PCC o Santa Juana.
    """
    return render(request, 'seleccionar_centro.html')


# --- VISTA INTELIGENTE: Redirige al formulario correcto según el centro ---
def vista_editar_incidencia_inteligente(request, pk):
    """
    Detecta si la incidencia es de Santa Juana o PCC y redirige al formulario correcto.
    """
    incidencia = get_object_or_404(Incidencia, pk=pk)
    
    # Si el centro es Santa Juana, redirige a su formulario
    if incidencia.centro and incidencia.centro.slug == 'santa-juana':
        return redirect('editar_incidencia_santa_juana', pk=pk)
    else:
        # Si es otro centro, va al formulario PCC
        return redirect('editar_incidencia_pcc', pk=pk)


# --- VISTA 2: FORMULARIO SANTA JUANA (FUNCIONAL) ---
def vista_formulario_santa_juana(request, pk=None):
    """
    Renderiza el formulario exclusivo de Santa Juana.
    """
    incidencia_a_editar = None
    incidencia_json = 'null'
    
    # 1. Lógica para EDITAR (serializar datos completos de la incidencia)
    if pk:
        incidencia_a_editar = get_object_or_404(Incidencia, pk=pk)
        incidencia_json = json.dumps({
            'pk': incidencia_a_editar.pk,
            'fecha_hora': incidencia_a_editar.fecha_hora.isoformat() if incidencia_a_editar.fecha_hora else None,
            'turno': incidencia_a_editar.turno,
            'centro_id': incidencia_a_editar.centro_id,
            'modulo': incidencia_a_editar.modulo,
            'estanque': incidencia_a_editar.estanque,
            'tipo_incidencia': incidencia_a_editar.tipo_incidencia,
            'tipo_incidencia_normalizada': incidencia_a_editar.tipo_incidencia_normalizada,
            'tiempo_resolucion': incidencia_a_editar.tiempo_resolucion,
            'riesgo_peces': incidencia_a_editar.riesgo_peces,
            'perdida_economica': incidencia_a_editar.perdida_economica,
            'riesgo_personas': incidencia_a_editar.riesgo_personas,
            'observacion': incidencia_a_editar.observacion,
            'operario_contacto_id': incidencia_a_editar.operario_contacto_id,
        })

    # 2. Obtener Centros y Operarios (igual que en PCC)
    todos_los_centros = Centro.objects.all().order_by('nombre')
    
    # Convertimos el QuerySet de Centros a una lista simple de diccionarios (JSON)
    centros_list = list(todos_los_centros.values('id', 'nombre'))
    centros_json = json.dumps(centros_list)
    
    # --- NUEVA CORRECCIÓN (para el error de "Centro no encontrado") ---
    # Necesitamos encontrar el slug del centro actual para pasarlo al JS
    centro_sj = todos_los_centros.filter(slug='santa-juana').first()
    
    operarios_por_centro = {}
    operarios = Operario.objects.select_related('centro').all()
    for op in operarios:
        centro_id = op.centro.id
        if centro_id not in operarios_por_centro:
            operarios_por_centro[centro_id] = []
        operarios_por_centro[centro_id].append({
            'id': op.id,
            'nombre': op.nombre,
            'cargo': op.cargo,
            'telefono': op.telefono
        })

    # --- CORRECCIÓN FINAL DEL CONTEXTO ---
    contexto = {
        'centros_json': centros_json, # Para el JS que usaba 'CENTROS' (ya no se usa pero es bueno tenerlo)
        'datos_modulos_json': json.dumps(DATOS_MODULOS_ESTANQUES),
        'datos_operarios_json': json.dumps(operarios_por_centro),
        'incidencia_a_editar': incidencia_a_editar,
        'incidencia_a_editar_json': incidencia_json,
        
        # --- ESTAS SON LAS 2 LÍNEAS QUE FALTABAN ---
        'centros': todos_los_centros,  # Para el bucle {% for %} en <script id="centros-data">
        'centro_actual_slug': centro_sj.slug if centro_sj else '' # Para el data-centro-slug
    }
    
    # Renderiza el nuevo template de Santa Juana
    return render(request, 'formulario_santa_juana.html', contexto)

# --- VISTA 1: EL FORMULARIO (Nombre original 'vista_formulario') ---
def vista_formulario_pcc(request, pk=None): 
    
    incidencia_a_editar = None
    incidencia_json = 'null'

    if pk:
        incidencia_a_editar = get_object_or_404(Incidencia, pk=pk)
        incidencia_json = json.dumps({
            'pk': incidencia_a_editar.pk,
            'fecha_hora': incidencia_a_editar.fecha_hora.isoformat() if incidencia_a_editar.fecha_hora else None,
            'turno': incidencia_a_editar.turno,
            'centro_id': incidencia_a_editar.centro_id,
            'tipo_incidencia': incidencia_a_editar.tipo_incidencia,
            'modulo': incidencia_a_editar.modulo,
            'estanque': incidencia_a_editar.estanque,
            'parametros_afectados': incidencia_a_editar.parametros_afectados.split(',') if incidencia_a_editar.parametros_afectados else [],
            'oxigeno_nivel': incidencia_a_editar.oxigeno_nivel,
            'oxigeno_valor': incidencia_a_editar.oxigeno_valor,
            'temperatura_nivel': incidencia_a_editar.temperatura_nivel,
            'temperatura_valor': incidencia_a_editar.temperatura_valor,
            'conductividad_nivel': incidencia_a_editar.conductividad_nivel,
            'turbidez_nivel': incidencia_a_editar.turbidez_nivel,
            'turbidez_valor': incidencia_a_editar.turbidez_valor,
            'sistema_sensor': incidencia_a_editar.sistema_sensor,
            'sensor_detectado': incidencia_a_editar.sensor_detectado,
            'sensor_nivel': incidencia_a_editar.sensor_nivel,
            'sensor_valor': incidencia_a_editar.sensor_valor,
            'tiempo_resolucion': incidencia_a_editar.tiempo_resolucion,
            'riesgo_peces': incidencia_a_editar.riesgo_peces,
            'perdida_economica': incidencia_a_editar.perdida_economica,
            'riesgo_personas': incidencia_a_editar.riesgo_personas,
            'observacion': incidencia_a_editar.observacion,
            'operario_contacto_id': incidencia_a_editar.operario_contacto_id,
            'tipo_incidencia_normalizada': incidencia_a_editar.tipo_incidencia_normalizada,
        })
    
    todos_los_centros = Centro.objects.all().order_by('nombre')
    operarios_por_centro = {}
    operarios = Operario.objects.select_related('centro').all()
    for op in operarios:
        centro_id = op.centro.id
        if centro_id not in operarios_por_centro:
            operarios_por_centro[centro_id] = []
        operarios_por_centro[centro_id].append({
            'id': op.id,
            'nombre': op.nombre,
            'cargo': op.cargo,
            'telefono': op.telefono
        })

    contexto = {
        'centros': todos_los_centros,
        'datos_modulos_json': json.dumps(DATOS_MODULOS_ESTANQUES),
        'datos_operarios_json': json.dumps(operarios_por_centro),
        'incidencia_a_editar': incidencia_a_editar,
        'incidencia_a_editar_json': incidencia_json
    }
    
    # Renderiza el formulario original
    return render(request, 'formulario.html', contexto)


# --- VISTA 2: LA PÁGINA DE REPORTES (Original) ---
def vista_reporte(request):
    
    lista_de_incidencias = Incidencia.objects.select_related(
        'centro', 'operario_contacto'
    ).all().order_by('-fecha_hora')
    
    filtro_fecha = request.GET.get('fecha', None)
    filtro_turno = request.GET.get('turno', None)
    filtro_centro = request.GET.get('centro', None)
    filtro_tipo = request.GET.get('tipo', None)

    if filtro_fecha:
        lista_de_incidencias = lista_de_incidencias.filter(fecha_hora__date=filtro_fecha)
    if filtro_turno:
        lista_de_incidencias = lista_de_incidencias.filter(turno=filtro_turno)
    if filtro_centro:
        lista_de_incidencias = lista_de_incidencias.filter(centro_id=filtro_centro)
    if filtro_tipo:
        lista_de_incidencias = lista_de_incidencias.filter(tipo_incidencia=filtro_tipo)

    todos_los_centros = Centro.objects.all().order_by('nombre')
    
    contexto = {
        'incidencias': lista_de_incidencias,
        'centros': todos_los_centros,
        'filtros_aplicados': request.GET
    }
    
    return render(request, 'reporte.html', contexto)


# --- VISTA 3: DASHBOARD (Original) ---
def vista_dashboard(request):
    
    periodo_filtro = request.GET.get('periodo', 'all')
    centro_filtro = request.GET.get('centro', None)

    base_query = Incidencia.objects.all()
    fecha_limite = None
    if periodo_filtro == 'week':
        fecha_limite = timezone.now() - timedelta(days=7)
    elif periodo_filtro == 'month':
        fecha_limite = timezone.now() - timedelta(days=30)
    elif periodo_filtro == 'quarter':
        fecha_limite = timezone.now() - timedelta(days=90)
    
    if fecha_limite:
        base_query = base_query.filter(fecha_hora__gte=fecha_limite)
    if centro_filtro:
        base_query = base_query.filter(centro_id=centro_filtro)

    total_incidencias = base_query.count()
    alto_riesgo_count = base_query.filter(Q(riesgo_peces=True) | Q(riesgo_personas=True)).count()
    promedio_dict = base_query.filter(tiempo_resolucion__isnull=False).aggregate(avg_tiempo=Avg('tiempo_resolucion'))
    promedio_resolucion = int(promedio_dict['avg_tiempo']) if promedio_dict['avg_tiempo'] else 0

    chart_centro_query = base_query.filter(centro__isnull=False) \
        .values('centro__nombre') \
        .annotate(count=Count('id')) \
        .order_by('-count')
    chart_centro_labels = [item['centro__nombre'] for item in chart_centro_query]
    chart_centro_counts = [item['count'] for item in chart_centro_query]
    centro_mas_incidencias = chart_centro_labels[0] if chart_centro_labels else "-"

    chart_tendencia_query = base_query \
        .annotate(dia=TruncDate('fecha_hora')) \
        .values('dia') \
        .annotate(count=Count('id')) \
        .order_by('dia')
    chart_tendencia_labels = [item['dia'].strftime('%Y-%m-%d') for item in chart_tendencia_query]
    chart_tendencia_data = [item['count'] for item in chart_tendencia_query]

    modulos_count = base_query.filter(tipo_incidencia='modulos').count()
    sensores_count = base_query.filter(tipo_incidencia='sensores').count()
    chart_tipos_data = [modulos_count, sensores_count]
    
    chart_operario_query = base_query.filter(operario_contacto__isnull=False) \
        .values('operario_contacto__nombre') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:7]
    chart_operario_labels = [item['operario_contacto__nombre'] for item in chart_operario_query]
    chart_operario_data = [item['count'] for item in chart_operario_query]

    chart_clasificacion_query = base_query.filter(tipo_incidencia_normalizada__isnull=False) \
        .exclude(tipo_incidencia_normalizada='') \
        .values('tipo_incidencia_normalizada') \
        .annotate(count=Count('id')) \
        .order_by('-count')
    chart_clasificacion_labels = [item['tipo_incidencia_normalizada'] for item in chart_clasificacion_query]
    chart_clasificacion_data = [item['count'] for item in chart_clasificacion_query]

    kpi_query = base_query.filter(centro__isnull=False, tiempo_resolucion__isnull=False) \
        .values('centro__nombre') \
        .annotate(
            total_incidencias=Count('id'),
            en_kpi=Count('id', filter=Q(tiempo_resolucion__lte=20)),
        ).order_by('-total_incidencias')
    kpi_lista_final = []
    
    for item in kpi_query:
        total = item['total_incidencias']
        en_kpi = item['en_kpi']
        porcentaje = round((en_kpi / total) * 100) if total > 0 else 0
        kpi_lista_final.append({
            'centro_nombre': item['centro__nombre'],
            'total_incidencias': total, 'en_kpi': en_kpi,
            'porcentaje': porcentaje, 'cumple_meta': porcentaje >= 80
        })

    contexto = {
        'total_incidencias': total_incidencias,
        'centro_mas_incidencias': centro_mas_incidencias,
        'alto_riesgo_count': alto_riesgo_count,
        'promedio_resolucion': promedio_resolucion,
        'chart_centro_labels_json': json.dumps(chart_centro_labels),
        'chart_centro_counts_json': json.dumps(chart_centro_counts),
        'chart_tendencia_labels_json': json.dumps(chart_tendencia_labels),
        'chart_tendencia_data_json': json.dumps(chart_tendencia_data),
        'chart_tipos_data_json': json.dumps(chart_tipos_data),
        'chart_operario_labels_json': json.dumps(chart_operario_labels),
        'chart_operario_data_json': json.dumps(chart_operario_data),
        'chart_clasificacion_labels_json': json.dumps(chart_clasificacion_labels),
        'chart_clasificacion_data_json': json.dumps(chart_clasificacion_data),
        'kpi_data': kpi_lista_final,
        'centros': Centro.objects.all().order_by('nombre'),
        'filtros_aplicados': request.GET
    }
    
    return render(request, 'dashboard.html', contexto)


# --- APIs (Originales) ---

@csrf_exempt
@api_view(['POST'])
def registrar_incidencia_api(request):
    if request.method == 'POST':
        serializer = IncidenciaSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
@api_view(['PUT'])
def update_incidencia_api(request, pk):
    try:
        incidencia = Incidencia.objects.get(pk=pk)
    except Incidencia.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = IncidenciaSerializer(incidencia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        print(serializer.errors) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
@api_view(['DELETE'])
def delete_incidencia_api(request, pk):
    
    incidencia = get_object_or_404(Incidencia, pk=pk)
    
    if request.method == 'DELETE':
        incidencia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)