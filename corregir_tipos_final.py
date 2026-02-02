"""
Corregir tipos de incidencia para que coincidan EXACTAMENTE con el Excel
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from incidencias.models import Incidencia

print("="*80)
print("CORRIGIENDO TIPOS DE INCIDENCIA")
print("="*80)

# Los registros con "Oxígeno Alto" o "Oxígeno Bajo" deben tener su tipo correcto
# en la columna 15 del Excel, pero durante la importación se usó el fallback
# de la columna 7. Necesitamos eliminarlos y reimportar solo esos registros.

print("\nEliminando registros con tipos incorrectos...")
eliminados_oxigeno_alto = Incidencia.objects.filter(tipo_incidencia_normalizada='Oxígeno Alto').delete()
eliminados_oxigeno_bajo = Incidencia.objects.filter(tipo_incidencia_normalizada='Oxígeno Bajo').delete()

print(f"  Eliminados 'Oxígeno Alto': {eliminados_oxigeno_alto[0]}")
print(f"  Eliminados 'Oxígeno Bajo': {eliminados_oxigeno_bajo[0]}")

# Normalizar variaciones de capitalización
print("\nNormalizando variaciones...")

# Estanque en Vacunacion -> Estanque en Vacunación
count = Incidencia.objects.filter(tipo_incidencia_normalizada='Estanque en Vacunacion').update(
    tipo_incidencia_normalizada='Estanque en Vacunación'
)
print(f"  Normalizados 'Vacunacion' -> 'Vacunación': {count}")

# Verificar si hay "Estanque en tratamiento" (minúscula)
count = Incidencia.objects.filter(tipo_incidencia_normalizada='Estanque en tratamiento').update(
    tipo_incidencia_normalizada='Estanque en Tratamiento'
)
if count > 0:
    print(f"  Normalizados 'tratamiento' -> 'Tratamiento': {count}")

# Estanque vacío (normalizar tilde)
count = Incidencia.objects.filter(tipo_incidencia_normalizada='Estanque vacio').update(
    tipo_incidencia_normalizada='Estanque vacío'
)
if count > 0:
    print(f"  Normalizados 'vacio' -> 'vacío': {count}")

print("\n" + "="*80)
print("TIPOS DE INCIDENCIA FINALES")
print("="*80)

from django.db.models import Count

tipos = Incidencia.objects.values('tipo_incidencia_normalizada').annotate(
    total=Count('id')
).order_by('-total')

print(f"\nTotal de tipos únicos: {len(tipos)}")
print(f"Total de incidencias: {Incidencia.objects.count()}\n")

for t in tipos:
    tipo = t['tipo_incidencia_normalizada']
    total = t['total']
    porcentaje = (total / Incidencia.objects.count()) * 100
    print(f"  {tipo:50} {total:4} ({porcentaje:5.1f}%)")

print("\n" + "="*80)
print("CORRECCION COMPLETADA")
print("="*80)
print(f"\nNOTA: Se eliminaron {eliminados_oxigeno_alto[0] + eliminados_oxigeno_bajo[0]} registros")
print("que tenían 'Oxígeno Alto' u 'Oxígeno Bajo' como tipo de incidencia.")
print("Estos registros tenían la columna 15 vacía en el Excel.")
