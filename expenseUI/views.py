from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from expenseUI.forms import AddIncomeForm, AddExpenseForm, DashboardPreferenceForm
from expenseUI.models import AddIncomeModel, AddExpenseModel, DashboardPreference

from datetime import datetime
from collections import defaultdict
from itertools import chain
from operator import attrgetter
from django.db.models import Sum
import json


@login_required
def handle_form_submission(request, form_class, model_class, template_name):
    data = model_class.objects.filter(user=request.user)

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('eUI')
    else:
        form = form_class()

    return render(request, template_name, {'form': form, 'data': data})


@login_required
def AddIncomeView(request):
    return handle_form_submission(request, AddIncomeForm, AddIncomeModel, 'addincome.html')


@login_required
def AddExpenseView(request):
    return handle_form_submission(request, AddExpenseForm, AddExpenseModel, 'addexpense.html')


@login_required
def ExpenseUIView(request):
    income_data = AddIncomeModel.objects.filter(user=request.user)
    expense_data = AddExpenseModel.objects.filter(user=request.user)

    total_income = sum(i.Income for i in income_data)
    total_expense = sum(e.Expense for e in expense_data)
    remaining_balance = total_income - total_expense

    combined_data = sorted(
        chain(income_data, expense_data),
        key=attrgetter('Date', 'Time'),
        reverse=True
    )[:5]

    preferences, created = DashboardPreference.objects.get_or_create(user=request.user)

    # Calculate top 3 spending categories for expenseUI.html
    category_totals = defaultdict(float)
    for expense in expense_data:
        category_totals[expense.Category] += expense.Expense
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    top_categories = sorted_categories[:3]

    # Calculate percentage for each category
    top_categories_with_pct = []
    for cat, amount in top_categories:
        pct = (amount / total_expense * 100) if total_expense > 0 else 0
        top_categories_with_pct.append({
            'category': cat,
            'amount': amount,
            'percent': round(pct, 2),
        })

    return render(request, 'expenseUI.html', {
        'transactions': combined_data,
        'total_income': total_income,
        'total_expense': total_expense,
        'remaining_balance': remaining_balance,
        'preferences': preferences,
        'top_categories': top_categories_with_pct,
    })


@login_required
def TransactionsView(request):
    income_data = AddIncomeModel.objects.filter(user=request.user)
    expense_data = AddExpenseModel.objects.filter(user=request.user)

    combined_data = sorted(
        chain(income_data, expense_data),
        key=attrgetter('Date', 'Time'),
        reverse=True
    )

    paginator = Paginator(combined_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'transactions.html', {'page_obj': page_obj})


@login_required
def DashboardSettingsView(request):
    preference, created = DashboardPreference.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = DashboardPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            return redirect('eUI')
    else:
        form = DashboardPreferenceForm(instance=preference)

    return render(request, 'dashboard_settings.html', {'form': form})


def get_current_month_summary(user):
    today = datetime.today()
    month = today.month
    year = today.year

    incomes = AddIncomeModel.objects.filter(user=user, Date__month=month, Date__year=year)
    expenses = AddExpenseModel.objects.filter(user=user, Date__month=month, Date__year=year)

    total_income = incomes.aggregate(total=Sum('Income'))['total'] or 0
    total_expense = expenses.aggregate(total=Sum('Expense'))['total'] or 0
    savings = total_income - total_expense

    category_totals = defaultdict(float)
    for expense in expenses:
        category_totals[expense.Category] += expense.Expense

    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    top_categories = sorted_categories[:3]

    chart_data = {
        "labels": ["Income", "Expense"],
        "data": [total_income, total_expense],
    }

    top_categories_with_pct = []
    for cat, amount in top_categories:
        pct = (amount / total_expense * 100) if total_expense > 0 else 0
        top_categories_with_pct.append({
            'category': cat,
            'amount': amount,
            'percent': round(pct, 2),
        })

    return {
        'total_income': total_income,
        'total_expense': total_expense,
        'savings': savings,
        'top_categories': top_categories_with_pct,
        'chart_data': json.dumps(chart_data),
    }


@login_required
def monthly_summary_view(request):
    context = get_current_month_summary(request.user)
    return render(request, 'monthly_summary.html', context)

