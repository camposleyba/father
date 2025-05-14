from django.shortcuts import render, redirect, get_object_or_404
from .models import Award
from .forms import AwardForm
from datetime import datetime

def newaward(request):
	if request.method == "GET":
		form = AwardForm()
		params = {'form':form}
		return render(request, 'tracker/newaward.html', params)
	else:
		try:
			aw_obj = Award()
			form = AwardForm(request.POST or None)
			if form.is_valid():
				form.save()
				return redirect('currentawards')
		except ValueError:
			form = AwardForm()
			params = {'form':form, 'error':'Something went wrong. We were not able to save the item. Try again.'}
			return render(request, 'tracker/newaward.html', params)

def currentawards(request):
	currentMonth = datetime.now().month
	match currentMonth:
		case 1:
			quarter="1Q"
		case 2:
			quarter="1Q"
		case 3:
			quarter="1Q"
		case 4:
			quarter="2Q"
		case 5:
			quarter="2Q"
		case 6:
			quarter="2Q"
		case 7:
			quarter="3Q"
		case 8:
			quarter="3Q"
		case 9:
			quarter="3Q"
		case 10:
			quarter="4Q"
		case 11:
			quarter="4Q"
		case 12:
			quarter="4Q"
	awards = Award.objects.filter(quarter=quarter, is_active=True)
	params={'awards':awards}
	return render(request, "tracker/currentawards.html", params)

def Q1currentawards(request):
	quarter = "1Q"
	awards = Award.objects.filter(quarter=quarter, is_active=True)
	params={'awards':awards}
	return render(request, "tracker/currentawards.html", params)

def Q2currentawards(request):
	quarter = "2Q"
	awards = Award.objects.filter(quarter=quarter, is_active=True)
	params={'awards':awards}
	return render(request, "tracker/currentawards.html", params)

def Q3currentawards(request):
	quarter = "3Q"
	awards = Award.objects.filter(quarter=quarter, is_active=True)
	params={'awards':awards}
	return render(request, "tracker/currentawards.html", params)

def Q4currentawards(request):
	quarter = "4Q"
	awards = Award.objects.filter(quarter=quarter, is_active=True)
	params={'awards':awards}
	return render(request, "tracker/currentawards.html", params)


def viewaward(request, award_pk):
	aw_obj = get_object_or_404(Award, pk=award_pk)
	if request.method == 'GET':
		form = AwardForm(instance=aw_obj) #esta sentencia me permite traer el form con la info dentro de la base de datos del objeto todo
		params = {'award':aw_obj,
					'form':form
					}
		return render(request, 'tracker/viewaward.html', params)
	else:
		try:
			form = AwardForm(request.POST, instance=aw_obj)
			form.save()
			return redirect('currentawards')
		except ValueError:
			form = AwardForm(instance=aw_obj)
			params = {'award':aw_obj,
						'form': form,
						'error': 'Bad data passed in. Try again'}
			return redirect(request, 'tracker/viewaward.html', params)

def awarddelete(request, award_pk):
	aw_obj = get_object_or_404(Award, pk=award_pk)
	aw_obj.delete()
	return redirect('currentawards')
