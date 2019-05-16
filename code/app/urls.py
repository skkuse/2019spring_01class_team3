from app import views
from django.urls import path, re_path
from django.contrib import admin



urlpatterns = [
    re_path('^admin/', admin.site.urls),
    re_path('^login/$', views.login, name="login"),
    re_path('^detail/(?P<pcode>.*)$', views.detail, name="detail"),
]

