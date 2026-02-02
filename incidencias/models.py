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

    # --- Sección 4b: Falla de Plataforma ---
    plataforma = models.CharField(max_length=50, blank=True)  # 'INNOVEX' o 'SINPLANT'
    sistema_fallando = models.CharField(max_length=200, blank=True)
    tiempo_fuera_servicio = models.IntegerField(null=True, blank=True)  # minutos
    contacto_proveedor = models.BooleanField(default=False)
    razon_caida = models.TextField(blank=True)

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

# --- NUEVO MODELO: CONTROL DIARIO ---
# Tabla para registrar parámetros diarios (Temp, pH, Oxígeno) por hora
class ControlDiario(models.Model):
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE, related_name='controles_diarios')
    fecha = models.DateField()
    anio = models.IntegerField()
    semana = models.IntegerField()
    dia = models.CharField(max_length=20)  # Lunes, Martes, etc.
    responsable = models.CharField(max_length=200)
    modulo = models.CharField(max_length=100, default='Hatchery')  # Hatchery, Fry, Smolt, etc.
    
    # Registros por hora (00:00, 04:00, 08:00, 12:00, 16:00, 20:00)
    hora_00_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hora_00_ph = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    hora_00_oxigeno = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    hora_04_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hora_04_ph = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    hora_04_oxigeno = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    hora_08_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hora_08_ph = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    hora_08_oxigeno = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    hora_12_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hora_12_ph = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    hora_12_oxigeno = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    hora_16_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hora_16_ph = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    hora_16_oxigeno = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    hora_20_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hora_20_ph = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    hora_20_oxigeno = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Promedios (se calculan automáticamente)
    promedio_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    promedio_ph = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    promedio_oxigeno = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Metadata
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha', '-creado_en']
        unique_together = ['centro', 'fecha', 'modulo']
    
    def calcular_promedios(self):
        """Calcula los promedios de temperatura, pH y oxígeno"""
        horas = ['00', '04', '08', '12', '16', '20']
        
        # Calcular promedio temperatura
        temps = [getattr(self, f'hora_{h}_temp') for h in horas if getattr(self, f'hora_{h}_temp') is not None]
        self.promedio_temp = sum(temps) / len(temps) if temps else None
        
        # Calcular promedio pH
        phs = [getattr(self, f'hora_{h}_ph') for h in horas if getattr(self, f'hora_{h}_ph') is not None]
        self.promedio_ph = sum(phs) / len(phs) if phs else None
        
        # Calcular promedio oxígeno
        oxigenos = [getattr(self, f'hora_{h}_oxigeno') for h in horas if getattr(self, f'hora_{h}_oxigeno') is not None]
        self.promedio_oxigeno = sum(oxigenos) / len(oxigenos) if oxigenos else None
    
    def save(self, *args, **kwargs):
        # Calcular promedios antes de guardar
        self.calcular_promedios()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Control Diario - {self.centro.nombre} - {self.fecha} - {self.modulo}"

# --- NUEVO MODELO: REPORTE DE CÁMARAS ---
# Tabla para registrar el estado diario de las cámaras de los 4 centros
class ReporteCamaras(models.Model):
    fecha = models.DateField()
    turno = models.CharField(max_length=20)  # Mañana, Tarde, Noche
    responsable = models.CharField(max_length=200)
    
    # Río Pescado
    rio_pescado_tiene_incidencias = models.BooleanField(default=False)
    rio_pescado_descripcion = models.TextField(default='No se detectaron novedades durante el monitoreo')
    
    # Collín
    collin_tiene_incidencias = models.BooleanField(default=False)
    collin_descripcion = models.TextField(default='No se detectaron novedades durante el monitoreo')
    
    # Lican
    lican_tiene_incidencias = models.BooleanField(default=False)
    lican_descripcion = models.TextField(default='No se detectaron novedades durante el monitoreo')
    
    # Trafún
    trafun_tiene_incidencias = models.BooleanField(default=False)
    trafun_descripcion = models.TextField(default='No se detectaron novedades durante el monitoreo')
    
    # Metadata
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha', '-creado_en']
        unique_together = ['fecha', 'turno']
        verbose_name = 'Reporte de Cámaras'
        verbose_name_plural = 'Reportes de Cámaras'
    
    def __str__(self):
        return f"Reporte Cámaras - {self.fecha} - {self.turno}"


# --- MODELOS PARA SISTEMA DE SENSORES (IDEAL CONTROL) ---

