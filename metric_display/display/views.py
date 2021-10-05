from django.shortcuts import render, redirect
from .forms import *
from .models import metric, metricpivot, backlog, award
import pandas as pd
from django.db.models import Sum
from datetime import date
from decimal import *
from datetime import date

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
				db_metric.tot_bots = int(file["COUNT"][i])
				db_metric.tot_hours = Decimal(file["HS"][i].item())
				db_metric.save()

			file_ = pd.read_excel(request.FILES['inputfile'],sheet_name="Pivotmetricdisplay")

			metricpivot.objects.all().delete()

			for i in range(file_["MANAGER"].size):
				db_metric_ = metricpivot()
				db_metric_.manager = file_["MANAGER"][i]
				db_metric_.developer = file_["DEVELOPERS"][i]
				db_metric_.tot_bots = Decimal(file_["ROBOT NUMBER"][i].item())
				db_metric_.tot_hours = Decimal(file_["HS SAVED"][i].item())
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

	fecha = date.today()
	mes = fecha.month

	if mes == 1 or mes == 2 or mes == 3:
		q = "1Q"
		budget = Decimal(2070)
		budgetq = Decimal(300)
	elif mes == 4 or mes == 5 or mes == 6:
		q = "2Q"
		budget = Decimal(1770)
		budgetq = Decimal(100)
	elif mes == 7 or mes == 8 or mes ==9:
		q = "3Q"
		budget = Decimal(1670)
		budgetq = Decimal(830)
	else:
		q = "4Q"
		budget = Decimal(840)
		budgetq = budget


	data = award.objects.filter(quarter=q).order_by("-totalamount")
	
		
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

def cleanaward(request):
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

	dev_list = ['Pablo Iacovone','Santiago Kitashima','Martin Spadoni',
	'Laura Bisaccia','Andres Grosman','Bruno Secchiari','Ezequiel Ferlauto',
	'Florencia Castelvero','Dario Atach']

	if request.method == "POST":
		totitems = award.objects.filter(quarter=q).count()
		for i in range(totitems):
			developer = dev_list[i]
			award_db = award.objects.get(quarter=q,developer=developer)
			award_db.goalamount = Decimal(0)
			award_db.wizardamount = Decimal(0)
			award_db.totalamount = Decimal(0)
			award_db.save()

	return redirect('awards')

def q1view(request):
	data = award.objects.filter(quarter="1Q").order_by("-totalamount")
	
	form = awardform()

	q="1Q"
	budget = Decimal(2070)
	budgetq = Decimal(300)
	
	sumatotal = sum(data.values_list('totalamount', flat=True))
	awardbudget = budget - sumatotal
	budgetq = budgetq - sumatotal

	context={
		'budget':awardbudget,
		'form':form,
		'quarter':q,
		'budgetq':budgetq,
		'data':data,
		'sumatotal':sumatotal
	}
	return render(request, 'display/awards1q.html', context)


def q2view(request):
	data = award.objects.filter(quarter="2Q").order_by("-totalamount")
	
	form = awardform()
	q="2Q"
	budget = Decimal(1770)
	budgetq = Decimal(100)
	
	sumatotal = sum(data.values_list('totalamount', flat=True))
	awardbudget = budget - sumatotal
	budgetq = budgetq - sumatotal

	context={
		'budget':awardbudget,
		'form':form,
		'quarter':q,
		'budgetq':budgetq,
		'data':data,
		'sumatotal':sumatotal
	}
	return render(request, 'display/awards2q.html', context)


def q3view(request):
	data = award.objects.filter(quarter="3Q").order_by("-totalamount")
	
	form = awardform()
	q="3Q"
	budget = Decimal(1670)
	budgetq = Decimal(830)
	
	sumatotal = sum(data.values_list('totalamount', flat=True))
	awardbudget = budget - sumatotal
	budgetq = budgetq - sumatotal

	context={
		'budget':awardbudget,
		'form':form,
		'quarter':q,
		'budgetq':budgetq,
		'data':data,
		'sumatotal':sumatotal
	}
	return render(request, 'display/awards3q.html', context)


