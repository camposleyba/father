"""Expense_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.currentexpense, name="currentexpense"),
    path('newexp/', views.tracker, name="tracker"),
    path('currentbudget/', views.currentbudget, name="currentbudget"),
    path('1Qexpenses/', views.Q1expense, name="Q1expense"),
    path('2Qexpenses/', views.Q2expense, name="Q2expense"),
    path('3Qexpenses/', views.Q3expense, name="Q3expense"),
    path('4Qexpenses/', views.Q4expense, name="Q4expense"),
    path('budget/', views.budget, name="budget"),
    path('qbudget/<int:budget_pk>', views.qbudgetget, name="qbudgetget"),
    path('qbudget/<int:budget_pk>/delete', views.budgetdelete, name="budgetdelete"),
    path('expense/<int:expense_pk>', views.expense, name="expense"),
    path('expense/<int:expense_pk>/delete', views.expensedelete, name="expensedelete"),
]
