# properties/views.py
from django.shortcuts import render
from .models import Property
from .charts import (
    distribution_price_chart,
    distribution_sqm_price_chart,
    area_properties_chart,
    comparison_price_chart,
    proportion_price_chart,
    total_properties_by_city_chart,
)

def home(request):
    return render(request, 'properties/home.html')  # Renderiza home.html

def graph_options(request):
    return render(request, 'properties/graph_options.html')  # Renderiza a página com opções de gráficos

def distribution_price_chart_view(request):
    properties = Property.objects.all()
    chart = distribution_price_chart(properties)
    return render(request, 'properties/single_chart.html', {'chart': chart})  # Atualizado para single_chart.html

def distribution_sqm_price_chart_view(request):
    properties = Property.objects.all()
    chart = distribution_sqm_price_chart(properties)
    return render(request, 'properties/single_chart.html', {'chart': chart})  # Atualizado para single_chart.html

def area_properties_chart_view(request):
    properties = Property.objects.all()
    chart = area_properties_chart(properties)
    return render(request, 'properties/single_chart.html', {'chart': chart})  # Atualizado para single_chart.html

def comparison_price_chart_view(request):
    properties = Property.objects.all()
    chart = comparison_price_chart(properties)
    return render(request, 'properties/single_chart.html', {'chart': chart})  # Atualizado para single_chart.html

def proportion_price_chart_view(request):
    properties = Property.objects.all()
    chart = proportion_price_chart(properties)
    return render(request, 'properties/single_chart.html', {'chart': chart})  # Atualizado para single_chart.html

def total_properties_by_city_chart_view(request):
    properties = Property.objects.all()
    chart = total_properties_by_city_chart(properties)
    return render(request, 'properties/single_chart.html', {'chart': chart})  # Atualizado para single_chart.html

def report_view(request):
    properties = Property.objects.all()
    context = {
        'properties': properties,
    }
    return render(request, 'properties/reports.html', context)
