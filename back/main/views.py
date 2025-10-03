from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.models import Q
from .models import Property
import pandas as pd
from . import charts
import csv

def home(request):
    return render(request, 'main/home.html')

def dashboard_view(request):
    cities = Property.objects.order_by('city').values_list('city', flat=True).distinct()
    context = {
        'cities': cities
    }
    return render(request, 'main/dashboard.html', context)

def get_filtered_data(request):
    selected_city = request.GET.get('city', None)
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    min_area = request.GET.get('min_area', None)
    max_area = request.GET.get('max_area', None)
    
    # AGORA podemos filtrar diretamente no banco pois os campos são numéricos
    properties_qs = Property.objects.all()

    if selected_city and selected_city != "all":
        properties_qs = properties_qs.filter(city=selected_city)

    # Aplicar filtros diretamente no banco (agora funciona!)
    try:
        if min_price:
            properties_qs = properties_qs.filter(price__gte=int(min_price))
        if max_price:
            properties_qs = properties_qs.filter(price__lte=int(max_price))
        if min_area:
            properties_qs = properties_qs.filter(area__gte=int(min_area))
        if max_area:
            properties_qs = properties_qs.filter(area__lte=int(max_area))
    except (ValueError, TypeError) as e:
        print(f"Erro nos filtros: {e}")
        return pd.DataFrame()

    # Converter para DataFrame
    properties_list = list(properties_qs.values())
    
    if not properties_list:
        return pd.DataFrame()
        
    properties_df = pd.DataFrame(properties_list)

    print(f"Dados carregados: {len(properties_df)} registros")

    # Aplicar limpeza de outliers apenas se houver dados suficientes
    if len(properties_df) > 1:
        try:
            cleaned_df = charts.remove_outliers_by_iqr(properties_df.copy(), 'price')
            return cleaned_df
        except Exception as e:
            print(f"Erro na limpeza de outliers: {e}")
            return properties_df
    else:
        return properties_df

def api_chart_data(request, chart_name):
    try:
        final_df = get_filtered_data(request)
        metric = request.GET.get('metric', 'mean') 

        data_for_chart = {}
        
        if final_df is None or final_df.empty:
            return JsonResponse({
                'title': 'Nenhum dado encontrado',
                'labels': [],
                'data': [],
                'datasetLabel': 'Nenhum dado'
            })
        
        if chart_name == 'comparison_price':
            # Agora os dados já vêm numéricos do banco
            city_group = final_df.groupby('city')['price']
            
            if metric == 'median':
                grouped_data = city_group.median()
            elif metric == 'count':
                grouped_data = city_group.count()
            else: 
                grouped_data = city_group.mean()
            
            # Ordenar e pegar top 20
            grouped_data = grouped_data.sort_values(ascending=False).head(20)
            
            if metric == 'median':
                title = 'Preço Mediano por Cidade'
                dataset_label = 'Preço Mediano (R$)'
            elif metric == 'count':
                title = 'Total de Imóveis por Cidade'
                dataset_label = 'Número de Imóveis'
            else: 
                title = 'Preço Médio por Cidade'
                dataset_label = 'Preço Médio (R$)'

            data_for_chart = {
                'title': title,
                'labels': grouped_data.index.tolist(),
                'data': grouped_data.values.tolist(),
                'datasetLabel': dataset_label
            }
            
        elif chart_name == 'proportion_price':
            if len(final_df) > 0:
                bins = [0, 1000000, 2000000, 3000000, float('inf')]
                labels = ['Menos de R$ 1M', 'R$ 1M a R$ 2M', 'R$ 2M a R$ 3M', 'Mais de R$ 3M']
                price_ranges = pd.cut(final_df['price'], bins=bins, labels=labels, right=False).value_counts()
                
                data_for_chart = {
                    'title': 'Proporção de Imóveis por Faixa de Preço',
                    'labels': price_ranges.index.tolist(),
                    'data': price_ranges.values.tolist(),
                }
            else:
                data_for_chart = {
                    'title': 'Proporção de Imóveis por Faixa de Preço',
                    'labels': [],
                    'data': [],
                }
        
        return JsonResponse(data_for_chart)
    
    except Exception as e:
        print(f"Erro em api_chart_data: {e}")
        return JsonResponse({
            'error': f'Erro ao processar dados: {str(e)}',
            'labels': [],
            'data': []
        })

def report_view(request):
    try:
        final_df = get_filtered_data(request)
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="relatorio_imoveis.csv"'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response, delimiter=';')
        
        if final_df is None or final_df.empty:
            writer.writerow(["Nenhum dado encontrado para os filtros selecionados."])
            return response

        available_columns = ['title', 'price', 'sqm_price', 'area', 'city', 'link']
        final_df_export = final_df[[col for col in available_columns if col in final_df.columns]]
        
        writer.writerow(final_df_export.columns)
        for index, row in final_df_export.iterrows():
            writer.writerow(row)
            
        return response
        
    except Exception as e:
        print(f"Erro em report_view: {e}")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="erro.csv"'
        writer = csv.writer(response, delimiter=';')
        writer.writerow([f"Erro ao gerar relatório: {str(e)}"])
        return response