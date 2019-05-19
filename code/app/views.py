from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import *
import requests as req
from datetime import datetime




from django.db.models.query import QuerySet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from forms import UserRegisterForm

# Create your views here.


def home(request):
    distinct_products = Product.objects.values('pcode').distinct()
    products = []

    for p in distinct_products:
        products.append(Product.objects.filter(pcode=p['pcode'])[0])

    return render(request, 'index.html', {'products': products})


def login(request):
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for %s' % username)
            return redirect('home')

    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def detail(request, pcode):
    if request.method == 'GET':
        products = Product.objects.filter(pcode=pcode)

        day = str(datetime.today().year) + '%02d'%datetime.today().month + str(datetime.today().day)


        url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=EgAaHKyguuwATPc8pOp29tLMJNOSYRw8&searchdate=%s&data=AP01'%day

        ex_rate_res = req.get(url).json()
        ex_rate = {}
        # DEAL_BAS_R
        for ex in ex_rate_res:
            if ex['cur_unit'] == 'USD':
                ex_rate['미국'] = float(ex['deal_bas_r'].replace(',',''))
            elif ex['cur_unit'] == 'EUR':
                ex_rate['프랑스'] = float(ex['deal_bas_r'].replace(',',''))
            elif ex['cur_unit'] == 'JPY(100)':
                ex_rate['일본'] = float(ex['deal_bas_r'].replace(',','')) / 100





        p = products[0]

        for product in products:
            if str(product.cid) != '대한민국':
                product.price = int(int(product.price) * ex_rate[str(product.cid)])
            product.price = "{:,}".format(product.price)

        return render(request, 'product_detail.html', {'products': products, 'p': p})


def searchList(request):
    try: query = request.GET.get('q')
    except: query = None
    queryset_list = Product.objects.all()
    if query:
        queryset_list = Product.objects.filter(
            pname__icontains=query
            ).distinct()

    qu = queryset_list[0]
    paginator = Paginator(queryset_list, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EnptyPage:
        queryset = paginator.page(paginator.num_pages)
    return render(request, 'searchList.html', {'products': queryset_list, 'q': qu})
