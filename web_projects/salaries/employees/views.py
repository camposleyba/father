from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, mid_exchrate
from .forms import EmployeeForm

# next to build is another table that will hold year, starting salary, end salary, band, all % increases in all the waves

def home(request):
	employees = Employee.objects.all().order_by('-salary_monthly')
	sum_dolar = 0.0
	sum_pesos = 0.0
	countb7=0
	countb6=0
	countrpa=0
	countwba=0
	countoda=0
	for employee in employees:
		if employee.band == "B7":
			midp = mid_exchrate.objects.get(band='B7')
			exchg = midp.exch_rate
			countb7 += 1
		elif employee.band == "B6":
			midp = mid_exchrate.objects.get(band='B6')
			exchg = midp.exch_rate
			countb6 += 1
		else:
			midp = mid_exchrate.objects.get(band='B8')
			exchg = midp.exch_rate

		if employee.designation == "RPA Developer":
			countrpa += 1
		elif employee.designation == "WBA Developer":
			countwba += 1
		else:
			if employee.first_name == "Bruno":
				countwba += 1
			elif employee.first_name == "Ezequiel":
				countoda += 1
			else:
				pass

		employee.pmr = (employee.salary_monthly/ midp.midpoint)*100
		employee.pmr = round(float(employee.pmr),2)
		employee.salary_usd = employee.salary_monthly / exchg
		employee.salary_usd = round(float(employee.salary_usd),2)
		employee.save()
		sum_dolar += float(employee.salary_usd)
		sum_pesos += float(employee.salary_monthly)
		sum_dolar = round(sum_dolar,2)
		sum_pesos = round(sum_pesos,2)

	context = {
		'employees': employees,
		'sum_dolar': sum_dolar,
		'sum_pesos': sum_pesos,
		'countb7': countb7,
		'countb6': countb6,
		'countoda': countoda,
		'countrpa': countrpa,
		'countwba': countwba,
		'exchg':exchg,
	}
	return render(request, 'home.html', context)

def uploadEmployee(request):
	if request.method == "GET":
		upload_form = EmployeeForm()
		context = {
			'form': upload_form,
		}
		return render(request, 'uploademployee.html', context)
	else:
		upload_form = EmployeeForm(request.POST, request.FILES)
		if upload_form.is_valid():
			upload_form.save()
			return redirect('home')
		else:
			print('something went wrong!')
			return redirect('uploadEmployee')


def employeeDetails(request, pk):
	employee = get_object_or_404(Employee, pk=pk)
	if request.method == "GET":
		context = {
			'employee': employee
		}
		return render(request, 'employeedetails.html', context)
	else:
		try:
			upload_form = EmployeeForm(request.POST, request.FILES, instance=employee)
			if upload_form.is_valid():
				upload_form.save()
			return redirect('home')
		except:
			print("something went wrong")
			context = {
				'employee': employee
			}
			return render(request, 'employeedetails.html', context)

def calculateincrease(request, pk):
	employee = get_object_or_404(Employee, pk=pk)
	if request.method == "POST":
		new_salary = 0.0
		new_pmr = 0.0
		new_salary_usd = 0.0
		if employee.band == "B7":
			midp = mid_exchrate.objects.get(band='B7')
			exchg = midp.exch_rate
		elif employee.band == "B6":
			midp = mid_exchrate.objects.get(band='B6')
			exchg = midp.exch_rate
		else:
			midp = mid_exchrate.objects.get(band='B8')
			exchg = midp.exch_rate
		percen = request.POST.get('percentage')
		try:
			float(percen)
			new_salary = round((float(employee.salary_monthly) * (1+(float(percen)/100))),2)
			midpoint = float(midp.midpoint)
			new_pmr = round((( new_salary / midpoint)*100),2)
			exchgs = float(exchg)
			new_salary_usd = round((new_salary / exchgs),2)
			context = {
				'employee': employee,
				'new_salary': new_salary,
				'new_pmr': new_pmr,
				'new_salary_usd': new_salary_usd,
				'percen': percen
			}
			return render(request, 'salaryincrease.html', context)
		except ValueError:
			error = "Please select a valid percentage increase"
			context = {
				'employee': employee,
				'error': error
				}
			return render(request, 'salaryincrease.html', context)


def saveIncrease(request, pk, salary):
	employee = get_object_or_404(Employee, pk=pk)
	if request.method == "POST":
		salary_incr = float(salary)
		employee.salary_monthly = salary_incr
		employee.save()
		return redirect('home')


def salaryIncrease(request, pk):
	employee = get_object_or_404(Employee, pk=pk)
	if request.method == "GET":
		context = {
			'employee': employee
		}
		return render(request, 'salaryincrease.html', context)
	else:
		try:
			update_form = EmployeeForm(request.POST, request.FILES, instance=employee)
			if update_form.is_valid():
				update_form.save()
			return redirect('home')
		except:
			print("something went wrong")
			context = {
				'employee': employee
			}
			return render(request, 'salaryincrease.html', context)


def employeeDelete(request, pk):
	employee = get_object_or_404(Employee, pk=pk)
	employee.delete()
	return redirect('home')
