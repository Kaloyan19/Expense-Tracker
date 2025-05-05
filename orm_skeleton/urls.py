from django.contrib import admin
from django.urls import path
from main_app.views import register, home

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("admin/", admin.site.urls),
]