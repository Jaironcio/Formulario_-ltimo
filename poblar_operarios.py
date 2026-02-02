import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from incidencias.models import Centro, Operario

# Limpiar operarios existentes
Operario.objects.all().delete()

# Datos de operarios por centro
operarios_data = [
    # CIPRESES
    {'id': 1, 'centro': 'cipreses', 'nombre': 'Roberto Alarcón', 'cargo': 'Jefe de Centro', 'telefono': '+569 6155 6741'},
    {'id': 2, 'centro': 'cipreses', 'nombre': 'Claudio Zúñiga', 'cargo': 'Asistente de Centro', 'telefono': '+569 8582 2564'},
    {'id': 3, 'centro': 'cipreses', 'nombre': 'Dominique Cabrera', 'cargo': 'Asistente de Centro', 'telefono': '+569 6181 0024'},
    {'id': 4, 'centro': 'cipreses', 'nombre': 'Jorge Vidal', 'cargo': 'Asistente de Centro', 'telefono': '+569 5361 2276'},
    {'id': 5, 'centro': 'cipreses', 'nombre': 'Marcelo Mena', 'cargo': 'Asistente de Centro', 'telefono': '+569 9884 2121'},
    {'id': 6, 'centro': 'cipreses', 'nombre': 'Rodrigo López', 'cargo': 'Asistente de Centro', 'telefono': '+569 6721 4135'},
    {'id': 7, 'centro': 'cipreses', 'nombre': 'Sebastián Peralta', 'cargo': 'Asistente de Centro', 'telefono': '+569 8475 6452'},
    {'id': 8, 'centro': 'cipreses', 'nombre': 'Técnicos turno día', 'cargo': 'Técnico', 'telefono': '65 256 8165'},
    {'id': 9, 'centro': 'cipreses', 'nombre': 'Operarios turno Tarde/Noche', 'cargo': 'Operario', 'telefono': '+569 8932 3982'},
    
    # LIQUIÑE
    {'id': 10, 'centro': 'liquine', 'nombre': 'Roberto Parra', 'cargo': 'Jefe de Centro', 'telefono': '+569 4471 6465'},
    {'id': 11, 'centro': 'liquine', 'nombre': 'Manuel Krebs', 'cargo': 'Asistente de Centro', 'telefono': '+569 8832 4988'},
    {'id': 12, 'centro': 'liquine', 'nombre': 'Guillermo Contreras', 'cargo': 'Asistente de Centro', 'telefono': '+569 4093 5028'},
    {'id': 13, 'centro': 'liquine', 'nombre': 'Diego Pichun', 'cargo': 'Asistente de Centro', 'telefono': '+569 4421 4065'},
    {'id': 14, 'centro': 'liquine', 'nombre': 'Genaro Delgado', 'cargo': 'Operario', 'telefono': '+569 6627 4984'},
    {'id': 15, 'centro': 'liquine', 'nombre': 'Gerardo Diaz', 'cargo': 'Operario', 'telefono': '+569 4099 8354'},
    {'id': 16, 'centro': 'liquine', 'nombre': 'Guido Diaz', 'cargo': 'Operario', 'telefono': '+569 9383 0562'},
    {'id': 17, 'centro': 'liquine', 'nombre': 'Iván Curiñaco', 'cargo': 'Operario', 'telefono': '+569 7750 7021'},
    {'id': 18, 'centro': 'liquine', 'nombre': 'José Cárdenas', 'cargo': 'Operario', 'telefono': '+569 4178 5650'},
    {'id': 19, 'centro': 'liquine', 'nombre': 'Miguel Cariman', 'cargo': 'Operario', 'telefono': '+569 5654 0215'},
    {'id': 20, 'centro': 'liquine', 'nombre': 'Oscar Melinao', 'cargo': 'Operario', 'telefono': '+569 9573 0288'},
    {'id': 21, 'centro': 'liquine', 'nombre': 'Celular Centro', 'cargo': 'Centro', 'telefono': '+569 3410 0884'},
    
    # TRAFÚN
    {'id': 22, 'centro': 'trafun', 'nombre': 'Víctor Hugo Pérez', 'cargo': 'Jefe de Centro', 'telefono': '+569 5738 2933'},
    {'id': 23, 'centro': 'trafun', 'nombre': 'Will Prato', 'cargo': 'Asistente de Centro', 'telefono': '+569 3070 1493'},
    {'id': 24, 'centro': 'trafun', 'nombre': 'Víctor Orrego', 'cargo': 'Asistente de Centro', 'telefono': '+569 9318 6653'},
    {'id': 25, 'centro': 'trafun', 'nombre': 'Marcelo Saldaña', 'cargo': 'Asistente de Centro', 'telefono': '+569 5580 2191'},
    {'id': 26, 'centro': 'trafun', 'nombre': 'Iván Aguayo', 'cargo': 'Asistente de Centro', 'telefono': '+569 5738 8101'},
    {'id': 27, 'centro': 'trafun', 'nombre': 'Boris Cortes', 'cargo': 'Asistente de Centro', 'telefono': '+569 5218 7753'},
    {'id': 28, 'centro': 'trafun', 'nombre': 'Operario Tarde/Noche', 'cargo': 'Operario', 'telefono': '+569 6198 7694'},
    {'id': 29, 'centro': 'trafun', 'nombre': 'Samuel Gaez', 'cargo': 'Jefe Monitoreo', 'telefono': '+569 7272 1618'},
    
    # PCC - Operarios genéricos
    {'id': 30, 'centro': 'pcc', 'nombre': 'Operario Turno Mañana', 'cargo': 'Operario', 'telefono': ''},
    {'id': 31, 'centro': 'pcc', 'nombre': 'Operario Turno Tarde', 'cargo': 'Operario', 'telefono': ''},
    {'id': 32, 'centro': 'pcc', 'nombre': 'Operario Turno Noche', 'cargo': 'Operario', 'telefono': ''},
    
    # SANTA JUANA
    {'id': 33, 'centro': 'santa-juana', 'nombre': 'Operario Turno Mañana', 'cargo': 'Operario', 'telefono': ''},
    {'id': 34, 'centro': 'santa-juana', 'nombre': 'Operario Turno Tarde', 'cargo': 'Operario', 'telefono': ''},
    {'id': 35, 'centro': 'santa-juana', 'nombre': 'Operario Turno Noche', 'cargo': 'Operario', 'telefono': ''},
    
    # RAHUE
    {'id': 36, 'centro': 'rahue', 'nombre': 'Operario Turno Mañana', 'cargo': 'Operario', 'telefono': ''},
    {'id': 37, 'centro': 'rahue', 'nombre': 'Operario Turno Tarde', 'cargo': 'Operario', 'telefono': ''},
    {'id': 38, 'centro': 'rahue', 'nombre': 'Operario Turno Noche', 'cargo': 'Operario', 'telefono': ''},
    
    # ESPERANZA
    {'id': 39, 'centro': 'esperanza', 'nombre': 'Operario Turno Mañana', 'cargo': 'Operario', 'telefono': ''},
    {'id': 40, 'centro': 'esperanza', 'nombre': 'Operario Turno Tarde', 'cargo': 'Operario', 'telefono': ''},
    {'id': 41, 'centro': 'esperanza', 'nombre': 'Operario Turno Noche', 'cargo': 'Operario', 'telefono': ''},
    
    # HUEYUSCA
    {'id': 42, 'centro': 'hueyusca', 'nombre': 'Operario Turno Mañana', 'cargo': 'Operario', 'telefono': ''},
    {'id': 43, 'centro': 'hueyusca', 'nombre': 'Operario Turno Tarde', 'cargo': 'Operario', 'telefono': ''},
    {'id': 44, 'centro': 'hueyusca', 'nombre': 'Operario Turno Noche', 'cargo': 'Operario', 'telefono': ''},
]

# Crear operarios
contador = 0
for op_data in operarios_data:
    try:
        centro = Centro.objects.get(id=op_data['centro'])
        Operario.objects.create(
            id=op_data['id'],
            centro=centro,
            nombre=op_data['nombre'],
            cargo=op_data['cargo'],
            telefono=op_data['telefono']
        )
        contador += 1
        print(f"[OK] Creado: {op_data['nombre']} ({centro.nombre})")
    except Centro.DoesNotExist:
        print(f"[ERROR] Centro no encontrado: {op_data['centro']}")
    except Exception as e:
        print(f"[ERROR] Error creando {op_data['nombre']}: {e}")

print(f"\n{contador} operarios creados exitosamente")
