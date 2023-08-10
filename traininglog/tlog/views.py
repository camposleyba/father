from django.shortcuts import render

def home(request):
	return render(request, "tlog/home.html")
