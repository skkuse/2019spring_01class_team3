from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm
from .models import *
import requests as req
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db.models.query import QuerySet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect

# 기본 함수

def getExRate():
    # day format : yyyymmdd
    day = str(datetime.today().year) + \
        '%02d' % datetime.today().month + str(datetime.today().day)

    url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=EgAaHKyguuwATPc8pOp29tLMJNOSYRw8&searchdate=%s&data=AP01' % day

    ex_rate_response = req.get(url)
    ex_rate_json = ex_rate_response.json()

    if str(ex_rate_response) != '<Response [200]>' or len(ex_rate_json) == 0: # 주말엔 없어서 그냥 -2일로 환율 확인.
        day = str(datetime.today().year) + \
            '%02d' % datetime.today().month + str(datetime.today().day - 2)

        url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=EgAaHKyguuwATPc8pOp29tLMJNOSYRw8&searchdate=%s&data=AP01' % day

    ex_rate_response = req.get(url)
    ex_rate_json = ex_rate_response.json()

    ex_rate = {}

    # DEAL_BAS_R
    for ex in ex_rate_json:
        if ex['cur_unit'] == 'USD':
            ex_rate['미국'] = float(ex['deal_bas_r'].replace(',', ''))
        elif ex['cur_unit'] == 'EUR':
            ex_rate['프랑스'] = float(ex['deal_bas_r'].replace(',', ''))
        elif ex['cur_unit'] == 'JPY(100)':
            ex_rate['일본'] = float(ex['deal_bas_r'].replace(',', '')) / 100

    return ex_rate


# HOME
def home(request):
    products = Product.objects.filter(cid=1).order_by('-phit')[:20]

    return render(request, 'index.html', {'products': products})


def home_filter(request, f, name):
    products=[]

    if f == "category":
        products = Product.objects.filter(category=name).filter(cid=1).order_by('-phit')[:20]
    elif f == "brand":
        products = Product.objects.filter(brand__icontains=name).filter(cid=1).order_by('-phit')[:20]

    return render(request, 'index.html', {'products':products})



# User Management System
@csrf_protect
def login_request(request):
    if request.method == "POST":
        input_email = request.POST.getlist('email')
        input_password = request.POST.getlist('password')
        print(input_email)
        print(input_password)
        user = authenticate(email=input_email, password=input_password)
        # user.is_active = True

        if user is not None:
            print("not none")
            login(request, user)
            return redirect('home')
        else:
            print("none")
            return render(request, 'login.html', {'error': 'email or password is incorrect'})
    else:
        return render(request, 'login.html')


def logout_request(request):
    logout(request)
    return render(request, 'logout.html')
    # if request.method == 'POST':
    #     return redirect('home')
    # return render(request, 'logout.html')


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


# Favorites System
def view_favorites(request):

    favorites = Favorite.objects.filter(uid=request.user)

    # API 추가
    ex_rate = getExRate()

    for f in favorites:
        if int(str(f.pid.cid)) != 1:
            f.pid.price = "{:,}".format(int(ex_rate[str(f.pid.cid.cname)] * int(f.pid.price)))


    return render(request, 'favorites.html', {'favorites': favorites})


def delFavorite(request, del_fid):
    if request.method == 'GET':
        del_favorite = Favorite.objects.get(fid=del_fid)
        del_favorite.delete()
        return view_favorites(request)


def addFavorite(request, add_id):
    print("-------------------------"+add_id)
    if request.method == 'GET':
        user = request.user
        product = Product.objects.get(id=add_id)
        ko_id = Product.objects.filter(pcode=product.pcode) #.filter(cid=0)

        ######kprice add 기능 구현 ######
        ###아직 kprice 0으로 뜸! ###

        kprice = '0'
        for k in ko_id:
            if k.cid == 1: kprice = "{:,}".format(k.price)

        favorite = Favorite(pid=product, uid=user, kprice=kprice)
        favorite.save()
        return detail(request, product.pcode)


# Comparing System

#HIT 수 올리기 반영
def detail(request, pcode):
    if request.method == 'GET':
        products = Product.objects.filter(pcode=pcode)
        # print(products)
        # print(pcode)

        p = products[0]

        ex_rate = getExRate()

        for product in products:
            if int(str(product.cid)) == 1:
                # print(product.phit)
                product.phit += 1
                product.save()
                # print(product.phit)
            else:
                product.price = int(int(product.price) *
                                    ex_rate[str(product.cid.cname)])
            product.price = "{:,}".format(product.price)

        return render(request, 'product_detail.html', {'products': products, 'p': p})


# SEARCH system
def searchList(request):
    try: query = request.GET.get('q')
    except: query = None

    dissearch_list = []

    if query is not None and len(query) != 0:
        search_list = Product.objects.filter(pname__icontains=query).filter(cid=1)
        if len(search_list) == 0:
            print("pcode 검색!")
            search_list = Product.objects.filter(pcode__icontains=query).filter(cid=1)

        pcode_dict = {}
        for p in search_list:
            if p.pcode not in pcode_dict:

                pcode_dict[p.pcode] = p.pname
                p.price = "{:,}".format(p.price)
                dissearch_list.append(p)

    elif len(query) == 0: # 빈 쿼리 날렸을 때. 뒤에 슬라이싱은 원하는대로 설정하면 될 듯.
        dissearch_list = Product.objects.filter(cid=1).order_by('-phit')[:50]


    # 첫 element 찾기
    if len(dissearch_list) != 0:
        elem = dissearch_list[0]
    else: elem = None

    print(search_list)
    paginator = Paginator(dissearch_list, 15)
    page = request.GET.get('page', 1)
    try:
        search = paginator.page(page)
    except PageNotAnInteger:
        search = paginator.page(1)
    except EmptyPage:
        search = paginator.page(paginator.num_pages)

    return render(request, 'searchList.html', {'products': dissearch_list, 'q': elem, 'search': search, 'query':query})
