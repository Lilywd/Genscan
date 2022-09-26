from django.contrib import admin
from django.urls import path,include
from genscan import views 

urlpatterns = [
    
    path('dashboard', views.dashboard, name="dashboard"),
    path('generator',views.generator, name='generator'),
    path('scanner',views.scanner, name='scanner'),
]