from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm, BudgetForm
from .models import Expense, qBudget
from django.db.models import Sum
from datetime import datetime

def tracker(request):
	if request.method == "GET":
		form = ExpenseForm()
		params = {'form':form}
		return render(request, 'tracker/tracker.html', params)
	else:
		try:
			exp_obj = Expense()
			form = ExpenseForm(request.POST or None)
			if form.is_valid():
				form.save()
				return redirect('currentexpense')
		except ValueError:
			form = ExpenseForm()
			params = {'form':form, 'error':'Something went wrong. We were not able to save the item. Try again.'}
			return render(request, 'tracker/tracker.html', params)

def currentexpense(request):
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
	budg = get_object_or_404(qBudget, quarter=quarter)
	qbudget = budg.budget * budg.tc
	expenses = Expense.objects.filter(quarter=quarter)
	expamt = Expense.objects.aggregate(Sum('monto'))
	exp_amt = expamt['monto__sum']
	qbudgetfinal = qbudget - exp_amt
	params={'expenses':expenses, 'budget':qbudgetfinal, 'spent':exp_amt}
	return render(request, "tracker/currentexpense.html", params)

def budget(request):
	if request.method == "GET":
		form = BudgetForm()
		params = {'form':form}
		return render(request, 'tracker/budget.html', params)
	else:
		try:
			form = BudgetForm(request.POST or None)
			if form.is_valid():
				form.save()
				return redirect('currentexpense')
		except ValueError:
			form = BudgetForm()
			params = {'form':form, 'error':'Issue when loading budget. Try again.'}
			return render(request, 'tracker/budget.html', params)

def currentbudget(request):
	q_budget = qBudget.objects.all()
	params = {'qbudget':q_budget}
	return render(request, 'tracker/currentbudget.html', params)

def qbudgetget(request, budget_pk):
	budget_obj = get_object_or_404(qBudget, pk=budget_pk)
	if request.method == 'GET':
		form = BudgetForm(instance=budget_obj) #esta sentencia me permite traer el form con la info dentro de la base de datos del objeto todo
		params = {'qbudget':budget_obj,
					'form':form
					}
		return render(request, 'tracker/qbudget.html', params)
	else:
		try:
			form = BudgetForm(request.POST, instance=budget_obj)
			form.save()
			return redirect('currentbudget')
		except ValueError:
			form = BudgetForm(instance=budget_obj)
			params = {'qbudget':budget_obj,
						'form': form,
						'error': 'Bad data passed in. Try again'}
			return redirect(request, 'tracker/qbudget.html', params)

def budgetdelete(request, budget_pk):
	budget_obj = get_object_or_404(qBudget, pk=budget_pk)
	budget_obj.delete()
	return redirect('currentbudget')

def expense(request, expense_pk):
	expense_obj = get_object_or_404(Expense, pk=expense_pk)
	if request.method == 'GET':
		form = ExpenseForm(instance=expense_obj) #esta sentencia me permite traer el form con la info dentro de la base de datos del objeto todo
		params = {'expense':expense_obj,
					'form':form
					}
		return render(request, 'tracker/expense.html', params)
	else:
		try:
			form = ExpenseForm(request.POST, instance=expense_obj)
			form.save()
			return redirect('currentexpense')
		except ValueError:
			form = ExpenseForm(instance=expense_obj)
			params = {'expense':expense_obj,
						'form': form,
						'error': 'Bad data passed in. Try again'}
			return redirect(request, 'tracker/expense.html', params)

def expensedelete(request, expense_pk):
	expense_obj = get_object_or_404(Expense, pk=expense_pk)
	expense_obj.delete()
	return redirect('currentexpense')
	




