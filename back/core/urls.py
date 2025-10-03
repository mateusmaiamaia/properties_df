from django.urls import path
from main import views # MUDE A IMPORTAÇÃO DE 'core' PARA 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/chart-data/<str:chart_name>/', views.api_chart_data, name='api_chart_data'),
    path('reports/', views.report_view, name='report_view'),
]