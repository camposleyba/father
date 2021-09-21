from django.shortcuts import render
from .forms import *
from .models import metric
import pandas as pd

#def handle_uploaded_file(f):
#	with open("C:/Users/016434613/Dev/metric_display/display/file.xlsm",'wb+') as destination:
#		for chunk in f.chunks:
#			destination.write(chunk)

def home(request):
	if request.method == "POST":
		input_form = inputf(request.POST, request.FILES)
		context = {
			'form':input_form
		}
		if input_form.is_valid():
			#handle_uploaded_file(request.FILES['inputfile'])
			file = pd.read_excel(request.FILES['inputfile'],sheet_name="Metricdisplay")

			metric.objects.all().delete()
			
			for i in range(file["MANAGER"].size):
				db_metric = metric()
				db_metric.manager = file["MANAGER"][i]
				db_metric.developer = file["DEVELOPERS"][i]
				db_metric.bot_nbr = file["ROBOT NBR"][i]
				db_metric.tot_bots = file["COUNT"][i]
				db_metric.tot_hours = file["HS"][i]
				db_metric.save()


	else:
		input_form = inputf(request.POST or None)
		context = {
			'form':input_form
		}

	return render(request, 'display/home.html', context)
