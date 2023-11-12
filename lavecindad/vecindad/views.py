import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from vecindad.decorators import anonymous_required, usuario_presidente_required, usuario_residente_required
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from .forms import AprobacionProyectoForm, EditProfileForm, MensajeModalForm, NoticiaForm, PostulacionProyectoForm, RegistroForm, InicioSesionForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import MensajeForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


# Create your views here.
import os

def descargar_pdf(request):
    # Ruta al archivo PDF
    pdf_path = os.path.join('media/pdf', 'certificado_residencia.pdf')  # Reemplaza con la ruta real de tu archivo

    # Verifica si el archivo PDF existe
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="certificado_residencia.pdf"'
            return response
    else:
        # Manejar el caso en que el archivo no existe
        return HttpResponse('El archivo PDF no se encontró.', status=404)


@csrf_exempt
@anonymous_required
def registro(request):
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            junta_de_vecinos = form.cleaned_data.get('junta_de_vecinos')
            usuario.junta_de_vecinos = junta_de_vecinos  # Asigna el objeto JuntaDeVecinos completo
            usuario.nombre_junta = junta_de_vecinos.nombre  # Asigna el nombre de la junta
            usuario.save()

            # Envía un correo electrónico de registro exitoso a través del servidor SMTP de Gmail
            subject = 'Registro Exitoso'
            message = 'Gracias por registrarte en nuestra plataforma.'
            from_email = settings.EMAIL_HOST_USER  # Debes configurar EMAIL_HOST_USER con tu dirección de Gmail
            to_email = [usuario.email]

            send_mail(subject, message, from_email, to_email, fail_silently=False)
            
            login(request, usuario)
            messages.success(request, 'Registrado exitosamente')

            return redirect('iniciar_sesion')  # Redirige al inicio de sesión
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}", extra_tags='error-message')
            return redirect('registro')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})

@csrf_exempt
@anonymous_required
def registro_presidente(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            presidente = form.save(commit=False)
            junta_id_sede = form.cleaned_data.get('id_sede')  # Obtén el valor ingresado
            try:
                junta_de_vecinos = JuntaDeVecinos.objects.get(id_sede=junta_id_sede)
            except JuntaDeVecinos.DoesNotExist:
                messages.error(request, "ID de Junta de Vecinos no válida.")
                return redirect('registro_presidente')
            
            # Asigna la id_sede ingresada directamente al presidente
            presidente.junta_de_vecinos = junta_de_vecinos
            presidente.save()

            # Envía un correo electrónico de registro exitoso a través del servidor SMTP de Gmail
            subject = 'Registro Exitoso'
            message = 'Gracias por registrarte en nuestra plataforma.'
            from_email = settings.EMAIL_HOST_USER  # Debes configurar EMAIL_HOST_USER con tu dirección de Gmail
            to_email = [presidente.email]

            send_mail(subject, message, from_email, to_email, fail_silently=False)

            login(request, presidente)
            messages.success(request, 'Registrado exitosamente')

            return redirect('iniciar_sesion') 
            
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}", extra_tags='error-message')
            
            # Verifica si hay un error específico para el campo 'id_sede' y agrega un mensaje personalizado
            junta_id_sede_error = form.errors.get('id_sede')
            if junta_id_sede_error:
                messages.error(request, "ID de Junta de Vecinos no válida.", extra_tags='error-message')

            return redirect('registro_presidente')



    else:
        form = RegistroForm()

    return render(request, 'registro_presidente.html', {'form': form})


@csrf_exempt
@anonymous_required
def sesion(request):
    if 'registro_exitoso' in request.GET:
        messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
    if request.method == 'POST':
        formlog = InicioSesionForm(request, request.POST)
        if formlog.is_valid():
            nombre_usuario = formlog.cleaned_data.get("username")
            contra = formlog.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=contra)
            if usuario is not None:
                login(request, usuario)

                if usuario.id_sede:
                    # El usuario tiene un id_sede, por lo que es presidente
                    return redirect('noticias_junta_presidente')
                else:
                    junta_de_vecinos = usuario.junta_de_vecinos
                    # El usuario no es presidente, redirigir a la página de noticias de su junta de vecinos
                    if junta_de_vecinos:
                        return redirect('noticias_junta')
                    else:
                        # Maneja el caso en que el usuario no pertenezca a ninguna junta de vecinos
                        return HttpResponse("No perteneces a ninguna junta de vecinos.")
            else:
                messages.error(request, "Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")
        else:
            error_message = 'Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.'
            messages.error(request, error_message)
            return redirect('iniciar_sesion')
    
    else:
        formlog = InicioSesionForm()

    return render(request, 'iniciar_sesion.html', {'formlog': InicioSesionForm()})




