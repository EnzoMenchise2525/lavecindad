from django.http import HttpResponseForbidden
from functools import wraps

def usuario_presidente_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (hasattr(request.user, 'id_sede') and request.user.id_sede is not None and request.user.id_sede != ""):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página como residente.")
    return _wrapped_view

def usuario_residente_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verifica si el usuario está autenticado y si el campo id_sede está vacío
        if request.user.is_authenticated and (not hasattr(request.user, 'id_sede') or request.user.id_sede == ""):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    return _wrapped_view
