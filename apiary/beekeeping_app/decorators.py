from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

#people that are not logged in basically
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

#people that are logged in
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            print('allowed_roles:', allowed_roles)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                print('user group:', group)
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                print('User not authorized')
                return HttpResponse('You are not authorized to view this page.')
        return wrapper_func
    return decorator
