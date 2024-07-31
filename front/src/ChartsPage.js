import React, { useState } from 'react';
import axios from 'axios';

function ChartsPage({ goToHome }) {
  const [chartType, setChartType] = useState('barras');

  const generateChart = async () => {
    try {
      const response = await axios.post('http://localhost:5000/gerar_grafico', {
        tipo: 'todos',
        grafico: chartType,
      }, {
        responseType: 'blob',
      });
      
      // Criar URL para exibir o gráfico
      const url = URL.createObjectURL(response.data);
      window.open(url);
    } catch (error) {
      console.error("Erro ao gerar gráfico:", error);
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <h1>Gerar Gráficos</h1>
      <select value={chartType} onChange={(e) => setChartType(e.target.value)}>
        <option value="barras">Gráfico de Barras</option>
        <option value="pizza">Gráfico de Pizza</option>
        <option value="dispersao">Gráfico de Dispersão</option>
        <option value="histograma">Histograma</option>
        <option value="boxplot">Box Plot</option>
        <option value="radar">Radar</option>
        <option value="heatmap">Heatmap</option>
        <option value="mapa_geografico">Mapa Geográfico</option>
      </select>
      <br />
      <button onClick={generateChart} style={{ margin: '10px' }}>
        Gerar Gráfico
      </button>
      <br />
      <button onClick={goToHome}>
        Voltar para Home
      </button>
    </div>
  );
}

export default ChartsPage;
