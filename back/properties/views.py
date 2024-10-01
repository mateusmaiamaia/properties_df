from django.shortcuts import render
from .models import Property
import matplotlib.pyplot as plt
import io
import base64
import re
from django.http import HttpResponse

def home(request):
    return render(request, 'properties/home.html')

def chart_view(request):
    properties = Property.objects.all()

    if not properties.exists():
        return render(request, 'properties/charts.html', {
            'error_message': 'Nenhum imóvel encontrado.'
        })

    return render(request, 'properties/charts.html', {
        'distribuicao_precos': distribution_price_chart(properties),
        'distribuicao_sqm_price': distribution_sqm_price_chart(properties),
        'area_imoveis': area_properties_chart(properties),
        'comparacao_precos': comparison_price_chart(properties),
        'proporcao_imoveis': proportion_price_chart(properties),
        # Removido 'area_vs_preco':
        # 'area_vs_preco': area_vs_price_scatter_chart(properties),
        'total_imoveis': total_properties_by_city_chart(properties),
    })

def distribution_price_chart(properties):
    prices = [
        int(p.price.replace('R$', '').replace('.', '').replace(',', '').strip()) 
        for p in properties 
        if p.price != 'Sob Consulta' and re.match(r'^\d+', p.price)
    ]

    fig, ax = plt.subplots()
    ax.hist(prices, bins=10, color='skyblue', edgecolor='black')
    ax.set_title('Distribuição de Preços dos Imóveis')
    ax.set_xlabel('Preço (R$)')
    ax.set_ylabel('Número de Imóveis')

    return convert_to_base64(fig)

def distribution_sqm_price_chart(properties):
    sqm_prices = [
        int(p.sqm_price.replace('R$', '').replace('.', '').replace(',', '').strip()) 
        for p in properties 
        if p.sqm_price != 'Sob Consulta' and re.match(r'^\d+', p.sqm_price)
    ]

    fig, ax = plt.subplots()
    ax.hist(sqm_prices, bins=10, color='lightgreen', edgecolor='black')
    ax.set_title('Distribuição de Preço por Metro Quadrado dos Imóveis')
    ax.set_xlabel('Preço por m² (R$)')
    ax.set_ylabel('Número de Imóveis')

    return convert_to_base64(fig)

def area_properties_chart(properties):
    fig, ax = plt.subplots()
    areas = []
    
    for p in properties:
        # Debug print para ver as áreas sendo processadas
        print(f"Processing property: {p.title}, area: {p.area}")
        
        # Verifica se a área é um intervalo
        if 'a' in p.area:
            area_range = p.area.split('a')
            # Remover 'm²' e espaços antes de converter
            area_max_str = area_range[1].replace('m²', '').strip()
            area_min_str = area_range[0].replace('m²', '').strip()
            
            if area_max_str and area_min_str:  # Verifica se não estão vazios
                try:
                    area_max = float(area_max_str.replace('.', '').replace(',', '.'))
                    area_min = float(area_min_str.replace('.', '').replace(',', '.'))
                    areas.append((area_min + area_max) / 2)  # Média do intervalo
                except ValueError:
                    print(f"Erro ao converter área: max='{area_max_str}', min='{area_min_str}'")
        else:
            area_cleaned = p.area.replace('m²', '').strip()
            if area_cleaned:  # Verifica se não está vazio
                try:
                    areas.append(int(float(area_cleaned.replace('.', '').replace(',', '.'))))  # Remover 'm²'
                except ValueError:
                    print(f"Erro ao converter área: '{area_cleaned}'")
                    
    if areas:  # Apenas plotar se houver áreas
        ax.hist(areas, bins=10, color='skyblue', edgecolor='black')
        ax.set_title('Distribuição de Área dos Imóveis')
        ax.set_xlabel('Área (m²)')
        ax.set_ylabel('Número de Imóveis')
    else:
        print("Nenhuma área válida encontrada.")

    return convert_to_base64(fig)

def comparison_price_chart(properties):
    city_prices = {}

    for p in properties:
        city = p.city
        if p.price != 'Sob Consulta':
            price_cleaned = re.sub(r'[^\d]', '', p.price)
            if price_cleaned:
                price = int(price_cleaned)
                if city in city_prices:
                    city_prices[city].append(price)
                else:
                    city_prices[city] = [price]

    avg_prices = {city: sum(prices) / len(prices) for city, prices in city_prices.items()}

    fig, ax = plt.subplots()
    ax.bar(avg_prices.keys(), avg_prices.values(), color='skyblue')
    ax.set_title('Preço Médio dos Imóveis por Cidade')
    ax.set_xlabel('Cidade')
    ax.set_ylabel('Preço Médio (R$)')

    return convert_to_base64(fig)

def proportion_price_chart(properties):
    price_ranges = {
        'Menos de R$ 1.000.000': 0,
        'R$ 1.000.000 a R$ 2.000.000': 0,
        'R$ 2.000.000 a R$ 3.000.000': 0,
        'Mais de R$ 3.000.000': 0,
    }

    for p in properties:
        if p.price != 'Sob Consulta':
            price_cleaned = re.sub(r'[^\d]', '', p.price)
            if price_cleaned:
                price = int(price_cleaned)
                if price < 1000000:
                    price_ranges['Menos de R$ 1.000.000'] += 1
                elif 1000000 <= price < 2000000:
                    price_ranges['R$ 1.000.000 a R$ 2.000.000'] += 1
                elif 2000000 <= price < 3000000:
                    price_ranges['R$ 2.000.000 a R$ 3.000.000'] += 1
                else:
                    price_ranges['Mais de R$ 3.000.000'] += 1

    fig, ax = plt.subplots()
    ax.pie(price_ranges.values(), labels=price_ranges.keys(), autopct='%1.1f%%', startangle=90)
    ax.set_title('Proporção de Imóveis por Faixa de Preço')

    return convert_to_base64(fig)

# A função area_vs_price_scatter_chart foi removida

def total_properties_by_city_chart(properties):
    city_counts = {}

    for p in properties:
        city = p.city
        if city in city_counts:
            city_counts[city] += 1
        else:
            city_counts[city] = 1

    fig, ax = plt.subplots()
    ax.bar(city_counts.keys(), city_counts.values(), color='lightgreen')
    ax.set_title('Total de Imóveis por Cidade')
    ax.set_xlabel('Cidade')
    ax.set_ylabel('Número de Imóveis')

    return convert_to_base64(fig)

def convert_to_base64(fig):
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)  # Fechar a figura após a conversão
    return image_base64

def report_view(request):
    properties = Property.objects.all()

    context = {
        'properties': properties,
    }
    return render(request, 'properties/reports.html', context)