@csrf_exempt
@usuario_residente_required
def noticias_junta(request):
    usuario = request.user
    junta_de_vecinos = usuario.junta_de_vecinos
    noticias = NoticiaJuntaVecinos.objects.filter(junta_de_vecinos=junta_de_vecinos).order_by('-fecha_publicacion')
    return render(request, 'noticias_junta.html', {'noticias': noticias, 'junta_de_vecinos': junta_de_vecinos})


@csrf_exempt
@usuario_presidente_required
def noticias_junta_presidente(request):
    usuario = request.user
    junta_de_vecinos = usuario.junta_de_vecinos
    noticias = NoticiaJuntaVecinos.objects.filter(junta_de_vecinos=junta_de_vecinos).order_by('-fecha_publicacion')
    return render(request, 'noticias_junta_presidente.html', {'noticias': noticias, 'junta_de_vecinos': junta_de_vecinos})


@csrf_exempt
@usuario_presidente_required
def ver_noticia_presidente(request, noticia_id):
    noticia = get_object_or_404(NoticiaJuntaVecinos, pk=noticia_id)
    junta_id = noticia.junta_de_vecinos.id

    # Define PAGE_URL y PAGE_IDENTIFIER
    PAGE_URL = request.build_absolute_uri()  # Esto obtiene la URL actual
    PAGE_IDENTIFIER = f'noticia-{noticia.id}'  # Usa el ID de la noticia como identificador único

    return render(request, 'ver_noticia_presidente.html', {
        'noticia': noticia,
        'junta_id': junta_id,
        'PAGE_URL': PAGE_URL,  # Pasa las variables PAGE_URL y PAGE_IDENTIFIER al contexto
        'PAGE_IDENTIFIER': PAGE_IDENTIFIER,
    })


@csrf_exempt
@usuario_residente_required
def ver_noticia(request, noticia_id):
    noticia = get_object_or_404(NoticiaJuntaVecinos, pk=noticia_id)
    junta_id = noticia.junta_de_vecinos.id

    # Define PAGE_URL y PAGE_IDENTIFIER
    PAGE_URL = request.build_absolute_uri()  # Esto obtiene la URL actual
    PAGE_IDENTIFIER = f'noticia-{noticia.id}'  # Usa el ID de la noticia como identificador único

    return render(request, 'ver_noticia.html', {
        'noticia': noticia,
        'junta_id': junta_id,
        'PAGE_URL': PAGE_URL,  # Pasa las variables PAGE_URL y PAGE_IDENTIFIER al contexto
        'PAGE_IDENTIFIER': PAGE_IDENTIFIER,
    })


@csrf_exempt
@usuario_residente_required
def perfil(request):
    usuario = request.user

    # Maneja el formulario de edición si se ha enviado
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')

    # Crea el formulario de edición y pásalo a la plantilla
    else:
        form = EditProfileForm(instance=usuario)

    return render(request, 'perfil.html', {'usuario': usuario, 'form': form})


@csrf_exempt
@usuario_presidente_required
def perfil_presidente(request):
    usuario = request.user

    # Maneja el formulario de edición si se ha enviado
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil_presidente')

    # Crea el formulario de edición y pásalo a la plantilla
    else:
        form = EditProfileForm(instance=usuario)

    return render(request, 'perfil_presidente.html', {'usuario': usuario, 'form': form})

@csrf_exempt
@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion') 



@csrf_exempt
@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        request.user.delete()  # Elimina el usuario actual
        logout(request)  # Cierra la sesión después de eliminar la cuenta
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})



