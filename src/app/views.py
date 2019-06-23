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
from django.http import HttpResponse
import json, random, os


# 기본 함수

def getExRate():
    # day format : yyyymmdd
    day = str(datetime.today().year) + \
        '%02d' % datetime.today().month + str(datetime.today().day)

    url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=EgAaHKyguuwATPc8pOp29tLMJNOSYRw8&searchdate=%s&data=AP01' % day


    ex_rate_response = req.get(url)

    ex_rate_json = ex_rate_response.json()

    before = 1
    while len(ex_rate_json) == 0 and ex_rate_response != '<Response [200]>':

        day = str(datetime.today().year) + \
            '%02d' % datetime.today().month + str(datetime.today().day - before)
        before += 1

        url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=EgAaHKyguuwATPc8pOp29tLMJNOSYRw8&searchdate=%s&data=AP01' % day

        ex_rate_response = req.get(url)
        ex_rate_json = ex_rate_response.json()


    ex_rate = {}

    #DEAL_BAS_R
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
    search = Product.objects.filter(cid=1).order_by('-phit')[:20]
    
    return render(request, 'index.html', {'search':search, 'num_pages':1})


def home_filter(request, f, name):
    products=[]

    if f == "category":
        products = Product.objects.filter(category=name).filter(cid=1).order_by('-phit')
    elif f == "brand":
        products = Product.objects.filter(brand__icontains=name).filter(cid=1).order_by('-phit')

    
    #### PAGINATOR ####
    paginator = Paginator(products, 15)
    page = request.GET.get('page')

    try:
        search = paginator.page(page)

    except PageNotAnInteger:
        search = paginator.page(1)

    except EmptyPage:
        search = paginator.page(paginator.num_pages)


    # paginator 범위 5개로 제한
    page_numbers_range = 5 # 보여줄 페이지 range: 5개
    max_idx = len(paginator.page_range) # 페이지 개수

    current_page = int(page) if page else 1
    start_idx = int((current_page - 1)/page_numbers_range) * page_numbers_range
    end_idx = start_idx + page_numbers_range

    if end_idx >= max_idx: end_idx = max_idx
    
    page_range = paginator.page_range[start_idx:end_idx]

    return render(request, 'index.html', {'search':search, 'num_pages':paginator.num_pages})



# User Management System
@csrf_protect
def login_request(request):
    if request.method == "POST":
        input_email = request.POST.getlist('email')
        input_password = request.POST.getlist('password')
        user = authenticate(email=input_email, password=input_password)
        # user.is_active = True

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
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
    pcode_list = {}
    for f in favorites :
        pcode = f.pid.pcode
        if pcode in pcode_list :
            continue
        else :
            pcode_list[pcode] = Product.objects.filter(pcode=pcode)[0]


    # API 추가
    ex_rate = getExRate()

    for f in favorites:
        if int(str(f.pid.cid)) != 1:
            f.pid.price = int(ex_rate[str(f.pid.cid.cname)] * int(f.pid.price))


    return render(request, 'favorites.html', {'favorites': favorites, 'pcode_list' :pcode_list})

def product_like(request) :
    pid = request.POST.get('add_pid', None)
    user = request.user

    product = Product.objects.get(id = pid)

    value = dup_check_favorite(request, pid)

    if( value ) : ##중복 pid 인 favorite가 존재하는 경우
        value.delete()
        message = "좋아요 취소"

    else :
        favorite = Favorite(pid=product, uid=user)
        favorite.save()
        message = "좋아요"

    context = {'message': message}

    return HttpResponse(json.dumps(context), content_type="application/json")


def dup_check_favorite(request, product_id) :
    ##pid를 넣고 user의 favorite에서 중복되는 항목을 찾아보고
    #중복의 경우 favorite객체를 리턴
    #중복x인 경우 False값을 리턴

    user = request.user
    favorites = Favorite.objects.filter(uid=request.user)
    value = False
    for f in favorites :
        if ( str(product_id) == str(f.pid.id) ) :
            value = f
    return value

