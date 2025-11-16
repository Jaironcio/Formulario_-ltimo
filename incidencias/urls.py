# incidencias/urls.py (Versión con Selector)

from django.urls import path
from . import views 

urlpatterns = [
    # 1. RUTA DE INICIO: Ahora apunta al selector
    path('', views.vista_selector_centro, name='home'), 
    
    # 2. RUTAS DEL FORMULARIO PCC
    # Ruta para "crear" (apunta a la vista renombrada)
    path('formulario/pcc/', views.vista_formulario_pcc, name='formulario_pcc'),
    # Ruta para "editar" PCC (apunta a la misma vista renombrada)
    path('formulario/pcc/editar/<int:pk>/', views.vista_formulario_pcc, name='editar_incidencia_pcc'), 

    # 3. RUTAS DEL FORMULARIO SANTA JUANA
    path('formulario/santa-juana/', views.vista_formulario_santa_juana, name='formulario_santa_juana'),
    path('formulario/santa-juana/editar/<int:pk>/', views.vista_formulario_santa_juana, name='editar_incidencia_santa_juana'),
    
    # 4. RUTA INTELIGENTE DE EDICIÓN (detecta el centro y redirige)
    path('editar/<int:pk>/', views.vista_editar_incidencia_inteligente, name='editar_incidencia'),
    
    # 5. OTRAS VISTAS (Reporte y Dashboard)
    path('reporte/', views.vista_reporte, name='reporte'),
    path('dashboard/', views.vista_dashboard, name='dashboard'),
    
    # 6. APIs (No cambian)
    path('api/registrar-incidencia/', views.registrar_incidencia_api, name='api-registrar-incidencia'),
    path('api/incidencia/<int:pk>/delete/', views.delete_incidencia_api, name='api-delete-incidencia'),
    path('api/incidencia/<int:pk>/update/', views.update_incidencia_api, name='api-update-incidencia'),
]