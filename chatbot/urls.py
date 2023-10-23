from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('register/', views.registerPage, name = "register"),
    path('home/', views.home, name="home"),
    path('chat/', views.chat, name="chat"),
    path('profile/', views.profile, name='profile'),
    path('recommendation/', views.product_recommendation_view, name='product_recommendation'),
]
