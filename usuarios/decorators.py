from django.core.exceptions import PermissionDenied

def vendedor_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'vendedor':
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view_func

def bodeguero_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'bodeguero':
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view_func

def contador_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'contador':
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view_func