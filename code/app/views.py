from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import *

# from forms import UserRegisterForm

# Create your views here.


def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products':products})


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

def view_favorites(request) :
    favorites = Favorite.objects.filter(uid=100)
    return render(request, 'favorites.html',{'favorites':favorites})

'''
def del_favorites(request) :
    #html에서 삭제하고자 하는 del_fid 전달받아와서 연결해놓으면 해결
    del_f = Favorite.objects.get(fid = del_fid)
    del_f.delete()

    #삭제한 뒤에 위의 view_favorites 메서드를 재수행 하면 업데이트된 My favorites로 바로 이동할 수 있을 것 같음
    return render(request, favorites)
'''


