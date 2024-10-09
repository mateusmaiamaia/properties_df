import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import re
from .models import Property  

def distribution_price_chart(properties):
    prices = [
        int(p.price.replace('R$', '').replace('.', '').replace(',', '').strip()) 
        for p in properties 
        if p.price != 'Sob Consulta' and re.match(r'^\d+', p.price)
    ]

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

    fig, ax1 = plt.subplots(figsize=(12, 6))

    if prices:
        counts, _ = np.histogram(prices, bins=bins)
        x_positions = np.arange(len(labels))

        ax1.bar(x_positions, counts, color='skyblue', edgecolor='black', width=0.8)
        ax1.set_title('Distribuição de Preços dos Imóveis')
        ax1.set_xlabel('Preço (R$)')
        ax1.set_ylabel('Número de Imóveis')
        ax1.set_xticks(x_positions)
        ax1.set_xticklabels(labels, rotation=45, ha='right')

    return convert_to_base64(fig)

def distribution_sqm_price_chart(properties):
    sqm_prices = [
        int(p.sqm_price.replace('R$', '').replace('.', '').replace(',', '').strip()) 
        for p in properties 
        if p.sqm_price != 'Sob Consulta' and 
           re.match(r'^\d+', p.sqm_price) and 
           p.sqm_price.replace('R$', '').replace('.', '').replace(',', '').strip().isdigit()
    ]

    bins = np.arange(0, 61000, 10000)
    labels = [
        '0 a 10k',
        '10 a 20k',
        '20 a 30k',
        '30 a 40k',
        '40 a 50k',
        '50 a 60k',
        '60k ou mais'
    ]

    fig, ax1 = plt.subplots(figsize=(12, 6))

    if sqm_prices:
        counts, _ = np.histogram(sqm_prices, bins=bins)
        x_positions = np.arange(len(counts))

        ax1.bar(x_positions, counts, color='lightgreen', edgecolor='black', width=0.8)
        ax1.set_title('Distribuição de Preço por Metro Quadrado dos Imóveis')
        ax1.set_xlabel('Preço por m² (R$)')
        ax1.set_ylabel('Número de Imóveis')
        ax1.set_xticks(x_positions)
        ax1.set_xticklabels(labels[:len(counts)], rotation=45, ha='right')

    return convert_to_base64(fig)

def area_properties_chart(properties):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    areas = []

    for p in properties:
        if 'a' in p.area:
            area_range = p.area.split('a')
            area_max_str = area_range[1].replace('m²', '').strip()
            area_min_str = area_range[0].replace('m²', '').strip()
            if area_max_str and area_min_str:
                try:
                    area_max = float(area_max_str.replace('.', '').replace(',', '.'))
                    area_min = float(area_min_str.replace('.', '').replace(',', '.'))
                    areas.append((area_min + area_max) / 2)
                except ValueError:
                    print(f"Erro ao converter área: max='{area_max_str}', min='{area_min_str}'")
        else:
            area_cleaned = p.area.replace('m²', '').strip()
            if area_cleaned:
                try:
                    areas.append(int(float(area_cleaned.replace('.', '').replace(',', '.'))))
                except ValueError:
                    print(f"Erro ao converter área: '{area_cleaned}'")

    bins = [0, 50, 100, 200, 300, 500, 1000, float('inf')]
    if areas:
        counts, _ = np.histogram(areas, bins=bins)
        x_labels = ['0 a 50 m²', '50 a 100 m²', '100 a 200 m²', 
                    '200 a 300 m²', '300 a 500 m²', '500 a 1000 m²', 
                    'Acima de 1000 m²']
        x_positions = np.arange(len(x_labels))

        ax1.bar(x_positions, counts, color='skyblue', edgecolor='black')
        ax1.set_title('Distribuição de Área dos Imóveis')
        ax1.set_xlabel('Área (m²)')
        ax1.set_ylabel('Número de Imóveis')
        ax1.set_xticks(x_positions)
        ax1.set_xticklabels(x_labels, rotation=45, ha='right')

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

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(avg_prices.keys(), avg_prices.values(), color='skyblue')
    ax.set_title('Preço Médio dos Imóveis por Cidade')
    ax.set_xlabel('Cidade')
    ax.set_ylabel('Preço Médio (R$)')
    ax.set_xticklabels(avg_prices.keys(), rotation=45, ha='right')

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
            if price_cleaned.isdigit():
                price = int(price_cleaned)
                if price < 1000000:
                    price_ranges['Menos de R$ 1.000.000'] += 1
                elif 1000000 <= price < 2000000:
                    price_ranges['R$ 1.000.000 a R$ 2.000.000'] += 1
                elif 2000000 <= price < 3000000:
                    price_ranges['R$ 2.000.000 a R$ 3.000.000'] += 1
                else:
                    price_ranges['Mais de R$ 3.000.000'] += 1

    fig, ax = plt.subplots(figsize=(10, 6))
    wedges, texts, autotexts = ax.pie(
        price_ranges.values(),
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 12},
    )

    ax.set_title('Proporção de Imóveis por Faixa de Preço', fontsize=14)

    ax.legend(wedges, price_ranges.keys(), title="Faixas de Preço", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax.axis('equal')

    plt.subplots_adjust(right=0.75)

    return convert_to_base64(fig)

def total_properties_by_city_chart(properties):
    city_counts = {}

    for p in properties:
        city = p.city
        if city in city_counts:
            city_counts[city] += 1
        else:
            city_counts[city] = 1

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(city_counts.keys(), city_counts.values(), color='lightblue')
    ax.set_title('Total de Imóveis por Cidade')
    ax.set_xlabel('Cidade')
    ax.set_ylabel('Número Total de Imóveis')
    ax.set_xticklabels(city_counts.keys(), rotation=45, ha='right')

    return convert_to_base64(fig)

def convert_to_base64(fig):
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)  # Fechar a figura após a conversão
    return image_base64
