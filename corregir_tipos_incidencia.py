"""
Script para corregir y normalizar los tipos de incidencia en la base de datos
según los valores exactos del Excel
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from incidencias.models import Incidencia

# Mapeo de normalización para unificar variaciones
normalizacion = {
    'Estanque en Flashing': 'Estanque en Flashing',
    'Estanque en flashing': 'Estanque en Flashing',
    'Estanque en Vacunación': 'Estanque en Vacunación',
    'Estanque en Vacunacion': 'Estanque en Vacunación',
    'Problemas con el cono de oxigenación': 'Problemas con el cono de oxigenación',
    'Problemas con el cono de oxigenacion': 'Problemas con el cono de oxigenación',
    'Estanque en Selección': 'Estanque en Selección',
    'Estanque vacío': 'Estanque vacío',
    'ALZA DE OXIGENO, SATURACION': 'ALZA DE OXIGENO, SATURACION',
}

print("="*80)
print("NORMALIZANDO TIPOS DE INCIDENCIA")
print("="*80)

# Obtener todos los tipos únicos actuales
tipos_actuales = Incidencia.objects.values_list('tipo_incidencia_normalizada', flat=True).distinct()
print(f"\nTipos únicos antes de normalizar: {len(tipos_actuales)}")

actualizados = 0

# Normalizar cada tipo
for tipo_original, tipo_normalizado in normalizacion.items():
    count = Incidencia.objects.filter(tipo_incidencia_normalizada=tipo_original).update(
        tipo_incidencia_normalizada=tipo_normalizado
    )
    if count > 0:
        actualizados += count
        print(f"  [{count:4}] '{tipo_original}' -> '{tipo_normalizado}'")

print(f"\nTotal de registros actualizados: {actualizados}")

# Mostrar tipos únicos después de normalizar
print("\n" + "="*80)
print("TIPOS DE INCIDENCIA FINALES")
print("="*80)

from django.db.models import Count

tipos_finales = Incidencia.objects.values('tipo_incidencia_normalizada').annotate(
    total=Count('id')
).order_by('-total')

print(f"\nTotal de tipos únicos: {len(tipos_finales)}\n")

for item in tipos_finales:
    tipo = item['tipo_incidencia_normalizada']
    total = item['total']
    porcentaje = (total / Incidencia.objects.count()) * 100
    print(f"  {tipo:50} {total:4} ({porcentaje:5.1f}%)")

print("\n" + "="*80)
print("NORMALIZACION COMPLETADA")
print("="*80)