@csrf_exempt
@usuario_presidente_required
def usuarios_junta(request):
    # Obtén al usuario actualmente autenticado (presidente)
    presidente = request.user

    # Obtén todos los usuarios que pertenecen a la misma junta de vecinos que el presidente
    usuarios_junta = UsuarioPersonalizado.objects.filter(junta_de_vecinos=presidente.junta_de_vecinos)

    # Pasa los usuarios a la plantilla
    return render(request, 'usuarios_junta.html', {'usuarios_junta': usuarios_junta})



@csrf_exempt
@usuario_presidente_required
def editar_usuario_presidente(request, usuario_id):
    usuario = UsuarioPersonalizado.objects.get(id=usuario_id)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuarios_junta')

    else:
        form = EditProfileForm(instance=usuario)

    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})
@csrf_exempt



@csrf_exempt
@usuario_presidente_required
def eliminar_cuenta_presidente(request, usuario_id):
    try:
        usuario = UsuarioPersonalizado.objects.get(id=usuario_id)
        usuario.delete()
        return redirect('usuarios_junta')
    except UsuarioPersonalizado.DoesNotExist:
        return JsonResponse({'success': False})


# Para que se envie correo al subir una nueva noticia
def enviar_correo_a_usuarios_junta(noticia, presidente):
    # Obtener la lista de correos electrónicos de los usuarios de la junta
    correos = UsuarioPersonalizado.objects.filter(junta_de_vecinos=noticia.junta_de_vecinos.id).exclude(id=presidente.id).values_list('email', flat=True)
    print("Lista de correos electrónicos:", correos)

    # Enviar un correo a cada usuario de la junta
    for correo in correos:
        send_mail(
            'Nueva noticia en la junta de vecinos',
            f'Se ha publicado una nueva noticia en la junta de vecinos por {presidente.username}: {noticia.titulo}',
            presidente.email,  # Remitente (correo del presidente)
            [correo],  # Destinatario (correo del usuario)
            fail_silently=False,
        )

@csrf_exempt
@usuario_presidente_required
def agregar_noticia(request):
    noticia = NoticiaJuntaVecinos.objects.filter(junta_de_vecinos=request.user.junta_de_vecinos)

    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar la noticia en la base de datos
            noticia = form.save(commit=False)
            noticia.junta_de_vecinos = request.user.junta_de_vecinos
            noticia.save()

            # Llamar a la función para enviar correos
            enviar_correo_a_usuarios_junta(noticia, request.user)

            return redirect('noticias_junta_presidente')  # Redirigir a la lista de noticias
    else:
        form = NoticiaForm()
    
    return render(request, 'agregar_noticia.html', {'form': form, 'noticias': noticia})


@csrf_exempt
@usuario_presidente_required
def eliminar_noticia(request, noticia_id):
    try:
        noticia = NoticiaJuntaVecinos.objects.get(id=noticia_id)
        
        # Verifica si la noticia pertenece al usuario actual (presidente)
        if noticia.junta_de_vecinos == request.user.junta_de_vecinos:
            noticia.delete()
            return redirect(reverse('agregar_noticia'))
        else:
            return JsonResponse({'error': 'No tienes permiso para eliminar esta noticia.'})
        
    except NoticiaJuntaVecinos.DoesNotExist:
        return JsonResponse({'error': 'La noticia no existe.'})
    
    
@csrf_exempt
@usuario_residente_required
def enviar_mensaje(request):
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.emisor = request.user

            # Obtén a los destinatarios (presidentes) que comparten el mismo `junta_de_vecinos_id`
            # y tienen un valor no vacío ni nulo en `id_sede`
            destinatarios = UsuarioPersonalizado.objects.filter(
                junta_de_vecinos=request.user.junta_de_vecinos,
                id_sede__isnull=False,
                id_sede__gt=""
            )

            if destinatarios:
                # Envía el mensaje a todos los destinatarios
                for destinatario in destinatarios:
                    mensaje.receptor = destinatario
                    mensaje.save()

                    # Envía un correo al destinatario (presidente)
                    send_mail(
                        'Nuevo mensaje de un residente',
                        'Residente: {}\nContenido: {}\nSolicitud de Espacios: {}\nFecha y hora solicitada: {}'.format(
                            mensaje.emisor,
                            mensaje.contenido,
                            mensaje.solicitud_espacios,
                            mensaje.solicitud_fecha_hora.strftime('%D %B %Y %H:%M') if mensaje.solicitud_fecha_hora else 'No especificada'
                        ),
                        request.user.email,  # Remitente (correo del emisor)
                        [destinatario.email],  # Destinatario (correo del presidente)
                        fail_silently=False,
                    )
                messages.success(request, 'El mensaje se ha enviado correctamente a los presidentes.')
            else:
                messages.warning(request, 'No se encontraron presidentes con `id_sede` no vacío ni nulo para enviar el mensaje.')

            return redirect('enviar_mensaje')

    else:
        form = MensajeForm()
    # Obtén el correo del remitente original (tu propio correo)
    remitente_original = request.user.email
    return render(request, 'enviar_mensaje.html', {'form': form, 'remitente_original': remitente_original})


