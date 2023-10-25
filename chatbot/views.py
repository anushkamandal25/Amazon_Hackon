from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.urls import reverse
from .models import *
from django.http import JsonResponse
from .recommend_products import recommend_products  # Import the recommendation function

# Create your views here.
@login_required(login_url="login_user")
def home(request):
    return render(request, 'home.html')

# @login_required(login_url="login_user")
def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "Successfully Logged In")
            return redirect('chat')
        else:
            messages.warning(request, "Incorrect Username or Password")
            return render(request, 'login.html')
    
    return render(request, "login.html")
        

def logoutPage(request):
    logout(request)
    return redirect('login')      

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request, 'register.html', context)

def chat(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')

        if user_message:
            recommended_products = recommend_products(user_message)
        else:
            recommended_products = []

        response_data = {
            'recommended_products': recommended_products.to_dict(orient='records')
        }

        return JsonResponse(response_data)
    return render(request, 'chatbot.html')

def profile(request):
    return render(request, 'profile.html')

# def product_recommendation_view(request):
#     if request.method == 'POST':
#         user_message = request.POST.get('user_message')
#         print("This is message" + user_message)

#         if user_message:
#             recommended_products = recommend_products(user_message)
#         else:
#             recommended_products = []

#         response_data = {
#             'recommended_products': recommended_products.to_dict(orient='records')
#         }

#         return JsonResponse(response_data)
