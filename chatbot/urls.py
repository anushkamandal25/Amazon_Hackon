from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('register/', views.registerPage, name = "register"),
    path('home/', views.home, name="home"),
]