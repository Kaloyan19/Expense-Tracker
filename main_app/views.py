from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm
from django.db.models import Sum

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
    print("DEBUG: request.user =", request.user)  # ✅ Check what request.user is returning
    print("DEBUG: request.user type =", type(request.user))  # ✅ Check its type

    # ✅ Ensure request.user is authenticated
    if not request.user.is_authenticated:
        print("ERROR: User is not authenticated!")
        return redirect("login")  # Redirect to login if user is invalid

    # ✅ Use request.user.id instead of request.user
    expenses = Expense.objects.filter(user_id=request.user.id).order_by("-date")  # 🔥 Order by most recent

    total_spent = expenses.aggregate(Sum("amount"))["amount__sum"] or 0

    # ✅ Show last 5 recent expenses
    recent_expenses = expenses[:5]

    # ✅ Fix category query: Use "category" instead of "category_id"
    category_data = list(expenses.values("category").annotate(total=Sum("amount")))

    # ✅ Convert category objects to category names
    for item in category_data:
        if item["category"]:  # Ensure category is not None
            category_obj = Category.objects.get(id=item["category"])
            item["category"] = category_obj.name  # Convert ID to name

    # ✅ Fetch expenses grouped by month
    monthly_data = list(expenses.values("date__month").annotate(total=Sum("amount")).order_by("date__month"))

    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October",
        11: "November", 12: "December"
    }

    monthly_labels = [month_names.get(item["date__month"], "Unknown") for item in monthly_data]
    monthly_values = [item["total"] for item in monthly_data]

    result = {
        "total_spent": total_spent,
        "recent_expenses": recent_expenses,  # ✅ Pass recent expenses
        "category_data": category_data,
        "monthly_labels": monthly_labels,
        "monthly_values": monthly_values,
    }

    return render(request, "dashboard.html", result)

@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user  # ✅ Assign category to the logged-in user
            category.save()
            return redirect("create_expense")  # ✅ Redirect back to expense creation
    else:
        form = CategoryForm()

    return render(request, "add_category.html", {"form": form})

@login_required
def create_expense(request):
    print("DEBUG: request.user =", request.user)  # ✅ Check what request.user is returning
    print("DEBUG: request.user type =", type(request.user))  # ✅ Check its type
    print("DEBUG: request.user.is_authenticated =", request.user.is_authenticated)  # ✅ Check if user is logged in

    # ✅ Ensure request.user is authenticated
    if not request.user.is_authenticated:
        print("ERROR: User is not authenticated!")
        return redirect("login")  # Redirect to login if user is invalid

    categories = Category.objects.filter(user=request.user)  # ✅ Show only the logged-in user's categories

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # ✅ Assign the correct user
            expense.save()
            return redirect("list_expenses")
    else:
        form = ExpenseForm()

    return render(request, "create_expense.html", {"form": form, "categories": categories})
def list_expenses(request):
    expenses = Expense.objects.filter(user_id=request.user.id).order_by("-date")  # 🔥 Order by most recent
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

