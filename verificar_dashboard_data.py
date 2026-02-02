"""
Verificar exactamente qué datos debería mostrar el dashboard
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from incidencias.models import Incidencia, Centro
from django.db.models import Count

print("="*80)
print("DATOS QUE DEBERIA MOSTRAR EL DASHBOARD")
print("="*80)

# Total de incidencias
total = Incidencia.objects.count()
print(f"\nTotal Incidencias: {total}")

# Oxígeno alto
oxigeno_alto = Incidencia.objects.filter(oxigeno_nivel='alta').count()
print(f"Oxígeno Alto: {oxigeno_alto}")

# Oxígeno bajo
oxigeno_bajo = Incidencia.objects.filter(oxigeno_nivel='baja').count()
print(f"Oxígeno Bajo: {oxigeno_bajo}")

# Temperatura baja
temperatura_baja = Incidencia.objects.filter(temperatura_nivel='baja').count()
print(f"Temperatura Baja: {temperatura_baja}")

# Por centro
print("\nIncidencias por Centro:")
por_centro = Incidencia.objects.values('centro__nombre').annotate(
    total=Count('id')
).order_by('-total')

for item in por_centro:
    print(f"  {item['centro__nombre']:20} {item['total']:4}")

# Por turno
print("\nIncidencias por Turno:")
por_turno = Incidencia.objects.values('turno').annotate(
    total=Count('id')
).order_by('-total')

for item in por_turno:
    print(f"  {item['turno']:20} {item['total']:4}")

# Tipos de incidencia
print("\nTop 10 Tipos de Incidencia:")
tipos = Incidencia.objects.values('tipo_incidencia_normalizada').annotate(
    total=Count('id')
).order_by('-total')[:10]

for item in tipos:
    tipo = item['tipo_incidencia_normalizada'] or 'Sin clasificar'
    print(f"  {tipo:50} {item['total']:4}")

print("\n" + "="*80)
