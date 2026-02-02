"""
Contar tipos únicos de incidencia eliminando duplicados y variaciones
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from incidencias.models import Incidencia
from django.db.models import Count

print("="*80)
print("TIPOS UNICOS DE INCIDENCIA (CONSOLIDADOS)")
print("="*80)

# Obtener todos los tipos
tipos = Incidencia.objects.values('tipo_incidencia_normalizada').annotate(
    total=Count('id')
).order_by('-total')

print(f"\nTotal de tipos únicos en BD: {len(tipos)}\n")

# Agrupar variaciones similares
tipos_consolidados = {}

for t in tipos:
    tipo = t['tipo_incidencia_normalizada']
    total = t['total']
    
    # Normalizar para consolidar
    tipo_lower = tipo.lower().strip()
    
    # Mapear variaciones al mismo tipo
    if 'vacunacion' in tipo_lower or 'vacunación' in tipo_lower:
        tipo_key = 'Estanque en Vacunación'
    elif tipo_lower == 'oxígeno alto' or tipo_lower == 'oxigeno alto':
        tipo_key = 'Oxígeno Alto'
    elif tipo_lower == 'oxígeno bajo' or tipo_lower == 'oxigeno bajo':
        tipo_key = 'Oxígeno Bajo'
    elif 'problema con el sensor' in tipo_lower or 'problemas con el sensor' in tipo_lower:
        tipo_key = 'Problema con el sensor'
    else:
        tipo_key = tipo
    
    if tipo_key in tipos_consolidados:
        tipos_consolidados[tipo_key] += total
    else:
        tipos_consolidados[tipo_key] = total

# Ordenar por cantidad
tipos_ordenados = sorted(tipos_consolidados.items(), key=lambda x: x[1], reverse=True)

print(f"Tipos consolidados: {len(tipos_ordenados)}\n")

for idx, (tipo, total) in enumerate(tipos_ordenados, 1):
    porcentaje = (total / Incidencia.objects.count()) * 100
    print(f"{idx:2}. {tipo:50} {total:4} ({porcentaje:5.1f}%)")

print(f"\n{'='*80}")
print(f"Total de incidencias: {Incidencia.objects.count()}")
print(f"Total de tipos consolidados: {len(tipos_ordenados)}")
print(f"{'='*80}")
