from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import purchase_product

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('register/', views.registerPage, name = "register"),
    path('home/', views.home, name="home"),
    path('chat/', views.chat, name="chat"),
    path('profile/', views.profile, name='profile'),
    path('logout', views.logoutPage, name="logout"),
    # path('recommendation/', views.product_recommendation_view, name='product_recommendation'),
    path('purchase/<product_id>/', purchase_product, name='purchase_product'),
]