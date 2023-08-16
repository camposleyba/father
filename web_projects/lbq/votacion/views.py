from django.shortcuts import render,redirect, get_object_or_404
from votacion.models import votados, categorias

def home(request):
	categ = categorias.objects.all()
	vota = votados.objects.all()
	context = {
		'categorias':categ,
		'votacion': vota,
	}
	return render(request, 'home.html', context)

def voto(request, pk):
	vota = get_object_or_404(votados, pk=pk)
	vota.cuentavotos += 1
	vota.save()
	return redirect('home')

def reset(request, category):
	vota_reset = votados.objects.filter(categoria=category)
	for v in vota_reset:
		v.cuentavotos = 0
		v.save()
	return redirect('home')
