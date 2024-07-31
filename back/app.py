from flask import Flask, request, send_file, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

app = Flask(__name__)

# Carregar dados (substitua pelo caminho correto do seu arquivo de dados)
dados = pd.read_csv('data/dados_imoveis.csv')

@app.route('/gerar_grafico', methods=['POST'])
def gerar_grafico():
    try:
        # Receber dados do front-end
        data = request.json
        tipo = data.get('tipo', 'todos')
        bairro = data.get('bairro', '')
        tipo_grafico = data.get('grafico', 'barras')

        # Filtrar dados conforme seleção
        dados_filtrados = dados.copy()
        if tipo != 'todos':
            dados_filtrados = dados_filtrados[dados_filtrados['tipo'].str.lower() == tipo.lower()]
        if bairro:
            dados_filtrados = dados_filtrados[dados_filtrados['bairro'].str.contains(bairro, case=False, na=False)]

        # Configurações iniciais de plotagem
        plt.figure()

        # Gerar o gráfico conforme o tipo escolhido
        if tipo_grafico == 'barras':
            media_preco_bairro = dados_filtrados.groupby('bairro')['preco'].mean().sort_values()
            media_preco_bairro.plot(kind='bar', color='skyblue')
            plt.title('Preço Médio dos Imóveis por Bairro')
            plt.xlabel('Bairro')
            plt.ylabel('Preço Médio')
        elif tipo_grafico == 'pizza':
            distribuicao_tipos = dados_filtrados['tipo'].value_counts()
            distribuicao_tipos.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
            plt.title('Distribuição Percentual de Tipos de Imóveis')
        elif tipo_grafico == 'dispersao':
            sns.scatterplot(data=dados_filtrados, x='metragem', y='preco', hue='tipo', palette='deep')
            plt.title('Relação entre Preço e Metragem dos Imóveis')
            plt.xlabel('Metragem (m²)')
            plt.ylabel('Preço')
        elif tipo_grafico == 'histograma':
            dados_filtrados['preco'] = pd.to_numeric(dados_filtrados['preco'], errors='coerce')
            dados_filtrados['preco'].dropna().plot(kind='hist', bins=20, color='blue', alpha=0.7)
            plt.title('Distribuição de Preços dos Imóveis')
            plt.xlabel('Preço')
            plt.ylabel('Frequência')
        elif tipo_grafico == 'boxplot':
            sns.boxplot(data=dados_filtrados, x='cidade', y='preco', palette='Set3')
            plt.title('Distribuição de Preços por Cidade')
            plt.xlabel('Cidade')
            plt.ylabel('Preço')
        elif tipo_grafico == 'radar':
            categorias = ['preco', 'sqm_price', 'area']
            medias = [dados_filtrados[col].mean() for col in categorias]
            labels = categorias
            valores = medias + [medias[0]]  # Fechar o gráfico

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.plot(labels, valores, marker='o', color='b')
            ax.fill(labels, valores, alpha=0.25, color='b')
            plt.title('Comparação de Atributos dos Imóveis')
        elif tipo_grafico == 'heatmap':
            corr = dados_filtrados.corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5)
            plt.title('Mapa de Calor das Correlações')
        elif tipo_grafico == 'mapa_geografico':
            # Assumindo que há colunas 'latitude' e 'longitude'
            try:
                import folium
                m = folium.Map(location=[dados_filtrados['latitude'].mean(), dados_filtrados['longitude'].mean()], zoom_start=12)
                for idx, row in dados_filtrados.iterrows():
                    folium.Marker([row['latitude'], row['longitude']], popup=row['title']).add_to(m)
                m.save('map.html')
                return send_file('map.html', mimetype='text/html')
            except ImportError:
                return jsonify({"error": "Biblioteca folium não está instalada. Instale-a para usar gráficos de mapas geográficos."}), 500

        # Salvar o gráfico em um objeto de bytes
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        # Retornar o gráfico como resposta
        return send_file(img, mimetype='image/png')
    except Exception as e:
        # Em caso de erro, retorne a mensagem de erro
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
