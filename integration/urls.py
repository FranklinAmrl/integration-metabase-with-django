from django.urls import path



from .views import ListDashboardView, IndexView, get_dashboard, private_chart, private_dashboard, CardView

urlpatterns = [
	path('private_chart/', private_chart, name='private_chart'),
	path('private_dashboard/', private_dashboard, name='private_dashboard'),
	path('show-dashboard/', ListDashboardView.as_view(), name='show_dashboard'),
	path('dashboard/<int:id>', get_dashboard, name='get_dashboard'),
	path('show-card/<int:id>', CardView.as_view(), name='show_card'),
	path('', IndexView.as_view(), name='index')
]