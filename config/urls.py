"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# config/urls.py

# config/urls.py (SOLO debe tener la URL del administrador e incluir las URLs de la app)

from django.contrib import admin
from django.urls import path, include # <-- Asegúrate de importar 'include'
# from incidencias import views # <-- ELIMINA ESTA LÍNEA

urlpatterns = [
    path('admin/', admin.site.urls),
    # Incluye TODAS las rutas de la aplicación 'incidencias'
    path('', include('incidencias.urls')),
    
]