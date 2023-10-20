# signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import UsuarioPersonalizado

@receiver(pre_save, sender=UsuarioPersonalizado)
def format_rut(sender, instance, **kwargs):
    if instance.rut:
        rut = instance.rut.replace(".", "")  # Elimina puntos si existen
        rut = rut[:-1] + "-" + rut[-1]  # Agrega guión
        rut = f"{rut[:2]}.{rut[2:5]}.{rut[5:-2]}-{rut[-1]}"  # Agrega puntos

        instance.rut = rut
