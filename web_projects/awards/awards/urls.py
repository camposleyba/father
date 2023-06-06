"""awards URL Configuration

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
    path('newaw/', views.newaward, name="newaward"),
    path('admin/', admin.site.urls),
    path('', views.currentawards, name="currentawards"),
    path('1qawards/', views.Q1currentawards, name="Q1currentawards"),
    path('2qawards/', views.Q2currentawards, name="Q2currentawards"),
    path('3qawards/', views.Q3currentawards, name="Q3currentawards"),
    path('4qawards/', views.Q4currentawards, name="Q4currentawards"),
    path('viewaw/<int:award_pk>', views.viewaward, name="viewaward"),
    path('viewaw/<int:award_pk>/delete', views.awarddelete, name="awarddelete"),
]
