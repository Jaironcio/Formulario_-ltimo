# incidencias/management/commands/poblar_contactos_centros.py
from django.core.management.base import BaseCommand
from incidencias.models import Centro, Operario

class Command(BaseCommand):
    help = 'Pobla los operarios/contactos de cada centro basado en NUMEROS DE TELEFONO (PISCICULTURAS).txt'

    def handle(self, *args, **options):
        self.stdout.write('Poblando contactos por centro...\n')
        
        # Datos de contactos por centro
        contactos_data = {
            'cipreses': [
                {'id': 201, 'nombre': 'Roberto Alarcón', 'cargo': 'Jefe de Centro', 'telefono': '+569 6155 6741'},
                {'id': 202, 'nombre': 'Claudio Zúñiga', 'cargo': 'Asistente de Centro', 'telefono': '+569 8582 2564'},
                {'id': 203, 'nombre': 'Dominique Cabrera', 'cargo': 'Asistente de Centro', 'telefono': '+569 6181 0024'},
                {'id': 204, 'nombre': 'Jorge Vidal', 'cargo': 'Asistente de Centro', 'telefono': '+569 5361 2276'},
                {'id': 205, 'nombre': 'Marcelo Mena', 'cargo': 'Asistente de Centro', 'telefono': '+569 9884 2121'},
                {'id': 206, 'nombre': 'Rodrigo López', 'cargo': 'Asistente de Centro', 'telefono': '+569 6721 4135'},
                {'id': 207, 'nombre': 'Sebastián Peralta', 'cargo': 'Asistente de Centro', 'telefono': '+569 8475 6452'},
                {'id': 208, 'nombre': 'Técnicos turno día', 'cargo': 'Técnico', 'telefono': '65 256 8165'},
                {'id': 209, 'nombre': 'Operarios turno Tarde/Noche', 'cargo': 'Operario', 'telefono': '+569 8932 3982'},
            ],
            'liquine': [
                {'id': 301, 'nombre': 'Roberto Parra', 'cargo': 'Jefe de Centro', 'telefono': '+569 4471 6465'},
                {'id': 302, 'nombre': 'Manuel Krebs', 'cargo': 'Asistente de Centro', 'telefono': '+569 8832 4988'},
                {'id': 303, 'nombre': 'Guillermo Contreras', 'cargo': 'Asistente de Centro', 'telefono': '+569 4093 5028'},
                {'id': 304, 'nombre': 'Diego Pichun', 'cargo': 'Asistente de Centro', 'telefono': '+569 4421 4065'},
                {'id': 305, 'nombre': 'Genaro Delgado', 'cargo': 'Operario', 'telefono': '+569 6627 4984'},
                {'id': 306, 'nombre': 'Gerardo Diaz', 'cargo': 'Operario', 'telefono': '+569 4099 8354'},
                {'id': 307, 'nombre': 'Guido Diaz', 'cargo': 'Operario', 'telefono': '+569 9383 0562'},
                {'id': 308, 'nombre': 'Iván Curiñaco', 'cargo': 'Operario', 'telefono': '+569 7750 7021'},
                {'id': 309, 'nombre': 'José Cárdenas', 'cargo': 'Operario', 'telefono': '+569 4178 5650'},
                {'id': 310, 'nombre': 'Miguel Cariman', 'cargo': 'Operario', 'telefono': '+569 5654 0215'},
                {'id': 311, 'nombre': 'Oscar Melinao', 'cargo': 'Operario', 'telefono': '+569 9573 0288'},
                {'id': 312, 'nombre': 'Celular Centro', 'cargo': 'Contacto General', 'telefono': '+569 3410 0884'},
            ],
            'trafun': [
                {'id': 401, 'nombre': 'Víctor Hugo Pérez', 'cargo': 'Jefe de Centro', 'telefono': '+569 5738 2933'},
                {'id': 402, 'nombre': 'Will Prato', 'cargo': 'Asistente de Centro', 'telefono': '+569 3070 1493'},
                {'id': 403, 'nombre': 'Víctor Orrego', 'cargo': 'Asistente de Centro', 'telefono': '+569 9318 6653'},
                {'id': 404, 'nombre': 'Marcelo Saldaña', 'cargo': 'Asistente de Centro', 'telefono': '+569 5580 2191'},
                {'id': 405, 'nombre': 'Iván Aguayo', 'cargo': 'Asistente de Centro', 'telefono': '+569 5738 8101'},
                {'id': 406, 'nombre': 'Boris Cortes', 'cargo': 'Asistente de Centro', 'telefono': '+569 5218 7753'},
                {'id': 407, 'nombre': 'Operario Tarde/Noche', 'cargo': 'Operario', 'telefono': '+569 6198 7694'},
                {'id': 408, 'nombre': 'Samuel Gaez', 'cargo': 'Jefe Monitoreo', 'telefono': '+569 7272 1618'},
            ],
        }
        
        total_creados = 0
        total_actualizados = 0
        
        for centro_slug, contactos in contactos_data.items():
            try:
                centro = Centro.objects.get(id=centro_slug)
                self.stdout.write(f'\n[*] Centro: {centro.nombre}')
                
                for contacto in contactos:
                    operario, created = Operario.objects.update_or_create(
                        id=contacto['id'],
                        defaults={
                            'nombre': contacto['nombre'],
                            'cargo': contacto['cargo'],
                            'telefono': contacto['telefono'],
                            'centro': centro
                        }
                    )
                    
                    if created:
                        self.stdout.write(f'  [+] Creado: {contacto["nombre"]} - {contacto["cargo"]}')
                        total_creados += 1
                    else:
                        self.stdout.write(f'  [~] Actualizado: {contacto["nombre"]} - {contacto["cargo"]}')
                        total_actualizados += 1
                        
            except Centro.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'[!] Centro "{centro_slug}" no encontrado. Saltando...'))
                continue
        
        self.stdout.write(self.style.SUCCESS(f'\n[OK] Proceso completado:'))
        self.stdout.write(self.style.SUCCESS(f'   - {total_creados} operarios creados'))
        self.stdout.write(self.style.SUCCESS(f'   - {total_actualizados} operarios actualizados'))
