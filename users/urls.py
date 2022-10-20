from django.urls import path
from users import views 

urlpatterns = [
    path('', views.landing, name="landing"),
    path('how-it-works/', views.manual, name="manual"),
    path('FAQs/', views.faqs, name="faqs"),
    path('register', views.register, name="register"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('profile', views.profile, name="profile"),
    path("contact", views.contact, name="contact"),
    path("password_reset", views.password_reset_request, name="password_reset"),

]

