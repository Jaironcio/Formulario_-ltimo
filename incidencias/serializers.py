# incidencias/serializers.py
from rest_framework import serializers
from .models import Incidencia, Centro

class IncidenciaSerializer(serializers.ModelSerializer):
    # Permitir que el campo centro acepte el ID del centro (que es string)
    centro = serializers.PrimaryKeyRelatedField(queryset=Centro.objects.all())
    
    class Meta:
        model = Incidencia
        # Le decimos que "traduzca" todos los campos
        # que definimos en el modelo Incidencia
        fields = '__all__'