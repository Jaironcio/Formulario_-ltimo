"""
Simular exactamente los datos que el dashboard debería mostrar
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from incidencias.models import Incidencia
from django.db.models import Count

print("="*80)
print("DATOS QUE EL DASHBOARD DEBERIA MOSTRAR")
print("="*80)

# Datos de turnos
print("\nDATOS DE TURNOS:")
turnos_stats = Incidencia.objects.values('turno').annotate(
    count=Count('id')
).order_by('-count')

turnos_labels = [t['turno'] or 'Sin turno' for t in turnos_stats]
turnos_data = [t['count'] for t in turnos_stats]

print(f"turnos_labels = {turnos_labels}")
print(f"turnos_data = {turnos_data}")

# Datos de tipos
print("\nDATOS DE TIPOS:")
tipos_stats = Incidencia.objects.values('tipo_incidencia_normalizada').annotate(
    count=Count('id')
).order_by('-count')

tipos_labels = [t['tipo_incidencia_normalizada'] or 'Sin clasificar' for t in tipos_stats]
tipos_data = [t['count'] for t in tipos_stats]

print(f"\nTotal de tipos: {len(tipos_labels)}")
print("\ntipos_labels:")
for i, (label, data) in enumerate(zip(tipos_labels, tipos_data), 1):
    print(f"  {i:2}. {label:50} {data:4}")
