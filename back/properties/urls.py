# properties/urls.py
from django.contrib import admin
from django.urls import path
from . import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('charts/', views.graph_options, name='graph_options'),  # Página com opções de gráficos
    path('reports/', views.report_view, name='reports'),
    path('charts/distribution_price/', views.distribution_price_chart_view, name='distribution_price_chart'),  # Corrigido o nome da view
    path('charts/distribution_sqm_price/', views.distribution_sqm_price_chart_view, name='distribution_sqm_price_chart'),  # Corrigido o nome da view
    path('charts/area_properties/', views.area_properties_chart_view, name='area_properties_chart'),  # Corrigido o nome da view
    path('charts/comparison_price/', views.comparison_price_chart_view, name='comparison_price_chart'),  # Corrigido o nome da view
    path('charts/proportion_price/', views.proportion_price_chart_view, name='proportion_price_chart'),  # Corrigido o nome da view
    path('charts/total_properties_by_city/', views.total_properties_by_city_chart_view, name='total_properties_by_city_chart'),  # Corrigido o nome da view

    path('reports/', views.report_view, name='reports'),  # Página de relatórios
]


