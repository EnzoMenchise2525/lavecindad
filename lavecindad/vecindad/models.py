from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from vecindad.validators import validate_rut

class JuntaDeVecinos(models.Model):
    id_sede = models.CharField(max_length=20, unique=True)
    comuna = models.CharField(max_length=100, blank=True, null=True)
    sector_cerro = models.CharField(max_length=100, blank=True, null=True)
    nombre = models.CharField(max_length=255)
    direccion = models.TextField(max_length=255,blank=True, null=True)
    telefono = models.CharField(max_length=20)
    unidad_vecinal = models.CharField(max_length=100)
  

    def __str__(self):
        return self.nombre

class UsuarioPersonalizado(AbstractUser):

    rut = models.CharField(
        max_length=20,  # El RUT chileno tiene un máximo de 12 caracteres (incluyendo guiones)
        unique=True,  # RUT debe ser único
        validators=[validate_rut],  # Aplicar validación personalizada
        null=True,
    )
    fecha_nacimiento = models.DateField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')], blank=True, null=True)
    nombre_junta = models.CharField(max_length=255, blank=True, null=True)
    junta_de_vecinos = models.ForeignKey(JuntaDeVecinos, on_delete=models.SET_NULL, blank=True, null=True)
    id_sede = models.CharField(max_length=20, blank=True, null=True)
  

    def __str__(self):
        return self.username



class NoticiaJuntaVecinos(models.Model):
    imagen = models.ImageField(upload_to='noticias/', blank=True, null=True)  # Campo de imagen
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    junta_de_vecinos = models.ForeignKey('JuntaDeVecinos', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
    

class Mensaje(models.Model):
    ELECCIONES_SOLICITUD = (
        ('cancha', 'Cancha'),
        ('sala', 'Sala'),
        ('plaza', 'Plaza'),
        ('otro', 'Otro'),
    )
    #Mensaje Modal
    asunto = models.TextField(null=True, blank=True)
    contenido_presidente = models.TextField(null=True, blank=True)

    emisor = models.ForeignKey('UsuarioPersonalizado', related_name='mensajes_enviados', on_delete=models.CASCADE)
    receptor = models.ForeignKey('UsuarioPersonalizado', related_name='mensajes_recibidos', on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(default=timezone.now)
    solicitud_espacios = models.CharField(
        max_length=10,
        choices=ELECCIONES_SOLICITUD,
        blank=True,
        verbose_name='Tipo de Espacio Solicitado'
    )
    solicitud_fecha_hora = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.emisor} -> {self.receptor}'

