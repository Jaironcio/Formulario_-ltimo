"""
Script para verificar la calidad de los datos importados y generar estadísticas
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from incidencias.models import Incidencia, Centro
from django.db.models import Count, Q
from collections import Counter

print("="*80)
print("VERIFICACION DE DATOS IMPORTADOS")
print("="*80)

# Total de incidencias
total = Incidencia.objects.count()
print(f"\nTotal de incidencias en BD: {total}")

# Por centro
print("\n" + "-"*80)
print("INCIDENCIAS POR CENTRO:")
print("-"*80)
por_centro = Incidencia.objects.values('centro__nombre').annotate(
    total=Count('id')
).order_by('-total')

for item in por_centro:
    centro = item['centro__nombre'] if item['centro__nombre'] else 'Sin centro'
    total = item['total']
    porcentaje = (total / Incidencia.objects.count()) * 100
    print(f"  {centro:20} {total:4} incidencias ({porcentaje:5.1f}%)")

# Por turno
print("\n" + "-"*80)
print("INCIDENCIAS POR TURNO:")
print("-"*80)
por_turno = Incidencia.objects.values('turno').annotate(
    total=Count('id')
).order_by('-total')

for item in por_turno:
    turno = item['turno'] if item['turno'] else 'Sin turno'
    total = item['total']
    porcentaje = (total / Incidencia.objects.count()) * 100
    print(f"  {turno:20} {total:4} incidencias ({porcentaje:5.1f}%)")

# Por tipo de incidencia normalizada
print("\n" + "-"*80)
print("TOP 10 TIPOS DE INCIDENCIA NORMALIZADA:")
print("-"*80)
por_tipo = Incidencia.objects.values('tipo_incidencia_normalizada').annotate(
    total=Count('id')
).order_by('-total')[:10]

for item in por_tipo:
    tipo = item['tipo_incidencia_normalizada'] if item['tipo_incidencia_normalizada'] else 'Sin clasificar'
    total = item['total']
    porcentaje = (total / Incidencia.objects.count()) * 100
    print(f"  {tipo:40} {total:4} ({porcentaje:5.1f}%)")

# Riesgos
print("\n" + "-"*80)
print("EVALUACION DE RIESGOS:")
print("-"*80)
riesgo_peces = Incidencia.objects.filter(riesgo_peces=True).count()
perdida_economica = Incidencia.objects.filter(perdida_economica=True).count()
riesgo_personas = Incidencia.objects.filter(riesgo_personas=True).count()

print(f"  Riesgo para peces:        {riesgo_peces:4} incidencias ({(riesgo_peces/total)*100:5.1f}%)")
print(f"  Perdida economica:        {perdida_economica:4} incidencias ({(perdida_economica/total)*100:5.1f}%)")
print(f"  Riesgo para personas:     {riesgo_personas:4} incidencias ({(riesgo_personas/total)*100:5.1f}%)")

# Tiempo de resolución
print("\n" + "-"*80)
print("TIEMPO DE RESOLUCION:")
print("-"*80)
con_tiempo = Incidencia.objects.filter(tiempo_resolucion__isnull=False)
if con_tiempo.exists():
    from django.db.models import Avg, Min, Max
    stats = con_tiempo.aggregate(
        promedio=Avg('tiempo_resolucion'),
        minimo=Min('tiempo_resolucion'),
        maximo=Max('tiempo_resolucion')
    )
    print(f"  Promedio: {stats['promedio']:.1f} minutos")
    print(f"  Minimo:   {stats['minimo']} minutos")
    print(f"  Maximo:   {stats['maximo']} minutos")
    print(f"  Total con tiempo registrado: {con_tiempo.count()} ({(con_tiempo.count()/total)*100:.1f}%)")

# Módulos más afectados
print("\n" + "-"*80)
print("TOP 10 MODULOS MAS AFECTADOS:")
print("-"*80)
por_modulo = Incidencia.objects.values('modulo').annotate(
    total=Count('id')
).order_by('-total')[:10]

for item in por_modulo:
    modulo = item['modulo'] if item['modulo'] else 'Sin modulo'
    total = item['total']
    print(f"  {modulo:20} {total:4} incidencias")

# Parámetros afectados
print("\n" + "-"*80)
print("PARAMETROS AFECTADOS:")
print("-"*80)
oxigeno = Incidencia.objects.filter(Q(oxigeno_nivel__isnull=False) & ~Q(oxigeno_nivel='')).count()
temperatura = Incidencia.objects.filter(Q(temperatura_nivel__isnull=False) & ~Q(temperatura_nivel='')).count()
turbidez = Incidencia.objects.filter(Q(turbidez_nivel__isnull=False) & ~Q(turbidez_nivel='')).count()
conductividad = Incidencia.objects.filter(Q(conductividad_nivel__isnull=False) & ~Q(conductividad_nivel='')).count()

print(f"  Oxigeno:        {oxigeno:4} incidencias")
print(f"  Temperatura:    {temperatura:4} incidencias")
print(f"  Turbidez:       {turbidez:4} incidencias")
print(f"  Conductividad:  {conductividad:4} incidencias")

# Operarios contactados
print("\n" + "-"*80)
print("OPERARIOS CONTACTADOS:")
print("-"*80)
con_operario = Incidencia.objects.filter(operario_contacto__isnull=False).count()
sin_operario = Incidencia.objects.filter(operario_contacto__isnull=True).count()
print(f"  Con operario registrado:  {con_operario:4} ({(con_operario/total)*100:5.1f}%)")
print(f"  Sin operario registrado:  {sin_operario:4} ({(sin_operario/total)*100:5.1f}%)")

# Rango de fechas
print("\n" + "-"*80)
print("RANGO DE FECHAS:")
print("-"*80)
from django.db.models import Min, Max
fechas = Incidencia.objects.aggregate(
    primera=Min('fecha_hora'),
    ultima=Max('fecha_hora')
)
if fechas['primera'] and fechas['ultima']:
    print(f"  Primera incidencia: {fechas['primera'].strftime('%Y-%m-%d %H:%M')}")
    print(f"  Ultima incidencia:  {fechas['ultima'].strftime('%Y-%m-%d %H:%M')}")
    dias = (fechas['ultima'].date() - fechas['primera'].date()).days
    print(f"  Periodo total:      {dias} dias")

print("\n" + "="*80)
print("VERIFICACION COMPLETADA")
print("="*80)
