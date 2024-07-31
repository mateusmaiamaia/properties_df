import React from 'react';

function ReportsPage({ goToHome }) {
  // Adicionar lógica para geração de relatórios

  return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <h1>Gerar Relatórios</h1>
      <p>Adicione aqui a lógica para gerar relatórios.</p>
      <button onClick={goToHome} style={{ margin: '10px' }}>
        Voltar para Home
      </button>
    </div>
  );
}

export default ReportsPage;
