from django.shortcuts import render
from .models import Property
import matplotlib.pyplot as plt
import io
import base64
from django.http import HttpResponse

def home(request):
    return render(request, 'properties/home.html')

def chart_view(request):
    properties = Property.objects.all()
    
    # Exemplo de gráfico (Distribuição de preços)
    fig, ax = plt.subplots()
    prices = [int(p.price.replace('R$', '').replace(',', '').strip()) for p in properties if p.price != 'Sob Consulta']
    ax.hist(prices, bins=10, color='skyblue', edgecolor='black')
    ax.set_title('Distribuição de Preços dos Imóveis')
    ax.set_xlabel('Preço (R$)')
    ax.set_ylabel('Número de Imóveis')

    # Converter gráfico para string base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    context = {
        'chart': image_base64,
    }
    return render(request, 'properties/charts.html', context)

def report_view(request):
    properties = Property.objects.all()

    context = {
        'properties': properties,
    }
    return render(request, 'properties/reports.html', context)
