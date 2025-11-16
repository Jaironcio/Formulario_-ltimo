# incidencias/admin.py
from django.contrib import admin
from .models import Centro, Operario, Incidencia

# Personalizar el admin de Centro
@admin.register(Centro)
class CentroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'slug')
    search_fields = ('nombre', 'slug')

# Personalizar el admin de Operario
@admin.register(Operario)
class OperarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'cargo', 'centro', 'telefono')
    list_filter = ('centro', 'cargo')
    search_fields = ('nombre', 'cargo')

# Personalizar el admin de Incidencia
@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_centro_nombre', 'fecha_hora', 'turno', 'modulo', 'tipo_incidencia', 'riesgo_peces')
    list_filter = ('centro', 'turno', 'tipo_incidencia', 'riesgo_peces', 'riesgo_personas')
    search_fields = ('centro__nombre', 'modulo', 'estanque', 'observacion', 'tipo_incidencia_normalizada')
    date_hierarchy = 'fecha_hora'
    
    def get_centro_nombre(self, obj):
        return obj.centro.nombre if obj.centro else "Sin centro"
    get_centro_nombre.short_description = 'Centro'
    get_centro_nombre.admin_order_field = 'centro'