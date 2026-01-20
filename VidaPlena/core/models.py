from django.db import models
from django.contrib.auth.models import User

# ROLES
class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_rol
    
    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

# GENERO
class Genero(models.Model):
    genero = models.CharField(max_length=50)

    def __str__(self):
        return self.genero

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"

# ESPECIALIDAD
class Especialidad(models.Model):
    especialidad = models.CharField(max_length=50)

    def __str__(self):
        return self.especialidad

    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"

# PACIENTES
class Paciente(models.Model):
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True, blank=True)

    correo_paciente = models.EmailField(unique=True)
    password_paciente = models.CharField(max_length=128) 
    rut_paciente = models.CharField(max_length=9, unique=True)
    nombre_paciente = models.CharField(max_length=50)
    apellido_paciente = models.CharField(max_length=50)
    fecha_nacimiento_paciente = models.DateField()
    residencia_paciente = models.CharField(max_length=100)
    telefono_paciente = models.CharField(max_length=15)

    def __str__(self):
        return f"Paciente: {self.nombre_paciente} {self.apellido_paciente}"
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

# MEDICOS
class Medico(models.Model):
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True, blank=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, null=True, blank=True)

    correo_medico = models.EmailField(unique=True)
    password_medico = models.CharField(max_length=128)
    rut_medico = models.CharField(max_length=9, unique=True)
    nombre_medico = models.CharField(max_length=50)
    apellido_medico = models.CharField(max_length=50)
    telefono_medico = models.CharField(max_length=15)

    def __str__(self):
        return f"Medico: {self.nombre_medico} {self.apellido_medico}"
    
    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"

# ADMINISTRATIVOS
class Administrativo(models.Model):
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True, blank=True)

    correo_administrativo = models.EmailField(unique=True)
    password_administrativo = models.CharField(max_length=128)
    rut_administrativo = models.CharField(max_length=9, unique=True)
    nombre_administrativo = models.CharField(max_length=50)
    apellido_administrativo = models.CharField(max_length=50)
    telefono_administrativo = models.CharField(max_length=15)

    def __str__(self):
        return f"Administrativo: {self.nombre_administrativo} {self.apellido_administrativo}"
    
    class Meta:
        verbose_name = "Administrativo"
        verbose_name_plural = "Administrativos"
    
# ADMINISTRADOR
class Administrador(models.Model):
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True, blank=True)

    correo_administrador = models.EmailField(unique=True)
    password_administrador = models.CharField(max_length=128)
    rut_administrador = models.CharField(max_length=9, unique=True)
    nombre_administrador = models.CharField(max_length=50)
    apellido_administrador = models.CharField(max_length=50)
    telefono_administrador = models.CharField(max_length=15)

    def __str__(self):
        return f"Administrador: {self.nombre_administrador} {self.apellido_administrador}"
    
    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"