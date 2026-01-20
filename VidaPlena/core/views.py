from django.shortcuts import render, redirect, get_object_or_404
from .models import Paciente, Medico, Administrativo, Administrador, Genero, Rol, Especialidad
from django.contrib import messages
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

# USUARIOS - ADMINISTRADOR

def ver_usuarios(request):
    if not request.session.get('usuario_id') or request.session.get('rol_id') != 4:
        request.session.flush()
        return redirect('login')

    tipo = request.GET.get('tipo', 'pacientes')
    
    usuarios = []

    if tipo == 'pacientes':
        usuarios = Paciente.objects.all()
    
    elif tipo == 'medicos':
        usuarios = Medico.objects.select_related('especialidad').all()
    
    elif tipo == 'administrativos':
        usuarios = Administrativo.objects.all()
    
    elif tipo == 'administradores':
        usuarios = Administrador.objects.all()

    datos = {
        'usuarios': usuarios,
        'tipo': tipo,
    }
    
    return render(request, 'usuarios.html', datos)

# BORRAR USUARIOS - ADMINISTRADOR

def eliminar_usuario(request, tipo, rut):

    if request.session.get('rol_id') != 4:
        return redirect('login')

    if tipo == 'pacientes':
        usuario = get_object_or_404(Paciente, rut_paciente=rut)
    elif tipo == 'medicos':
        usuario = get_object_or_404(Medico, rut_medico=rut)
    elif tipo == 'administrativos':
        usuario = get_object_or_404(Administrativo, rut_administrativo=rut)
    elif tipo == 'administradores':
        usuario = get_object_or_404(Administrador, rut_administrador=rut)
    
    usuario.delete()

    return redirect(f'/gestion-usuarios/?tipo={tipo}')

# MODIFICAR USUARIO - ADMINISTRADOR

def editar_usuario(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo_usuario')
        rut_orig = request.POST.get('rut_original')
        rut_nuevo = request.POST.get('nuevo_rut')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        password = request.POST.get('nueva_password')

        try:
  
            if tipo == 'pacientes':
                u = Paciente.objects.get(rut_paciente=rut_orig)
                u.rut_paciente = rut_nuevo
                u.nombre_paciente, u.apellido_paciente, u.correo_paciente = nombre, apellido, correo
                if password: u.contrasena_paciente = password
            elif tipo == 'medicos':
                u = Medico.objects.get(rut_medico=rut_orig)
                u.rut_medico = rut_nuevo
                u.nombre_medico, u.apellido_medico, u.correo_medico = nombre, apellido, correo
                if password: u.contrasena_medico = password
            elif tipo == 'administrativos':
                u = Administrativo.objects.get(rut_administrativo=rut_orig)
                u.rut_administrativo = rut_nuevo
                u.nombre_administrativo, u.apellido_administrativo, u.correo_administrativo = nombre, apellido, correo
                if password: u.contrasena_administrativo = password
            elif tipo == 'administradores':
                u = Administrador.objects.get(rut_administrador=rut_orig)
                u.rut_administrador = rut_nuevo
                u.nombre_administrador, u.apellido_administrador, u.correo_administrador = nombre, apellido, correo
                if password: u.contrasena_administrador = password
            
            u.save()
        except Exception as e:
            print(f"Error al editar: {e}")

    return redirect(f'/gestion-usuarios/?tipo={tipo}')

# CREAR USUARIO - ADMINISTRADOR

def crear_usuario(request):
    especialidades = Especialidad.objects.all()
    roles_db = Rol.objects.all()
    generos_db = Genero.objects.all()
    
    if request.method == 'POST':
        id_rol = request.POST.get('rol') 
        rut = request.POST.get('rut', '').strip()
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        genero_id = request.POST.get('genero')
        telefono = request.POST.get('telefono', '').strip()
        correo = request.POST.get('correo', '').strip().lower()
        password = request.POST.get('password')

        try:
            rut_existe = (
                Administrador.objects.filter(rut_administrador=rut).exists() or
                Administrativo.objects.filter(rut_administrativo=rut).exists() or
                Medico.objects.filter(rut_medico=rut).exists()
            )
            if rut_existe:
                raise Exception(f"El RUT {rut} ya se encuentra registrado.")

            correo_existe = (
                Administrador.objects.filter(correo_administrador=correo).exists() or
                Administrativo.objects.filter(correo_administrativo=correo).exists() or
                Medico.objects.filter(correo_medico=correo).exists()
            )
            if correo_existe:
                raise Exception(f"El correo {correo} ya está en uso.")

            rol_instancia = Rol.objects.get(id=id_rol)
            genero_instancia = Genero.objects.get(id=genero_id)
            nombre_rol_limpio = rol_instancia.nombre_rol.strip().lower()

            if nombre_rol_limpio == 'administrador':
                Administrador.objects.create(
                    rut_administrador=rut, nombre_administrador=nombre,
                    apellido_administrador=apellido, genero=genero_instancia,
                    rol=rol_instancia, telefono_administrador=telefono,
                    correo_administrador=correo, password_administrador=password
                )
            elif nombre_rol_limpio == 'administrativo':
                Administrativo.objects.create(
                    rut_administrativo=rut, nombre_administrativo=nombre,
                    apellido_administrativo=apellido, genero=genero_instancia,
                    rol=rol_instancia, telefono_administrativo=telefono,
                    correo_administrativo=correo, password_administrativo=password
                )
            elif nombre_rol_limpio == 'medico':
                id_esp = request.POST.get('especialidad')
                esp_instancia = Especialidad.objects.get(id=id_esp)
                Medico.objects.create(
                    rut_medico=rut, nombre_medico=nombre,
                    apellido_medico=apellido, genero=genero_instancia,
                    rol=rol_instancia, especialidad=esp_instancia,
                    telefono_medico=telefono, correo_medico=correo,
                    password_medico=password
                )

            messages.success(request, f"Usuario {nombre} {apellido} creado correctamente.")
            return render(request, 'crear_usuario.html', {
                'especialidades': especialidades,
                'roles': roles_db,
                'generos': generos_db
            })

        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'crear_usuario.html', {
                'especialidades': especialidades,
                'roles': roles_db,
                'generos': generos_db,
                'datos': request.POST 
            })

    return render(request, 'crear_usuario.html', {
        'especialidades': especialidades, 'roles': roles_db, 'generos': generos_db
    })