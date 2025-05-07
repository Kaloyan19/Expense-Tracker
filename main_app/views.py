from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm

def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})

class CustomLoginView(LoginView):
    template_name = "login.html"

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

def create_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_expenses")
    else:
        form = ExpenseForm()
    return render(request, "create_expense.html", {"form": form})

def list_expenses(request):
    expenses = Expense.objects.all()
    return render(request, "list_expenses.html", {"expenses": expenses})

def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("list_expenses")
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "update_expense.html", {"form": form})

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    return redirect("list_expenses")