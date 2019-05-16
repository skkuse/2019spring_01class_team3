from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import *



# from forms import UserRegisterForm

# Create your views here.


def home(request):
    distinct_products = Product.objects.values('pcode').distinct()
    products = []

    for p in distinct_products:
        products.append(Product.objects.filter(pcode = p['pcode'])[0])


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

def detail(request, pcode):
    if request.method == 'GET':
        products = Product.objects.filter(pcode = pcode)
        print("-----products: ",products)
        
        p = products[0]
        
    
        return render(request, 'product_detail.html', {'products':products, 'p': p})
