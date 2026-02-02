"""
Normalizar tipos de incidencia duplicados en la base de datos
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from incidencias.models import Incidencia

print("="*80)
print("NORMALIZANDO TIPOS DE INCIDENCIA DUPLICADOS")
print("="*80)

# 1. Normalizar "Estanque en Vacunacion" (sin tilde) a "Estanque en Vacunación" (con tilde)
print("\n1. Normalizando 'Estanque en Vacunacion' -> 'Estanque en Vacunación'")
count1 = Incidencia.objects.filter(tipo_incidencia_normalizada='Estanque en Vacunacion').update(
    tipo_incidencia_normalizada='Estanque en Vacunación'
)
print(f"   Actualizados: {count1} registros")

# 2. Normalizar "ALZA DE OXIGENO, SATURACION" a "Oxígeno Alto"
print("\n2. Normalizando 'ALZA DE OXIGENO, SATURACION' -> 'Oxígeno Alto'")
count2 = Incidencia.objects.filter(tipo_incidencia_normalizada='ALZA DE OXIGENO, SATURACION').update(
    tipo_incidencia_normalizada='Oxígeno Alto'
)
print(f"   Actualizados: {count2} registros")

# 3. Verificar tipos únicos después de normalización
print("\n" + "="*80)
print("TIPOS DE INCIDENCIA DESPUÉS DE NORMALIZACIÓN")
print("="*80)

from django.db.models import Count

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
