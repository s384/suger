from .models import Notificacion

def ctx_dict(request):
    if request.user.is_authenticated:
        noti =  Notificacion.objects.filter(usuario=request.user)[:5]
    
        return {'notificaciones':noti}
    return {}

def new_noti(request):
    if request.user.is_authenticated:
        new_noti = Notificacion.objects.filter(usuario=request.user).exclude(
                                            estado=1)

        return {'new_noti':new_noti}
    return {}