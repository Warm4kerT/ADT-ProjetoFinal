"""ADT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from pages import views

urlpatterns = [
    path('',views.router_db),
    path('router_form/',views.add_router),
    path('router_db/',views.router_db),
    path('script_form/',views.add_script),
    path('script_db/',views.script_db),
    path('logs/',views.deployment_db),
    path('delete_router/<int:router_id>', views.delete_router, name='delete_router'),
    path('delete_script/<int:script_id>', views.delete_script, name='delete_script'),
    path('view/<int:dp_id>', views.show_file, name='show'),    
]
