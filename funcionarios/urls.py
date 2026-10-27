from django.urls import path

from . import views

app_name = "funcionario" 

urlpatterns = [
    path('',views.inicio,name="funcionario"),
    path('registro/',views.registro, name="registro"),
    path('base/',views.base),
    path('iniciarSesion/', views.iniciarSesion, name='iniciar_sesion'),

    #Rutas para recuperar contraseña
    path('recuperarContrasena/', views.recuperarContrasena, name='password_reset'),#ingresar el correo
    path('recuperarContrasena/enviado/', views.recuperacionEnviada, name='password_reset_done'),#confirmacion solicitud

    #--- crear contrasena nueva
    #--- uidb64 identificador de la cuenta doficiado para poder incluirlo en una url
    #--- token es el valor de seguridad que django genera y valida para esta solicitud
    path('restablecerContrasena/<uidb64>/<token>/',views.confirmarContrasena,name='password_reset_confirm',),

    path('restablecerContrasena/completa/',views.contrasenaRestablecida,name='password_reset_complete'), # confirmacion del cambio

    
    path('cerrarSesion/', views.cerrarSesion, name='cerrar_sesion'),
    path('perfil/<str:username>',views.perfil,name="perfil"),
    path('agregarNumero/',views.modificarFuncionario,name="agregarNumero")

]