def q4view(request):
	data = award.objects.filter(quarter="4Q").order_by("-totalamount")
	
	form = awardform()
	q="4Q"
	budget = Decimal(840)
	budgetq = Decimal(840)
	
	sumatotal = sum(data.values_list('totalamount', flat=True))
	awardbudget = budget - sumatotal
	budgetq = budgetq - sumatotal

	context={
		'budget':awardbudget,
		'form':form,
		'quarter':q,
		'budgetq':budgetq,
		'data':data,
		'sumatotal':sumatotal
	}
	return render(request, 'display/awards4q.html', context)




def displaybacklog(request):
	hoy = date.today()
	data = backlog.objects.filter(status="Ready for development", bot_nbr="nan").order_by("-autotype")
	totitems = backlog.objects.filter(status="Ready for development", bot_nbr="nan").count()
	context = {
		'data':data,
		'totitems':totitems,
		'fecha':hoy
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
	data = metricpivot.objects.filter(manager="Martin Campos").order_by("-tot_bots")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/pivot.html", context)

def marekpivot(request):
	data = metricpivot.objects.filter(manager="Marek Tarkos").order_by("-tot_bots")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/pivot.html", context)

def andrejpivot(request):
	data = metricpivot.objects.filter(manager="Andrej Csiaki").order_by("-tot_bots")
	sumabots = sum(data.values_list('tot_bots', flat=True))
	sumahs = sum(data.values_list('tot_hours', flat=True))
	context = {
		'data':data,
		'sumabots':sumabots,
		'sumahs':sumahs
	}
	return render(request, "display/pivot.html", context)

def franciscopivot(request):
	data = metricpivot.objects.filter(manager="Francisco del Castillo").order_by("-tot_bots")
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

def jglui(request):
	hoy = date.today()
	data = backlog.objects.filter(autotype="Journal - GLUI", bot_nbr="nan")
	totitems = backlog.objects.filter(autotype="Journal - GLUI", bot_nbr="nan").count()
	context = {
		'data':data,
		'totitems':totitems,
		'fecha':hoy
	}
	return render(request, "display/displaybacklog.html", context)

def jcglui(request):
	hoy = date.today()
	data = backlog.objects.filter(autotype="Journal - CGLUI", bot_nbr="nan")
	totitems = backlog.objects.filter(autotype="Journal - CGLUI", bot_nbr="nan").count()
	context = {
		'data':data,
		'totitems':totitems,
		'fecha':hoy
	}
	return render(request, "display/displaybacklog.html", context)

def jierp(request):
	hoy = date.today()
	data = backlog.objects.filter(autotype="Journal - iERP", bot_nbr="nan")
	totitems = backlog.objects.filter(autotype="Journal - iERP", bot_nbr="nan").count()
	context = {
		'data':data,
		'totitems':totitems,
		'fecha':hoy
	}
	return render(request, "display/displaybacklog.html", context)

def recon(request):
	hoy = date.today()
	data = backlog.objects.filter(autotype="Reconciliation", bot_nbr="nan")
	totitems = backlog.objects.filter(autotype="Reconciliation", bot_nbr="nan").count()
	context = {
		'data':data,
		'totitems':totitems,
		'fecha':hoy
	}
	return render(request, "display/displaybacklog.html", context)

def reporting(request):
	hoy = date.today()
	data = backlog.objects.filter(autotype="Reporting", bot_nbr="nan")
	totitems = backlog.objects.filter(autotype="Reporting", bot_nbr="nan").count()
	context = {
		'data':data,
		'totitems':totitems,
		'fecha':hoy
	}
	return render(request, "display/displaybacklog.html", context)

def customsol(request):
	hoy = date.today()
	data = backlog.objects.filter(autotype="Customized Solution", bot_nbr="nan")
	totitems = backlog.objects.filter(autotype="Customized Solution", bot_nbr="nan").count()
	context = {
		'data':data,
		'totitems':totitems,
		'fecha':hoy
	}
	return render(request, "display/displaybacklog.html", context)
