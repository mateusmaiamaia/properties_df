import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import re
from django.http import HttpResponse
from django.shortcuts import render
from .models import Property

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
        'total_imoveis': total_properties_by_city_chart(properties),
    })

def distribution_price_chart(properties):
    prices = [
        int(p.price.replace('R$', '').replace('.', '').replace(',', '').strip()) 
        for p in properties 
        if p.price != 'Sob Consulta' and re.match(r'^\d+', p.price)
    ]

    # Defina os bins e as faixas corretamente
    bins = [0, 100000, 300000, 500000, 1000000, 1500000, 2500000, float('inf')]
    labels = [
        'R$ 0k', 
        'R$ 100k', 
        'R$ 300k',
        'R$ 500k', 
        'R$ 1M', 
        'R$ 1.5M', 
        'R$ 2.5M'
    ]

    # Criando o gráfico
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Adicionando o histograma
    ax1.hist(prices, bins=bins, color='skyblue', edgecolor='black')
    ax1.set_title('Distribuição de Preços dos Imóveis')
    ax1.set_xlabel('Preço (R$)')
    ax1.set_ylabel('Número de Imóveis')

    # Corrigindo ticks e rótulos
    ax1.set_xticks(bins[:-1])  # Ajusta para usar os limites inferior de bins
    ax1.set_xticklabels(labels, rotation=45, ha='right')

    # Contagem de imóveis por faixa de preço
    counts, _ = np.histogram(prices, bins=bins)

    # Criando a tabela
    table_data = [
        ['0 a 100', counts[0]],
        ['100 a 300', counts[1]],
        ['300 a 500', counts[2]],
        ['500 a 1.000', counts[3]],
        ['1.000 a 1.500', counts[4]],
        ['1.500 a 2.500', counts[5]],
        ['Acima de 2.500', counts[6]]
    ]

    ax2.axis('off')
    table = ax2.table(cellText=table_data, colLabels=['Preço em mil', 'Quantidade'], loc='center', cellLoc='center')
    table.scale(1, 2)

    plt.subplots_adjust(wspace=0.5)

    return convert_to_base64(fig)

def distribution_sqm_price_chart(properties):
    # Filtrar e processar os preços por metro quadrado
    sqm_prices = [
        int(p.sqm_price.replace('R$', '').replace('.', '').replace(',', '').strip()) 
        for p in properties 
        if p.sqm_price != 'Sob Consulta' and 
           re.match(r'^\d+', p.sqm_price) and 
           p.sqm_price.replace('R$', '').replace('.', '').replace(',', '').strip().isdigit()
    ]

    # Definindo os bins e labels
    bins = np.arange(0, 61000, 10000)  # Isso terá 7 limites
    labels = [
        '0 a 10k',
        '10 a 20k',
        '20 a 30k',
        '30 a 40k',
        '40 a 50k',
        '50 a 60k',
        '60k ou mais'
    ]

    # Criando o gráfico
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Adicionando o histograma
    ax1.hist(sqm_prices, bins=bins, color='lightgreen', edgecolor='black')
    ax1.set_title('Distribuição de Preço por Metro Quadrado dos Imóveis')
    ax1.set_xlabel('Preço por m² (R$)')
    ax1.set_ylabel('Número de Imóveis')

    # Corrigindo ticks e rótulos
    ax1.set_xticks(bins)
    ax1.set_xticklabels(labels, rotation=45, ha='right')

    # Contagem de imóveis por faixa de preço
    counts, _ = np.histogram(sqm_prices, bins)

    # Criando a tabela
    table_data = []
    for i in range(len(counts)):
        label = labels[i] if i < len(labels) else 'Outros'
        table_data.append([label, counts[i]])

    # Adicionando '60k ou mais' se necessário
    if len(counts) < len(labels):
        table_data.append(['60k ou mais', 0])  # Ajuste conforme necessário

    ax2.axis('off')
    table = ax2.table(cellText=table_data, colLabels=['Preço por m²', 'Quantidade'], loc='center', cellLoc='center')
    table.scale(1, 2)

    plt.subplots_adjust(wspace=0.5)

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
