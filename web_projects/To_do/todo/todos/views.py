from django.shortcuts import render, redirect, get_object_or_404
from .forms import TodoForm, categoryForm
from .models import Todo
from django.utils import timezone
from datetime import datetime

def home(request):
	if request.method == 'GET':
		form = categoryForm()
		params = {'form':form}
		return render(request, 'todos/home.html', params)

def currenttodo(request):
	if request.method == 'POST':
		form = categoryForm(request.POST or None)
		if form.is_valid():
			category = form.cleaned_data.get('category')
		todos = Todo.objects.filter(datecompleted__isnull=True, category=category)
		params = {'todos':todos}
		return render(request, 'todos/currenttodo.html', params)
	else:
		currentMonth = datetime.now().month
		match currentMonth:
			case 1:
				quarter="Delivery 1Q23"
			case 2:
				quarter="Delivery 1Q23"
			case 3:
				quarter="Delivery 1Q23"
			case 4:
				quarter="Delivery 2Q23"
			case 5:
				quarter="Delivery 2Q23"
			case 6:
				quarter="Delivery 2Q23"
			case 7:
				quarter="Delivery 3Q23"
			case 8:
				quarter="Delivery 3Q23"
			case 9:
				quarter="Delivery 3Q23"
			case 10:
				quarter="Delivery 4Q23"
			case 11:
				quarter="Delivery 4Q23"
			case 12:
				quarter="Delivery 4Q23"
		todos = Todo.objects.filter(datecompleted__isnull=True, category=quarter)
		params = {'todos':todos}
		return render(request, 'todos/currenttodo.html', params)

def catcurrenttodo(request, category):
	todos = Todo.objects.filter(datecompleted__isnull=True, category=category)
	params = {'todos':todos}
	return render(request, 'todos/catcurrenttodo.html', params)

def completedtodo(request):
	if request.method == 'GET':
		todos = Todo.objects.filter(datecompleted__isnull=False).order_by('-datecompleted')
		params = {'todos':todos}
		return render(request, 'todos/completedtodo.html', params)

def currentcompletedtodo(request):
	if request.method == 'GET':
		currentMonth = datetime.now().month
		match currentMonth:
			case 1:
				quarter="Delivery 1Q23"
			case 2:
				quarter="Delivery 1Q23"
			case 3:
				quarter="Delivery 1Q23"
			case 4:
				quarter="Delivery 2Q23"
			case 5:
				quarter="Delivery 2Q23"
			case 6:
				quarter="Delivery 2Q23"
			case 7:
				quarter="Delivery 3Q23"
			case 8:
				quarter="Delivery 3Q23"
			case 9:
				quarter="Delivery 3Q23"
			case 10:
				quarter="Delivery 4Q23"
			case 11:
				quarter="Delivery 4Q23"
			case 12:
				quarter="Delivery 4Q23"
		todos = Todo.objects.filter(datecompleted__isnull=False, category=quarter).order_by('-datecompleted')
		params = {'todos':todos}
		return render(request, 'todos/completedtodo.html', params)

def create(request):
	if request.method == 'GET':
		form = TodoForm()
		params = {'form': form}
		return render(request, 'todos/createtodo.html', params)
	else:
		try:
			form = TodoForm(request.POST or None)
			if form.is_valid():
				cate = form.cleaned_data.get('category')
			form.save()
			return redirect('catcurrenttodo', category=cate)
		except ValueError:
			params = {'form': TodoForm(),
						'error': 'Bad data passed in. Try again'}
			return render(request, 'todos/createtodo.html', params)

def viewtodo(request, todo_pk):
	todo = get_object_or_404(Todo, pk=todo_pk) #voy a tener que agregar algo del estilo user=request.user con la category
	if request.method == 'GET':
		form = TodoForm(instance=todo) #esta sentencia me permite traer el form con la info dentro de la base de datos del objeto todo
		params = {'todo':todo,
					'form':form
					}
		return render(request, 'todos/viewtodo.html', params)
	else:
		try:
			form = TodoForm(request.POST, instance=todo)
			form.save()
			cate = todo.category
			return redirect('catcurrenttodo', category=cate)
		except ValueError:
			form = TodoForm(instance=todo)
			params = {'todo':todo,
						'form': form,
						'error': 'Bad data passed in. Try again'}
			return render(request, 'todos/viewtodo.html', params)

def completetodo(request, todo_pk):
	todo = get_object_or_404(Todo, pk=todo_pk)
	if request.method == "POST":
		todo.datecompleted = timezone.now()
		todo.save()
		cate = todo.category
		return redirect('catcurrenttodo', category=cate)

def deletetodo(request, todo_pk):
	todo = get_object_or_404(Todo, pk=todo_pk)
	if request.method == "POST":
		cate = todo.category
		todo.delete()
		return redirect('catcurrenttodo', category=cate)
