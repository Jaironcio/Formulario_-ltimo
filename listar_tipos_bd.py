"""
Listar tipos de incidencia en la base de datos
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from incidencias.models import Incidencia
from django.db.models import Count

tipos = Incidencia.objects.values('tipo_incidencia_normalizada').annotate(
    total=Count('id')
).order_by('-total')

print("="*80)
print("TIPOS DE INCIDENCIA EN LA BASE DE DATOS")
print("="*80)
print(f"\nTotal de tipos unicos: {len(tipos)}\n")

for t in tipos:
    tipo = t['tipo_incidencia_normalizada']
    total = t['total']
    print(f"  {tipo:50} {total:4}")

print("\n" + "="*80)
print("COMPARACION CON FILTROS ESPERADOS")
print("="*80)

# Tipos que deberían estar según la imagen
tipos_esperados = [
    'Estanque en Manejo',
    'Estanque en tratamiento',
    'Estanque con traslado de peces',
    'Problemas con el cono de oxigenación',
    'Estanque en Vacunación',
    'Estanque en Selección',
    'Manipulando sensor',
    'Desdoble de estanque',
    'Estanque en Flashing',
    'Sin respuesta del centro',
    'Estanque vacío',
    'Estanque en Ayunas',
    'ALZA DE OXIGENO, SATURACION',
    'Problemas con la plataforma'
]

tipos_bd = [t['tipo_incidencia_normalizada'] for t in tipos]

print("\nTipos esperados que NO estan en BD:")
for tipo in tipos_esperados:
    if tipo not in tipos_bd:
        print(f"  - {tipo}")

print("\nTipos en BD que NO estan en lista esperada:")
for tipo in tipos_bd:
    if tipo not in tipos_esperados:
        print(f"  - {tipo}")
