"""lavecindad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from vecindad import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', views.sesion, name='iniciar_sesion'),  # Reemplaza 'views' con el módulo que contiene tu vista personalizada
    path('bienvenida/',views.bienvenida, name="bienvenida"), 
    path('registro',views.registro, name="registro"),
    path('registro_presidente',views.registro_presidente, name="registro_presidente"),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil_presidente/', views.perfil_presidente, name='perfil_presidente'),
    path('noticias/junta/', views.noticias_junta, name='noticias_junta'),
    path('noticias_junta_presidente/', views.noticias_junta_presidente, name='noticias_junta_presidente'),
    path('ver_noticia/<int:noticia_id>/', views.ver_noticia, name='ver_noticia'),  # Nueva URL para ver noticias completas
    path('ver_noticia_presidente/<int:noticia_id>/', views.ver_noticia_presidente, name='ver_noticia_presidente'),  # Nueva URL para ver noticias completas
    path('cerrar_sesion/', views.cerrar_sesion, name='logout'),
    path('eliminar_cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('usuarios_junta/', views.usuarios_junta, name='usuarios_junta'),
    path('agregar_noticia/', views.agregar_noticia, name='agregar_noticia'),
    path('editar-usuario/<int:usuario_id>/', views.editar_usuario_presidente, name='editar_usuario'),
    path('eliminar_cuenta_presidente/<int:usuario_id>/', views.eliminar_cuenta_presidente, name='eliminar_cuenta_presidente'),
    path('enviar_mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    path('mensajes_recibidos_presidente/', views.mensajes_recibidos_presidente, name='mensajes_recibidos_presidente'),
    path('descargar_pdf/', views.descargar_pdf, name='descargar_pdf'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
