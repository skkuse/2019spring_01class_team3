from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import *
import requests as req
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db.models.query import QuerySet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.query import QuerySet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect

# 기본 함수


def home(request):
    ko_products = Product.objects.filter(cid=1)

    products = []

    count = 0
    for p in ko_products:
        if count == 20:
            break
        count += 1
        products.append(p)

    return render(request, 'index.html', {'products': products})


def getExRate():
    # day format : yyyymmdd
    day = str(datetime.today().year) + \
        '%02d' % datetime.today().month + str(datetime.today().day)

    url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=EgAaHKyguuwATPc8pOp29tLMJNOSYRw8&searchdate=%s&data=AP01' % day

    ex_rate_response = req.get(url)
    ex_rate_json = ex_rate_response.json()

    if str(ex_rate_response) != '<Response [200]>' or len(ex_rate_json) == 0:
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
    # user login 실패시..
    # favorites = Favorite.objects.filter(uid = 100)

        # user 성공하면...
    favorites = Favorite.objects.filter(uid=request.user)

    # API 추가
    ex_rate = getExRate()
    for f in favorites:
        if int(f.id.cid) != 1:
            f.id.price = "{:,}".format(int(ex_rate[str(f.id.cid.cname)] * int(f.id.price)))
        

    return render(request, 'favorites.html', {'favorites': favorites})


def delFavorite(request, del_fid):
    if request.method == 'GET':
        del_favorite = Favorite.objects.get(fid=del_fid)
        del_favorite.delete()
        return view_favorites(request)


def addFavorite(request, add_id):
    if request.method == 'GET':
        '''
        product = Product.objects.get(id = add_id)
        favorite = Favorite(id=product, uid=100)
        favorite.save()
        return view_favorites(request)
        '''

        # User 연동 성공하면...

        user = request.user
        product = Product.objects.get(id=add_id)
        ko_id = Product.objects.filter(pcode=product.pcode) #.filter(cid=0)
        kprice = '0'
        for k in ko_id:
            if k.cid == 1: kprice = "{:,}".format(k.price)
    
        favorite = Favorite(id=product, uid=user, kprice=kprice)
        favorite.save()
        return detail(request, product.pcode)

        # 원하는 페이지로 설정...보통 즐겨찾기는 세부페이지에서 진행하므로

# Comparing System


def detail(request, pcode):
    if request.method == 'GET':
        products = Product.objects.filter(pcode=pcode)

        p = products[0]

        ex_rate = getExRate()

        for product in products:
            if int(str(product.cid)) != 1:
                product.price = int(int(product.price) *
                                    ex_rate[str(product.cid.cname)])
            product.price = "{:,}".format(product.price)

        return render(request, 'product_detail.html', {'products': products, 'p': p})


def searchList(request):
    try:
        query = request.GET.get('q')
    except:
        query = None
    queryset_list = Product.objects.all()
    if query:
        queryset_list = Product.objects.filter(
            pname__icontains=query
        ).distinct()

    # queryset_list = queryset_list.values('pname').distinct()   --> 이걸 치면 가격정보와 이미지가 안나오네요.....
    qu = queryset_list[0]

    paginator = Paginator(queryset_list, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    return render(request, 'searchList.html', {'products': queryset_list, 'q': qu})
