from django.contrib import admin
from django.urls import path,include
from . import views 



urlpatterns = [
    path('', views.landing, name="landing"),
    path('signin', views.signin, name="signin"),
    path('register', views.register, name="register"),
    path('signout', views.signout, name="signout"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('contact', views.contact, name="contact"),
    path('profile', views.profile, name="profile"),
    path("password_change", views.password_change, name="password_change"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    # path('change_email', views.change_email, name="change_email"),
]