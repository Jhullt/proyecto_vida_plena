from django.shortcuts import render, redirect
from .models import Paciente, Medico, Administrativo, Administrador, Genero, Rol

def home(request):
    return render(request, 'home.html')

# VISTAS NAVEGACION PROTEGIDAS

def pacientes(request):
    if not request.session.get('usuario_id') or request.session.get('rol_id') != 1:
        request.session.flush()
        return redirect('login')
    return render(request, 'pacientes.html')

def medicos(request):
    if not request.session.get('usuario_id') or request.session.get('rol_id') != 2:
        request.session.flush()
        return redirect('login')
    return render(request, 'medicos.html')

def administrativos(request):
    if not request.session.get('usuario_id') or request.session.get('rol_id') != 3:
        request.session.flush()
        return redirect('login')
    return render(request, 'administrativos.html')

def administrador(request):
    if not request.session.get('usuario_id') or request.session.get('rol_id') != 4:
        request.session.flush()
        return redirect('login')
    return render(request, 'administrador.html')

# FORMULARIO REGISTRO

def registro_paciente(request):
    lista_generos = Genero.objects.all()

    if request.method == 'POST':

        datos_enviados = request.POST 
        
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        telefono = request.POST.get('telefono')
        residencia = request.POST.get('residencia')
        password = request.POST.get('password')
        genero_id = request.POST.get('genero')

        # VALIDAR RUT REPETIDO
        existe_rut = (
            Paciente.objects.filter(rut_paciente=rut).exists() or
            Medico.objects.filter(rut_medico=rut).exists() or
            Administrativo.objects.filter(rut_administrativo=rut).exists() or
            Administrador.objects.filter(rut_administrador=rut).exists()
        )
        if existe_rut:
            return render(request, 'registrarse.html', {
                'generos': lista_generos, 
                'error': 'Este RUT ya está registrado.',
                'datos': datos_enviados
            })

        # VALIDAR CORREO REPETIDO
        existe_correo = (
            Paciente.objects.filter(correo_paciente=email).exists() or
            Medico.objects.filter(correo_medico=email).exists() or
            Administrativo.objects.filter(correo_administrativo=email).exists() or
            Administrador.objects.filter(correo_administrador=email).exists()
        )
        if existe_correo:
            return render(request, 'registrarse.html', {
                'generos': lista_generos, 
                'error': 'Este correo ya está en uso.',
                'datos': datos_enviados
            })

        try:
            genero_obj = Genero.objects.get(id=genero_id)
            rol_obj = Rol.objects.get(id=1)

            nuevo_paciente = Paciente(
                rut_paciente=rut,
                nombre_paciente=nombre,
                apellido_paciente=apellido,
                correo_paciente=email,
                fecha_nacimiento_paciente=fecha_nacimiento,
                telefono_paciente=telefono,
                residencia_paciente=residencia,
                password_paciente=password,
                genero=genero_obj,
                rol=rol_obj
            )
            nuevo_paciente.save()
            return redirect('login')
            
        except Exception as e:
            return render(request, 'registrarse.html', {
                'generos': lista_generos, 
                'error': 'Error al procesar el registro.',
                'datos': datos_enviados
            })

    return render(request, 'registrarse.html', {'generos': lista_generos})

# FUNCION LOGIN

def login(request):
    if request.method == 'POST':
        correo_ingresado = request.POST.get('email')
        pass_ingresada = request.POST.get('password')

        user = (
            Paciente.objects.filter(correo_paciente=correo_ingresado, password_paciente=pass_ingresada).first() or
            Medico.objects.filter(correo_medico=correo_ingresado, password_medico=pass_ingresada).first() or
            Administrativo.objects.filter(correo_administrativo=correo_ingresado, password_administrativo=pass_ingresada).first() or
            Administrador.objects.filter(correo_administrador=correo_ingresado, password_administrador=pass_ingresada).first()
        )

        if user:
            request.session['usuario_id'] = user.id
            request.session['rol_id'] = user.rol_id
            
            if hasattr(user, 'nombre_paciente'):
                nombre = f"{user.nombre_paciente} {user.apellido_paciente}"
            elif hasattr(user, 'nombre_medico'):
                nombre = f"{user.nombre_medico} {user.apellido_medico}"

                if user.especialidad:
                    request.session['usuario_especialidad'] = user.especialidad.especialidad
                else:
                    request.session['usuario_especialidad'] = "Médico General"
            elif hasattr(user, 'nombre_administrativo'):
                nombre = f"{user.nombre_administrativo} {user.apellido_administrativo}"
            else:
                nombre = f"{user.nombre_administrador} {user.apellido_administrador}"
            
            request.session['usuario_completo'] = nombre

            if user.rol_id == 1: return redirect('pacientes')
            elif user.rol_id == 2: return redirect('medicos')
            elif user.rol_id == 3: return redirect('administrativos')
            elif user.rol_id == 4: return redirect('administrador')

        return render(request, 'login.html', {'error': 'Correo o contraseña incorrectos.'})

    return render(request, 'login.html')

# CERRAR SESION

def logout(request):
    request.session.flush()
    return redirect('login')