from django.shortcuts import render
from .forms import *

def home(request):
	input_form = addDaysForm(request.POST or None)
	context = {
		'form':input_form,
	}
	return render(request, 'vacation/home.html', context)
