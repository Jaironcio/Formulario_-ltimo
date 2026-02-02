"""
Normalizar variaciones de "Problemas con el cono de oxigenación"
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from incidencias.models import Incidencia
from django.db.models import Count

print("="*80)
print("NORMALIZANDO 'PROBLEMAS CON EL CONO DE OXIGENACIÓN'")
print("="*80)

# Buscar todas las variaciones
variaciones = Incidencia.objects.filter(
    tipo_incidencia_normalizada__icontains='cono'
).values('tipo_incidencia_normalizada').annotate(
    total=Count('id')
).order_by('-total')

print("\nVariaciones encontradas:")
for v in variaciones:
    print(f"  '{v['tipo_incidencia_normalizada']}' - {v['total']} registros")

# Normalizar todas las variaciones a una forma estándar
tipo_normalizado = 'Problemas con el cono de oxigenación'

print(f"\nNormalizando todas a: '{tipo_normalizado}'")

# Actualizar todas las variaciones
total_actualizados = 0

# Variación 1: "Problemas con el cono de oxigenacion" (sin tilde)
count1 = Incidencia.objects.filter(
    tipo_incidencia_normalizada='Problemas con el cono de oxigenacion'
).update(tipo_incidencia_normalizada=tipo_normalizado)
if count1 > 0:
    print(f"  'Problemas con el cono de oxigenacion' -> {count1} registros")
    total_actualizados += count1

# Variación 2: Con mayúsculas diferentes
count2 = Incidencia.objects.filter(
    tipo_incidencia_normalizada='problemas con el cono de oxigenación'
).update(tipo_incidencia_normalizada=tipo_normalizado)
if count2 > 0:
    print(f"  'problemas con el cono de oxigenación' -> {count2} registros")
    total_actualizados += count2

print(f"\nTotal actualizados: {total_actualizados}")

# Verificar resultado final
print("\n" + "="*80)
print("TIPOS DE INCIDENCIA DESPUÉS DE NORMALIZACIÓN")
print("="*80)

tipos = Incidencia.objects.values('tipo_incidencia_normalizada').annotate(
    total=Count('id')
).order_by('-total')

print(f"\nTotal de tipos únicos: {len(tipos)}\n")

for idx, item in enumerate(tipos, 1):
    tipo = item['tipo_incidencia_normalizada']
    total = item['total']
    porcentaje = (total / Incidencia.objects.count()) * 100
    print(f"{idx:2}. {tipo:50} {total:4} ({porcentaje:5.1f}%)")

print(f"\n{'='*80}")
print(f"Total de incidencias: {Incidencia.objects.count()}")
print(f"Total de tipos únicos: {len(tipos)}")
print(f"{'='*80}")
