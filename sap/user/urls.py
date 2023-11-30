"""
URL configuration for sap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
#from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register', views.register,name='register'),
    path('login', views.custom_login,name='login'),
    path('logout', views.custom_logout,name='logout'),
    path('profile/<username>', views.profile,name='profile'),
    path('active/<uidb64>/<token>', views.activate,name='activate'),
    path('password_change', views.password_change,name='password_change'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    path('social/signup/', views.signup_redirect, name='signup_redirect'),

    #path('login', auth_views.LoginView.as_view(template_name='user/auth/login.html'),name='login'),
    #path('logout', auth_views.LogoutView.as_view(template_name='user/auth/logout.html'),name='logout'),
]