class SensorConfig(models.Model):
    """Configuración de sensores por centro - basado en Alertas_IdealControl.xlsm"""
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE, related_name='sensores')
    sistema = models.CharField(max_length=100)  # MEE, Efluente, Turbidez y CO2, etc.
    equipo = models.CharField(max_length=200)  # Flujómetro pozo 1, NTU Módulo 200, etc.
    tipo_medicion = models.CharField(max_length=100)  # CAUDAL, NIVEL, NTU, CO2, etc.
    limite_min = models.CharField(max_length=50, blank=True)
    limite_max = models.CharField(max_length=50, blank=True)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)  # Para ordenar sensores en el formulario
    
    class Meta:
        ordering = ['centro', 'sistema', 'orden', 'equipo']
        unique_together = ['centro', 'sistema', 'equipo']
        verbose_name = 'Configuración de Sensor'
        verbose_name_plural = 'Configuraciones de Sensores'
    
    def __str__(self):
        return f"{self.centro.nombre} - {self.sistema} - {self.equipo}"


class MonitoreoSensores(models.Model):
    """Registro diario de monitoreo de sensores por turno"""
    ESTADO_CHOICES = [
        ('NORMAL', 'Normal'),
        ('ALTO', 'Alto - Sobre límite'),
        ('BAJO', 'Bajo - Bajo límite'),
        ('N/A', 'No aplica')
    ]
    
    TURNO_CHOICES = [
        ('MAÑANA', 'Mañana'),
        ('TARDE', 'Tarde'),
        ('NOCHE', 'Noche')
    ]
    
    fecha = models.DateField()
    hora_inicio = models.TimeField(null=True, blank=True, help_text="Hora de inicio de la incidencia")
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)
    sensor = models.ForeignKey(SensorConfig, on_delete=models.CASCADE)
    
    # Estado del sensor en este turno
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='NORMAL')
    
    # Observación específica para este sensor/turno
    observacion = models.TextField(blank=True)
    
    # Metadata
    responsable = models.CharField(max_length=100)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha', 'turno', 'centro', 'sensor']
        unique_together = ['fecha', 'turno', 'centro', 'sensor']
        verbose_name = 'Monitoreo de Sensor'
        verbose_name_plural = 'Monitoreos de Sensores'
    
    def __str__(self):
        return f"{self.fecha} - {self.turno} - {self.centro.nombre} - {self.sensor.equipo}: {self.estado}"


class ReportePlataforma(models.Model):
    """Registro de fallas de plataformas INNOVEX, SINPLANT e IDEAL CONTROL"""
    PLATAFORMA_CHOICES = [
        ('INNOVEX', 'INNOVEX'),
        ('SINPLANT', 'SINPLANT'),
        ('IDEAL CONTROL', 'IDEAL CONTROL')
    ]
    
    TURNO_CHOICES = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche')
    ]
    
    CONTACTO_PROVEEDOR_CHOICES = [
        ('no', 'No se contactó'),
        ('si', 'Sí, con respuesta'),
        ('sin_respuesta', 'Sí, sin respuesta')
    ]
    
    UNIDAD_TIEMPO_CHOICES = [
        ('minutos', 'Minutos'),
        ('dias', 'Días')
    ]
    
    # Información básica
    fecha_hora = models.DateTimeField()
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE, related_name='reportes_plataforma')
    
    # Detalles de la falla
    plataforma = models.CharField(max_length=20, choices=PLATAFORMA_CHOICES)
    sistema_fallando = models.CharField(max_length=200)
    tiempo_fuera_servicio = models.IntegerField(help_text='Duración del tiempo fuera de servicio')
    unidad_tiempo = models.CharField(max_length=10, choices=UNIDAD_TIEMPO_CHOICES, default='minutos')
    contacto_proveedor = models.CharField(max_length=20, choices=CONTACTO_PROVEEDOR_CHOICES, default='no')
    razon_caida = models.TextField()
    
    # Evaluación de impacto
    riesgo_peces = models.BooleanField(default=False)
    perdida_economica = models.BooleanField(default=False)
    
    # Información adicional
    responsable = models.CharField(max_length=200)
    observacion = models.TextField(blank=True)
    
    # Metadata
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_hora', '-creado_en']
        verbose_name = 'Reporte de Plataforma'
        verbose_name_plural = 'Reportes de Plataformas'
    
    def __str__(self):
        return f"{self.plataforma} - {self.centro.nombre} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"