from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def logout_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('layout')  # Redirect to home or any other page
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func