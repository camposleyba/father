from django.shortcuts import render, redirect
from .forms import *
from .models import metric, metricpivot, backlog, award
import pandas as pd
from django.db.models import Sum
from datetime import date
from decimal import *

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

			file_ = pd.read_excel(request.FILES['inputfile'],sheet_name="Pivotmetricdisplay")

			metricpivot.objects.all().delete()

			for i in range(file_["MANAGER"].size):
				db_metric_ = metricpivot()
				db_metric_.manager = file_["MANAGER"][i]
				db_metric_.developer = file_["DEVELOPERS"][i]
				db_metric_.tot_bots = file_["ROBOT NUMBER"][i]
				db_metric_.tot_hours = file_["HS SAVED"][i]
				db_metric_.save()


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

def backlogpage(request):
	if request.method == "POST":
		input_form = inputf(request.POST, request.FILES)

		if input_form.is_valid():
			#handle_uploaded_file(request.FILES['inputfile'])
			file = pd.read_excel(request.FILES['inputfile'],sheet_name="rfd")

			#-- Start by clearing the database
			backlog.objects.all().delete()
			
			for i in range(file["STATUS"].size):
				db_backlog = backlog()
				db_backlog.status = file["STATUS"][i]
				db_backlog.bot_nbr = file["ROBOT NUMBER"][i]
				db_backlog.title = file["TITLE"][i]
				db_backlog.autotype = file["AUTOMATION TYPE"][i]
				db_backlog.region = file["REGIONS"][i]
				db_backlog.save()
		
		context = {
			'form':input_form
		}

		return redirect('displaybacklog')


	else:
		input_form = inputf(request.POST or None)
		context = {
			'form':input_form,
		}

	return render(request, 'display/backlog.html', context)

def awards(request):
	budget = Decimal(1670)

	fecha = date.today()
	mes = fecha.month



	if mes == 1 or mes == 2 or mes == 3:
		q = "1Q"
	elif mes == 4 or mes == 5 or mes == 6:
		q = "2Q"
	elif mes == 7 or mes == 8 or mes ==9:
		q = "3Q"
	else:
		q = "4Q"

	data = award.objects.filter(quarter=q)
	budgetq = budget / 2
	
	
	if request.method =="POST":
		form = awardform(request.POST or None)
		if form.is_valid():
			developer = form.cleaned_data.get('choiceaward')
			award_db = award.objects.get(quarter=q,developer=developer)
			award_db.goalamount = form.cleaned_data.get('goalamount')
			award_db.wizardamount = form.cleaned_data.get('wizardamount')
			suma = form.cleaned_data.get('goalamount') + form.cleaned_data.get('wizardamount')
			award_db.totalamount = suma
			award_db.save()
	else:
		form = awardform()

	sumatotal = sum(data.values_list('totalamount', flat=True))
	awardbudget = budget - sumatotal
	budgetq = budgetq - sumatotal

	context = {
		'budget':awardbudget,
		'form':form,
		'quarter':q,
		'budgetq':budgetq,
		'data':data,
		'sumatotal':sumatotal
	}
	return render(request, "display/awards.html", context)

def displaybacklog(request):
	data = backlog.objects.filter(status="Ready for development", bot_nbr="nan").order_by("-autotype")
	totitems = backlog.objects.filter(status="Ready for development", bot_nbr="nan").count()
	context = {
		'data':data,
		'totitems':totitems,
	}
	return render(request, "display/displaybacklog.html", context)


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

def pivot(request):
	data = metricpivot.objects.all()
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/pivot.html", context)

def martin(request):
	data = metric.objects.filter(manager="Martin Campos").order_by("developer")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/display.html", context)

def marek(request):
	data = metric.objects.filter(manager="Marek Tarkos").order_by("developer")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/display.html", context)

def andrej(request):
	data = metric.objects.filter(manager="Andrej Csiaki").order_by("developer")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/display.html", context)

def francisco(request):
	data = metric.objects.filter(manager="Francisco del Castillo").order_by("developer")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/display.html", context)

def martinpivot(request):
	data = metricpivot.objects.filter(manager="Martin Campos")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/pivot.html", context)

def marekpivot(request):
	data = metricpivot.objects.filter(manager="Marek Tarkos")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/pivot.html", context)

def andrejpivot(request):
	data = metricpivot.objects.filter(manager="Andrej Csiaki")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/pivot.html", context)

def franciscopivot(request):
	data = metricpivot.objects.filter(manager="Francisco del Castillo")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/pivot.html", context)

def orderbycount(request):
	dire = request.META.get('HTTP_REFERER')
	direlist = dire.split("/")
	
	if direlist[4] == "MC":
		mgr="Martin Campos"
		data = metricpivot.objects.filter(manager=mgr).order_by("-tot_bots")
	elif direlist[4] == "MT":
		mgr="Marek Tarkos"
		data = metricpivot.objects.filter(manager=mgr).order_by("-tot_bots")
	elif direlist[4] == "AC":
		mgr="Andrej Csiaki"
		data = metricpivot.objects.filter(manager=mgr).order_by("-tot_bots")
	elif direlist[4] == "FC":
		mgr="Francisco del Castillo"
		data = metricpivot.objects.filter(manager=mgr).order_by("-tot_bots")
	else:
		data = metricpivot.objects.all().order_by("-tot_bots")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/pivot.html", context)

def orderbyhs(request):
	dire = request.META.get('HTTP_REFERER')
	direlist = dire.split("/")
	
	if direlist[4] == "MC":
		mgr="Martin Campos"
		data = metricpivot.objects.filter(manager=mgr).order_by("-tot_hours")
	elif direlist[4] == "MT":
		mgr="Marek Tarkos"
		data = metricpivot.objects.filter(manager=mgr).order_by("-tot_hours")
	elif direlist[4] == "AC":
		mgr="Andrej Csiaki"
		data = metricpivot.objects.filter(manager=mgr).order_by("-tot_hours")
	elif direlist[4] == "FC":
		mgr="Francisco del Castillo"
		data = metricpivot.objects.filter(manager=mgr).order_by("-tot_hours")
	else:
		data = metricpivot.objects.all().order_by("-tot_hours")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/pivot.html", context)
