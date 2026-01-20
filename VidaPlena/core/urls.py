from django.urls import path
from .views import home, login, registro_paciente, pacientes, medicos, administrador, administrativos, logout, ver_usuarios, eliminar_usuario, editar_usuario, crear_usuario

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('registrarse/', registro_paciente, name='registrarse'),
    path('pacientes/', pacientes, name='pacientes'),
    path('medicos/', medicos, name='medicos'),
    path('administrador/', administrador, name='administrador'),
    path('administrativos/', administrativos, name='administrativos'),
    path('logout/', logout, name='logout'),
    path('gestion-usuarios/', ver_usuarios, name='ver_usuarios'),
    path('eliminar-usuario/<str:tipo>/<str:rut>/', eliminar_usuario, name='eliminar_usuario'),
    path('editar-usuario/', editar_usuario, name='editar_usuario'),
    path('crear-usuario/', crear_usuario, name='crear_usuario'),
]