def delFavorite(request, del_fid):
    if request.method == 'GET':
        if( del_fid == 'all') :
            del_favorites = Favorite.objects.filter(uid = request.user)
            for f in del_favorites :
                f.delete()
        else :
            del_favorite = Favorite.objects.get(fid=del_fid)
            del_favorite.delete()
        return view_favorites(request)


# Comparing System

#HIT 수 올리기 반영
#Search DB

## @saanmin editted
## 로그인된 유저의 경우, 원래 pcode에 대하여 관심상품으로 가지고 있는 list를 같이 전달해주어 
## 기존에 관심상품으로 등록되어 있는 것은
## 꽉찬 하트로 나타나도록 만들려고 리스트 넘기기 위해 수정했습니다!

def detail(request, pcode):
    # pcode = pcode[]
    if request.method == 'GET':
<<<<<<< HEAD
        products = Product.objects.filter(pcoworkde=pcode)
        # print(products)
        # print(pcode)

        p = products[0]

=======
        products = Product.objects.filter(pcode=pcode)
        p = products.filter(cid=1)[0]
>>>>>>> 2e9e29d7fd0f0f937a5c02ee429779e96b310cce
        ex_rate = getExRate()
        user_fav_list = []

        for product in products:
            if request.user.is_authenticated:
                user = request.user
                user_fav_list = list(Favorite.objects.filter(uid = user).values_list('pid', flat=True))
                searchlog = Searchlog(uid=user,pcode=product)
                searchlog.save()

            if int(str(product.cid)) == 1:
                # print(product.phit)
                product.phit += 1
                product.save()

            else:
                product.price = int(int(product.price) *ex_rate[str(product.cid.cname)])

        
        recom_products = list(Recommend.objects.filter(pcode=pcode)[:10])
        random.shuffle(recom_products)

        im_list = os.listdir("/var/www/src/media/img/products")

        recom_result = []
        
        for rp in recom_products:
            rp_im = str(rp.r_pcode)+".png"
            if rp_im in im_list: 
                recom_result.append(rp)
                if len(recom_result) == 4: break

        
        return render(request, 'product_detail.html', {'products': products, 'p': p, 
        'user_fav_list':user_fav_list, 'recom_products':recom_result})



# SEARCH system
def searchList(request):
    try: query = request.GET.get('q')
    except: query = None

    dissearch_list = []

    if query is not None and len(query) != 0: # 빈 쿼리가 아닐 때
        search_list = Product.objects.filter(pname__icontains=query).filter(cid=1)
        if len(search_list) == 0:
            search_list = Product.objects.filter(pcode__icontains=query).filter(cid=1)

        pcode_dict = {}
        for p in search_list:
            if p.pcode not in pcode_dict:

                pcode_dict[p.pcode] = p.pname
                p.price = "{:,}".format(p.price)
                dissearch_list.append(p)

    elif len(query) == 0: # 빈 쿼리 날렸을 때.
        dissearch_list = Product.objects.filter(cid=1).order_by('-phit')[:100]


    # 첫 element 찾기
    if len(dissearch_list) != 0:
        elem = dissearch_list[0]
    else: elem = None


    #### PAGINATOR ####
    paginator = Paginator(dissearch_list, 15)
    page = request.GET.get('page')

    try:
        search = paginator.page(page)

    except PageNotAnInteger:
        search = paginator.page(1)

    except EmptyPage:
        search = paginator.page(paginator.num_pages)


    # paginator 범위 5개로 제한
    page_numbers_range = 5 # 보여줄 페이지 range: 5개
    max_idx = len(paginator.page_range) # 페이지 개수

    current_page = int(page) if page else 1
    start_idx = int((current_page - 1)/page_numbers_range) * page_numbers_range
    end_idx = start_idx + page_numbers_range

    if end_idx >= max_idx: end_idx = max_idx

    page_range = paginator.page_range[start_idx:end_idx]


    return render(request, 'searchList.html',
    {'q': elem, 'search': search, 'query':query,
    'page_range':page_range, 'num_pages':paginator.num_pages})
