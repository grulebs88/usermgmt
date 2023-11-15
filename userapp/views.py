from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, ImageUploadForm
from .models import LoginHistory, UploadedImage
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages

# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                ip = request.META.get('REMOTE_ADDR')
                LoginHistory.objects.create(user=user, ip_address=ip)
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    login_history = LoginHistory.objects.filter(user=request.user).order_by('-login_time').first()
    if login_history:
        login_history.logout_time = timezone.now()
        login_history.save()

    logout(request)
    return redirect('login')

def index_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = UploadedImage(image=form.cleaned_data['image'], user=request.user)
            image.save()
            return render(request, 'index.html', {'form': form, 'image': image})
    else:
        form = ImageUploadForm()
    return render(request, 'index.html', {'form': form})