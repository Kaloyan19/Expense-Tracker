from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["title", "amount", "category"]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter expense title"}),
            "amount": forms.NumberInput(attrs={"min": "0.01"}),
            "category": forms.Select(),
        }