from app import views
from django.urls import path, re_path
from django.contrib import admin



urlpatterns = [
    re_path('^admin/', admin.site.urls),
    re_path('^login/$', views.login, name="login"),
    re_path('^logout/$', views.logout, name="logout"),
    re_path('^detail/(?P<pcode>.*)$', views.detail, name="detail"),
    re_path('^searchList/$', views.searchList, name="searchList"),
    # $ : 뒤에 더이상 다른 슬래시가 오지 않도록 막아버리는 기
    re_path('^favorites/(?P<del_fid>.*)$', views.delFavorite, name="delFavorite"),

]
