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
