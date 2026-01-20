from django.urls import path
from .views import home, login, registro_paciente, pacientes, medicos, administrador, administrativos, logout

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('registrarse/', registro_paciente, name='registrarse'),
    path('pacientes/', pacientes, name='pacientes'),
    path('medicos/', medicos, name='medicos'),
    path('administrador/', administrador, name='administrador'),
    path('administrativos/', administrativos, name='administrativos'),
    path('logout/', logout, name='logout'),
]
