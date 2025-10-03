import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from matplotlib.ticker import FuncFormatter

# --- Utilitários ---
def remove_outliers_by_iqr(df, column_name):
    """Remove outliers de uma coluna de DataFrame via método IQR."""
    # CORREÇÃO: Verificar se a coluna existe e tem dados numéricos
    if column_name not in df.columns or df[column_name].isna().all():
        return df
        
    # Garantir que é numérico
    df_clean = df.copy()
    df_clean[column_name] = pd.to_numeric(df_clean[column_name], errors='coerce')
    df_clean = df_clean.dropna(subset=[column_name])
    
    if len(df_clean) == 0:
        return df_clean
        
    Q1 = df_clean[column_name].quantile(0.25)
    Q3 = df_clean[column_name].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    df_filtered = df_clean[(df_clean[column_name] >= lower_bound) & (df_clean[column_name] <= upper_bound)]
    print(f"Limpeza de '{column_name}': {len(df_clean) - len(df_filtered)} outliers removidos.")
    return df_filtered

    
def convert_to_base64(fig):
    """Converte uma figura Matplotlib para uma string base64."""
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return image_base64

# --- Funções de Gráfico ---
def distribution_price_chart(df):
    bins = [0, 500000, 1000000, 1500000, 2500000, 5000000, float('inf')]
    labels = ['< 500k', '500k-1M', '1M-1.5M', '1.5M-2.5M', '2.5M-5M', '> 5M']
    price_distribution = pd.cut(df['price'], bins=bins, labels=labels, right=False).value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    price_distribution.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black', width=0.8)
    ax.set_title('Distribuição de Preços dos Imóveis (Sem Outliers)')
    ax.set_xlabel('Faixa de Preço (R$)')
    ax.set_ylabel('Número de Imóveis')
    ax.tick_params(axis='x', rotation=45)
    
    return convert_to_base64(fig)

def distribution_sqm_price_chart(df):
    bins = [0, 5000, 10000, 15000, 20000, float('inf')]
    labels = ['< 5k', '5k-10k', '10k-15k', '15k-20k', '> 20k']
    sqm_price_distribution = pd.cut(df['sqm_price'], bins=bins, labels=labels, right=False).value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sqm_price_distribution.plot(kind='bar', ax=ax, color='lightgreen', edgecolor='black', width=0.8)
    ax.set_title('Distribuição de Preço por m² (Sem Outliers)')
    ax.set_xlabel('Preço por m² (R$)')
    ax.set_ylabel('Número de Imóveis')
    ax.tick_params(axis='x', rotation=45)

    return convert_to_base64(fig)

def area_properties_chart(df):
    bins = [0, 50, 100, 200, 300, 500, 1000, float('inf')]
    labels = ['0-50', '50-100', '100-200', '200-300', '300-500', '500-1000', '> 1000']
    area_distribution = pd.cut(df['area'], bins=bins, labels=labels, right=False).value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    area_distribution.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black', width=0.8)
    ax.set_title('Distribuição de Área dos Imóveis (m²)')
    ax.set_xlabel('Área (m²)')
    ax.set_ylabel('Número de Imóveis')
    ax.tick_params(axis='x', rotation=45)

    return convert_to_base64(fig)

def comparison_price_chart(df):
    avg_prices = df.groupby('city')['price'].mean().sort_values(ascending=False).head(20)

    fig, ax = plt.subplots(figsize=(12, 7))
    avg_prices.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
    ax.set_title('Preço Médio dos Imóveis por Cidade (Top 20)')
    ax.set_xlabel('Cidade')
    ax.set_ylabel('Preço Médio (R$)')
    
    def format_currency(x, pos):
        if x >= 1_000_000:
            return f'R$ {x/1_000_000:.1f}M'
        return f'R$ {x/1_000:.0f}k'
    ax.yaxis.set_major_formatter(FuncFormatter(format_currency))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    return convert_to_base64(fig)

def proportion_price_chart(df):
    bins = [0, 1000000, 2000000, 3000000, float('inf')]
    labels = ['Menos de R$ 1.000.000', 'R$ 1M a R$ 2M', 'R$ 2M a R$ 3M', 'Mais de R$ 3M']
    price_ranges = pd.cut(df['price'], bins=bins, labels=labels, right=False).value_counts()

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.pie(price_ranges, labels=price_ranges.index, autopct='%1.1f%%', startangle=90)
    ax.set_title('Proporção de Imóveis por Faixa de Preço')
    ax.axis('equal')

    return convert_to_base64(fig)

def total_properties_by_city_chart(df):
    city_counts = df['city'].value_counts().head(20)

    fig, ax = plt.subplots(figsize=(12, 6))
    city_counts.plot(kind='bar', ax=ax, color='lightblue', edgecolor='black')
    ax.set_title('Total de Imóveis por Cidade (Top 20)')
    ax.set_xlabel('Cidade')
    ax.set_ylabel('Número Total de Imóveis')
    ax.tick_params(axis='x', rotation=45)

    return convert_to_base64(fig)