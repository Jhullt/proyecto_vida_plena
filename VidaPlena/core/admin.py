from django.contrib import admin
from .models import Rol, Paciente, Medico, Administrador, Administrativo, Genero, Especialidad

admin.site.register(Rol)
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Administrativo)
admin.site.register(Administrador)
admin.site.register(Genero)
admin.site.register(Especialidad)
