from django.urls import path

from . import views

urlpatterns = [
	path('private_chart/', views.private_chart, name='private_chart'),
	path('private_dashboard/', views.private_dashboard, name='private_dashboard'),
	path('public_dashboard/', views.public_dashboard, name='public_dashboard'),
    path('', views.index, name='index'),
]