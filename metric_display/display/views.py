from django.shortcuts import render
from .forms import *

def home(request):
	if request.method =="POST":
		inputF = inputf(request.POST)
	else:
		inputF = inputf()
	context = {'form':inputF

	}
	return render(request, 'display/home.html', context)
