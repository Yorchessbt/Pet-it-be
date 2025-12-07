from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, logout_user
from .views import *
from .forms import LoginForm

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='perfil/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    path('<str:username>/', profile, name='profile'),
    path('', edit_profile, name='edit_profile')

]