from django.urls import path



from .views import DocumentationView, ListCardiew, ListDashboardView, IndexView, ShowDashboardView, CardView

urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('list-dashboard/', ListDashboardView.as_view(), name='list_dashboard'),
	path('list-card/', ListCardiew.as_view(), name='list_card'),
	path('show-dashboard/<int:id>', ShowDashboardView.as_view(), name='show_dashboard'),
	path('show-card/<int:id>', CardView.as_view(), name='show_card'),
	path('documentation', DocumentationView.as_view(), name='documentation')
]