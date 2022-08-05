from django.urls import path



from . import views

urlpatterns = [
	path('private_chart/', views.private_chart, name='private_chart'),
	path('private_dashboard/', views.private_dashboard, name='private_dashboard'),
	path('public_dashboard/', views.DashboardView.as_view(), name='public_dashboard'),
	path('dashboard/<int:id>', views.get_dashboard, name='get_dashboard'),
	path('card/<int:id>', views.CardView.as_view(), name='get_card'),
    path('', views.index, name='index'),
]