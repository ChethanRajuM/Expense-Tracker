from django import forms
from expenseUI.models import AddIncomeModel,AddExpenseModel
from .models import DashboardPreference

class AddIncomeForm(forms.ModelForm):
    class Meta:
        model = AddIncomeModel
        fields = '__all__'
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'}),
            'Time': forms.TimeInput(attrs={'type': 'time'}),
            'Notes': forms.TextInput(attrs={'placeholder': 'Optional'}),
        }
        exclude = ['user']

class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = AddExpenseModel
        fields = '__all__'
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'}),
            'Time': forms.TimeInput(attrs={'type': 'time'}),
            'Notes': forms.TextInput(attrs={'placeholder': 'Optional'}),
        }
        exclude = ['user']


class DashboardPreferenceForm(forms.ModelForm):
    class Meta:
        model = DashboardPreference
        fields = ['show_income', 'show_expense', 'show_balance']
        widgets = {
            'show_income': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_expense': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_balance': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


