from app import views
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    re_path('^admin/', admin.site.urls),
    re_path('^login/$', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    re_path('^logout/$',
            auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
    re_path('^detail/(?P<pcode>.*)$', views.detail, name="detail"),
    re_path('^searchList/', views.searchList, name="searchList"),

    re_path('^delFavorite/(?P<del_fid>.*)$', views.delFavorite, name="delFavorite"),
    re_path('^product_like/$', views.product_like, name='product_like'),

    re_path('^filter/(?P<f>.*)/(?P<name>.*)$', views.home_filter, name='home_filter'),
]
