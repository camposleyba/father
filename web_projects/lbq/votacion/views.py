from django.shortcuts import render,redirect, get_object_or_404
from votacion.models import votados, categorias
from django.db.models import Sum

def home(request):
	categ = categorias.objects.all()
	vota = votados.objects.all()
	context = {
		'categorias':categ,
		'votacion': vota,
	}
	return render(request, 'home.html', context)

def voto(request, pk):
	max_votos = 14
	vota = get_object_or_404(votados, pk=pk)
	votas = votados.objects.filter(categoria=vota.categoria)
	dict_votos = {}
	suma = votados.objects.filter(categoria=vota.categoria).aggregate(Sum('cuentavotos'))
	verdadero = False
	if suma['cuentavotos__sum'] < max_votos:
		for vot in votas:
			porcentaje = vot.cuentavotos / max_votos
			if porcentaje > 0.5:
				verdadero = True
				vota = get_object_or_404(votados, pk=vot.pk)
	else:
		for vot in votas:
			porcentaje = vot.cuentavotos / max_votos
			dict_votos[vot.pk]=porcentaje
		maximo = max(dict_votos.values())
		for k, v in dict_votos.items():
			if maximo == v:
				vota = get_object_or_404(votados, pk=k)
				verdadero=True
				break
	if not verdadero:
		vota.cuentavotos += 1
		vota.save()
		return redirect('home')
	else:
		categ = categorias.objects.all()
		votas = votados.objects.all()
		category = categorias.objects.get(categoria=vota.categoria)
		category.ganador = vota.apodo
		tot_votos = vota.cuentavotos
		category.save()
		context = {
			'categorias':categ,
			'votacion': votas,
			'tot_votos':tot_votos,
		}
		return render(request, 'home.html', context)



def reset(request, category):
	vota_reset = votados.objects.filter(categoria=category)
	ganador_reset = categorias.objects.get(categoria=category)
	ganador_reset.ganador = None
	ganador_reset.save()
	for v in vota_reset:
		v.cuentavotos = 0
		v.save()
	return redirect('home')
