"""
Verificar turnos en la base de datos
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from incidencias.models import Incidencia
from django.db.models import Count

print("="*80)
print("VERIFICANDO TURNOS EN LA BASE DE DATOS")
print("="*80)

turnos = Incidencia.objects.values('turno').annotate(
    total=Count('id')
).order_by('-total')

print(f"\nTotal de turnos únicos: {len(turnos)}\n")

for t in turnos:
    turno = t['turno'] if t['turno'] else '(vacío)'
    total = t['total']
    porcentaje = (total / Incidencia.objects.count()) * 100
    print(f"  Turno: '{turno:20}' -> {total:4} incidencias ({porcentaje:5.1f}%)")

print("\n" + "="*80)
print("VERIFICANDO VALORES EXACTOS")
print("="*80)

# Verificar valores específicos
dia = Incidencia.objects.filter(turno='Día').count()
manana = Incidencia.objects.filter(turno='Mañana').count()
tarde = Incidencia.objects.filter(turno='Tarde').count()
noche = Incidencia.objects.filter(turno='Noche').count()

print(f"\nBúsqueda exacta:")
print(f"  turno='Día':     {dia}")
print(f"  turno='Mañana':  {manana}")
print(f"  turno='Tarde':   {tarde}")
print(f"  turno='Noche':   {noche}")

# Verificar con case-insensitive
dia_i = Incidencia.objects.filter(turno__iexact='dia').count()
manana_i = Incidencia.objects.filter(turno__iexact='mañana').count()

print(f"\nBúsqueda case-insensitive:")
print(f"  turno__iexact='dia':     {dia_i}")
print(f"  turno__iexact='mañana':  {manana_i}")
