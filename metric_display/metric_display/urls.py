"""metric_display URL Configuration

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
from display import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('display/', views.display, name="display"),
    path('pivot/', views.pivot, name="pivot"),
    path('awards/', views.awards, name="awards"),
    path('awards/CL/', views.cleanaward, name="cleanaward"),
    path('backlog/', views.backlogpage, name="backlogpage"),
    path('displaybacklog/', views.displaybacklog, name="displaybacklog"),

    path('awards/1Q/', views.q1view, name="q1view"),
    path('awards/2Q/', views.q2view, name="q2view"),
    path('awards/3Q/', views.q3view, name="q3view"),
    path('awards/4Q/', views.q4view, name="q4view"),

    path('pivot/orderby/', views.orderbycount, name="orderbycount"),
    path('pivot/orderbyhs/', views.orderbyhs, name="orderbyhs"),
    
    path('filter/MC/', views.martin, name="martin"),
    path('filter/MT/', views.marek, name="marek"),
    path('filter/AC/', views.andrej, name="andrej"),
    path('filter/FC/', views.francisco, name="francisco"),
    path('pivot/MC/', views.martinpivot, name="martinpivot"),
    path('pivot/MT/', views.marekpivot, name="marekpivot"),
    path('pivot/AC/', views.andrejpivot, name="andrejpivot"),
    path('pivot/FC/', views.franciscopivot, name="franciscopivot"),

    path('backlog/JG/', views.jglui, name="jglui"),
    path('backlog/JCG/', views.jcglui, name="jcglui"),
    path('backlog/iERP/', views.jierp, name="jierp"),
    path('backlog/REC/', views.recon, name="recon"),
    path('backlog/REP/', views.reporting, name="reporting"),
    path('backlog/CS/', views.customsol, name="customsol"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
