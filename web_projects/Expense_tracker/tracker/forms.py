from django.forms import ModelForm
from django import forms
from .models import Expense, qBudget

class ExpenseForm(ModelForm):
	class Meta:
		model = Expense
		fields = ['quarter','title','description','monto','rendido']

class BudgetForm(ModelForm):
	class Meta:
		model = qBudget
		fields = ['quarter','budget','tc']