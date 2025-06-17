from django.db import models
from django.contrib.auth.models import User  # import if you want user relation

class AddIncomeModel(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('other income','Other Income')
    ]

    CATEGORY_CHOICES = [
        ('health', 'Health'),
        ('shopping', 'Shopping'),
        ('salary', 'Salary'),
        ('food', 'Food'),
        ('entertainment', 'Entertainment'),
        ('other income','Other Income')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # link to user (optional)
    Income = models.PositiveIntegerField()
    Payment_Method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    Category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    Notes = models.CharField(max_length=200, blank=True, null=True)
    Date = models.DateField()
    Time = models.TimeField()

    def __str__(self):
        return f"{self.user.username} - {self.Category} - {self.Income}"


class AddExpenseModel(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('other income','Other Income')
    ]

    CATEGORY_CHOICES = [
        ('health', 'Health'),
        ('shopping', 'Shopping'),
        ('salary', 'Salary'),
        ('food', 'Food'),
        ('entertainment', 'Entertainment'),
        ('other income','Other Income')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # link to user (optional)
    Expense = models.PositiveIntegerField()
    Payment_Method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    Category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    Notes = models.CharField(max_length=200, blank=True, null=True)
    Date = models.DateField()
    Time = models.TimeField()

    def __str__(self):
        return f"{self.user.username} - {self.Category} - {self.Expense}"
    


class DashboardPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    show_income = models.BooleanField(default=True)
    show_expense = models.BooleanField(default=True)
    show_balance = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Preferences"




# Create your models here.
