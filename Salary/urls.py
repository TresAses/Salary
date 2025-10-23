"""Salary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from Aplicaciones.Salary import views
from Aplicaciones.Salary.views import admin_redirect
from django.contrib.auth.views import logout_then_login

urlpatterns = [
    path('administracion-django/ex-salary/', admin.site.urls),

    path('admin-redirect/', admin_redirect, name='administrador'),

    path('', include('Aplicaciones.Salary.urls')),

    # path('login/', include('Aplicaciones.Salary.urls')),

    path('accounts/login/', views.LogIn, name="inicio_sesion"),

    path('accounts/login/salary/', views.custom_login, name='login-salary'),

    path('logout/', logout_then_login, name='logout'),

    path('accounts/login/logout/', logout_then_login, name='log_out'),
]
    # location ~ /\.git {
    #     deny all;
    # }
    
    # location ~ \.yml$ {
    #     deny all;
    # }