@csrf_exempt
@usuario_presidente_required
def mensajes_recibidos_presidente(request):
    
    if request.method == 'POST':
        form = MensajeModalForm(request.POST)
        if form.is_valid():
            mensaje_respuesta = form.cleaned_data['contenido_presidente']
            asunto = form.cleaned_data['asunto']
            remitente = request.user.email
            destinatario = request.POST.get('remitente')  # Obtén el correo del remitente original
            # Construye el cuerpo del correo que incluye el asunto, el contenido y el mensaje respondido
            cuerpo_correo = f"Asunto: {asunto}\n\nContenido: {mensaje_respuesta}\n\nMensaje Respondido: {mensaje_respuesta}"

            # Enviar el correo de respuesta al remitente original
            send_mail(
                asunto,
                cuerpo_correo,
                remitente,
                [destinatario],  # Utiliza el correo del remitente original como destinatario
                fail_silently=False,
            )

            # Devuelve una respuesta JSON exitosa
            return JsonResponse({'success': True})
        else:
            # Devuelve una respuesta JSON de error si el formulario no es válido
            return JsonResponse({'success': False, 'error': 'Formulario inválido'})
    else:
        # Renderiza la página con el formulario modal
        form = MensajeModalForm()
        mensajes_recibidos = Mensaje.objects.filter(receptor=request.user)
        

        return render(request, 'mensajes_recibidos_presidente.html', {'mensajes_recibidos': mensajes_recibidos, 'form': form})


@csrf_exempt
@usuario_residente_required
def postular_proyecto(request):
    if request.method == 'POST':
        form = PostulacionProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.residente = request.user
            destinatarios = UsuarioPersonalizado.objects.filter(
                junta_de_vecinos=request.user.junta_de_vecinos,
                id_sede__isnull=False,
                id_sede__gt=""
            )
            if destinatarios:
                # Envía el mensaje a todos los destinatarios
                for destinatario in destinatarios:
                    proyecto.presidente = destinatario
                    proyecto.save()

            messages.success(request, 'Proyecto postulado correctamente')

            return redirect('postular_proyecto')  # Redirigir a la lista de proyectos pendientes

    else:
        form = PostulacionProyectoForm()
    
    proyectos_postulados = Proyecto.objects.filter(residente=request.user).order_by('-fecha_postulacion')


    return render(request, 'postular_proyecto.html', {'form': form, 'proyectos_postulados': proyectos_postulados})


@csrf_exempt
@usuario_presidente_required
def proyectos_pendientes(request):
    proyectos_pendientes = Proyecto.objects.filter(estado='P', presidente=request.user).order_by('-fecha_postulacion')

    if request.method == 'POST':
        form = AprobacionProyectoForm(request.POST)
        if form.is_valid():
            proyecto_id = form.cleaned_data['proyecto_id']
            estado = form.cleaned_data['estado']

            proyecto = Proyecto.objects.get(pk=proyecto_id)
            if estado == 'A':
                proyecto.estado = 'A'  # Aprobar
                proyecto.fecha_aprobacion = timezone.now()
            elif estado == 'R':
                proyecto.estado = 'R'  # Rechazar
                proyecto.fecha_rechazo = timezone.now()
            proyecto.save()

            return redirect('proyectos_pendientes')

    else:
        form = AprobacionProyectoForm()

    return render(request, 'proyectos_pendientes.html', {'proyectos_pendientes': proyectos_pendientes, 'form': form})
