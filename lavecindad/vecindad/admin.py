from django.contrib import admin
from .models import UsuarioPersonalizado, JuntaDeVecinos, NoticiaJuntaVecinos, Mensaje
# Register your models here.
admin.site.register(UsuarioPersonalizado)
admin.site.register(JuntaDeVecinos)
admin.site.register(NoticiaJuntaVecinos)
admin.site.register(Mensaje)



