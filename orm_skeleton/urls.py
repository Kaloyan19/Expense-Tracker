from django.urls import path
from main_app.views import register, home, dashboard
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
]