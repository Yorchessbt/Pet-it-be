from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm
from django.contrib.auth import logout
from Pets.views import home
from django.contrib.auth.decorators import login_required
from .models import Perfil
from django.contrib.auth.models import User
from .forms import ProfileForm

# Create your views here.

def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    perfil = get_object_or_404(Perfil, user=user_obj)

    context = {
        'perfil': perfil,
        'perfil_user': user_obj,  
    }
    return render(request, 'perfil/perfil.html', context)

@login_required
def edit_profile(request):
    edit_p = request.user.perfil

    if request.method == 'POST':
        perfilform = ProfileForm(request.POST, request.FILES, instance=edit_p)

        if perfilform.is_valid():
            perfilform.save()
            return redirect('profile', username=request.user.username)
    else:
        perfilform = ProfileForm(instance=edit_p)
    
    context = {
        'perfilform': perfilform,
        'edit_p': edit_p

    }

    return render(request, 'perfil/perfil.html', context)


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    context = {
        'form': form
    }
    return render(request, 'perfil/signup.html', context)    

def login_view(request):
    return render(request, 'perfil/login.html')

def logout_user(request):
    logout(request)

    return redirect(home)