from django.forms import ModelForm
from django import forms
from .models import Award

class AwardForm(ModelForm):
	class Meta:
		model = Award
		fields = ['quarter','award_category','who','description','bp','monto']