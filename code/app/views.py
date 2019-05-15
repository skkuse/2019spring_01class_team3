from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

# from forms import UserRegisterForm

# Create your views here.


def home(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for %s'%username)
            return redirect('home')

    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
