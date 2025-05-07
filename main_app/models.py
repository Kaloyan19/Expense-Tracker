from django.db import models
from django.contrib.auth.models import AbstractUser
from main_app.validators import PositiveNumberValidator

class User(AbstractUser):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('JPY', 'Japanese Yen'),
        ('GBP', 'British Pound'),
        ('CNY', 'Chinese Yuan'),
    ]
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions'
    )

    def __str__(self):
        return self.username

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class Expense(models.Model):  # Keep this version
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category_expense')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[PositiveNumberValidator('The expense must be non-negative and over 0!')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title} - {self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category_budget')
    limit = models.DecimalField(max_digits=10, decimal_places=2, validators=[PositiveNumberValidator('The budget must be non-negative and over 0!')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.limit}"

class RecurringExpense(models.Model):
    FrequencyChoices = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recurring_expenses')
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_recurring_expense')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[PositiveNumberValidator('The expense must be non-negative and over 0!')])
    frequency = models.CharField(
        max_length=20, choices=FrequencyChoices
    )
    next_due_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.title} - {self.frequency}"