from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, 'home.html')

def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request, 'login.html')

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}
    return render(request, 'register.html', context)
