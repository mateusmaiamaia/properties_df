import React, { useState } from 'react';
import ChartsPage from './ChartsPage';
import ReportsPage from './ReportsPage';

function App() {
  const [currentPage, setCurrentPage] = useState('home');

  const renderPage = () => {
    switch (currentPage) {
      case 'charts':
        return <ChartsPage goToHome={() => setCurrentPage('home')} />;
      case 'reports':
        return <ReportsPage goToHome={() => setCurrentPage('home')} />;
      default:
        return (
          <div style={{ textAlign: 'center', marginTop: '20px' }}>
            <button onClick={() => setCurrentPage('charts')} style={{ margin: '10px' }}>
              Gerar Gráficos
            </button>
            <button onClick={() => setCurrentPage('reports')} style={{ margin: '10px' }}>
              Gerar Relatórios
            </button>
          </div>
        );
    }
  };

  return (
    <div>
      {renderPage()}
    </div>
  );
}

export default App;
