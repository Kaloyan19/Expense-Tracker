from django.urls import path
from main_app.views import register, home, dashboard, create_expense, list_expenses, update_expense, delete_expense
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("expenses/", list_expenses, name="list_expenses"),
    path("expenses/new/", create_expense, name="create_expense"),
    path("expenses/<int:expense_id>/edit/", update_expense, name="update_expense"),
    path("expenses/<int:expense_id>/delete/", delete_expense, name="delete_expense"),
]