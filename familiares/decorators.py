from functools import wraps
from django.shortcuts import redirect
from .models import Familiar


def familiar_requerido(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        rut = request.session.get("familiar_rut")
        if not rut:
            return redirect("familiares:iniciar_sesion")
        try:
            request.familiar = Familiar.objects.get(rut=rut)
        except Familiar.DoesNotExist:
            request.session.flush()
            return redirect("familiares:iniciar_sesion")
        return view(request, *args, **kwargs)
    return wrapper