from django.urls import path

from . import views

app_name = "recordatorios" 

urlpatterns = [
    path('crear_recordatorio/<str:uuid>/', views.crear_recordatorio, name="crear_recordatorio"),
    path('modificar_recordatorio/<uuid:uuid>/', views.modi_recordatorio, name="mod_recordatorio"),
    path('eliminar_recordatorio/<uuid:uuid>/', views.eliminar_recordatorio, name="eliminar_recordatorio"),
    path('marcar_cumplido/<int:fecha_id>/', views.marcar_cumplido, name='marcar_cumplido'),
    path('calendario/<uuid:uuid>/eventos/', views.eventos_calendario, name='eventos_calendario'),
]
