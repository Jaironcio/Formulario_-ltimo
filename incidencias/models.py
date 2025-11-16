# incidencias/models.py
from django.db import models
from django.utils.text import slugify

class Centro(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # ID es string
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    # (Esto crea automáticamente el slug, ej: "Santa Juana" -> "santa-juana")
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        if not self.id:
            self.id = self.slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

# --- NUEVO MODELO: OPERARIO ---
# Vamos a guardar los operarios en la base de datos
class Operario(models.Model):
    # Usamos un ID numérico simple
    id = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    cargo = models.CharField(max_length=200)
    telefono = models.CharField(max_length=50, blank=True)
    
    # IMPORTANTE: Un operario pertenece a un Centro
    # related_name='operarios' nos permite buscar operarios desde un centro
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE, related_name='operarios')

    def __str__(self):
        return f"{self.nombre} ({self.centro.nombre})"

# --- NUEVO MODELO: INCIDENCIA ---
# La tabla principal que guarda todo el formulario
class Incidencia(models.Model):
    # --- Sección 1: Info Básica ---
    fecha_hora = models.DateTimeField()
    turno = models.CharField(max_length=50)
    centro = models.ForeignKey(Centro, on_delete=models.SET_NULL, null=True, blank=True)
    
    # --- Sección 2: Tipo ---
    tipo_incidencia = models.CharField(max_length=50, blank=True) # 'modulos' o 'sensores'

    # --- Sección 3: Módulos ---
    modulo = models.CharField(max_length=100, blank=True)
    estanque = models.CharField(max_length=100, blank=True)
    
    # Checkboxes de parámetros (guardamos una lista simple)
    parametros_afectados = models.CharField(max_length=500, blank=True) # ej: "oxigeno,temperatura"

    # Valores (los guardamos como texto para aceptar la coma ',')
    oxigeno_nivel = models.CharField(max_length=50, blank=True) # 'alta' o 'baja'
    oxigeno_valor = models.CharField(max_length=50, blank=True) # '12,2'
    
    temperatura_nivel = models.CharField(max_length=50, blank=True)
    temperatura_valor = models.CharField(max_length=50, blank=True)

    conductividad_nivel = models.CharField(max_length=50, blank=True)
    # (Conductividad no tiene valor)

    turbidez_nivel = models.CharField(max_length=50, blank=True)
    turbidez_valor = models.CharField(max_length=50, blank=True)

    # --- Sección 4: Sensores (simplificado) ---
    sistema_sensor = models.CharField(max_length=100, blank=True)
    sensor_detectado = models.CharField(max_length=100, blank=True)
    sensor_nivel = models.CharField(max_length=100, blank=True)
    sensor_valor = models.CharField(max_length=50, blank=True)

    # --- Sección 5: Riesgos ---
    tiempo_resolucion = models.IntegerField(null=True, blank=True)
    riesgo_peces = models.BooleanField(default=False)
    perdida_economica = models.BooleanField(default=False)
    riesgo_personas = models.BooleanField(default=False)
    observacion = models.TextField(blank=True)

    # --- Sección 6: Contacto ---
    operario_contacto = models.ForeignKey(Operario, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_incidencia_normalizada = models.CharField(max_length=100, blank=True)

    # Esto es para que se vea bien en el Admin
    def __str__(self):
        centro_nombre = self.centro.nombre if self.centro else "Centro no especificado"
        fecha_str = self.fecha_hora.strftime('%Y-%m-%d %H:%M') if self.fecha_hora else "Fecha no especificada"
        return f"Incidencia en {centro_nombre} - {fecha_str}"