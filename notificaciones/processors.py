from .models import Notificacion

def ctx_dict(request):
    noti =  Notificacion.objects.filter(usuario=request.user)
    
    return {'notificaciones':noti}

def new_noti(request):
    new_noti = Notificacion.objects.filter(usuario=request.user).exclude(
                                        estado=1)

    return {'new_noti':new_noti}