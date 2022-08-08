from django.urls import path



from .views import PublicDashboardView, IndexView, get_dashboard, private_chart, private_dashboard, CardView

urlpatterns = [
	path('private_chart/', private_chart, name='private_chart'),
	path('private_dashboard/', private_dashboard, name='private_dashboard'),
	path('public_dashboard/', PublicDashboardView.as_view(), name='public_dashboard'),
	path('dashboard/<int:id>', get_dashboard, name='get_dashboard'),
	path('card/<int:id>', CardView.as_view(), name='get_card'),
	path('', IndexView.as_view(), name='index')
]