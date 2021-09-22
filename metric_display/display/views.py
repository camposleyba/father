from django.shortcuts import render, redirect
from .forms import *
from .models import metric
import pandas as pd
from django.db.models import Sum

#def handle_uploaded_file(f):
#	with open("C:/Users/016434613/Dev/metric_display/display/file.xlsm",'wb+') as destination:
#		for chunk in f.chunks:
#			destination.write(chunk)

def home(request):
	if request.method == "POST":
		input_form = inputf(request.POST, request.FILES)

		if input_form.is_valid():
			#handle_uploaded_file(request.FILES['inputfile'])
			file = pd.read_excel(request.FILES['inputfile'],sheet_name="Metricdisplay")

			#-- Start by clearing the database
			metric.objects.all().delete()
			
			for i in range(file["MANAGER"].size):
				db_metric = metric()
				db_metric.manager = file["MANAGER"][i]
				db_metric.developer = file["DEVELOPERS"][i]
				db_metric.bot_nbr = file["ROBOT NBR"][i]
				db_metric.tot_bots = file["COUNT"][i]
				db_metric.tot_hours = file["HS"][i]
				db_metric.save()


		context = {
			'form':input_form
		}

		return redirect('display')


	else:
		input_form = inputf(request.POST or None)
		context = {
			'form':input_form,
		}

	return render(request, 'display/home.html', context)


def display(request):
	data = metric.objects.all()
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/display.html", context)

def martin(request):
	data = metric.objects.filter(manager="Martin Campos")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/display.html", context)

def marek(request):
	data = metric.objects.filter(manager="Marek Tarkos")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/display.html", context)

def andrej(request):
	data = metric.objects.filter(manager="Andrej Csiaki")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/display.html", context)

def francisco(request):
	data = metric.objects.filter(manager="Francisco del Castillo")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/display.html", context)