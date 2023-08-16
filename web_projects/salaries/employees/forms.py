from django.forms import ModelForm
from .models import Employee
from django import forms


class EmployeeForm(ModelForm):
	class Meta:
		model = Employee
		fields = ['first_name','last_name','designation','photo','band','pmr','salary_increase_ytd'
		,'salary_monthly','salary_usd','title']
