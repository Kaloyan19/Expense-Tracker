from django import forms
from .models import Expense, Category

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["title", "amount", "category"]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter expense title"}),
            "amount": forms.NumberInput(attrs={"min": "0.01"}),
            "category": forms.Select(),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter category name"}),
        }