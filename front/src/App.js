import React, { useState } from 'react';
import HomePage from './HomePage';
import ReportsPage from './ReportsPage';
import ChartsPage from './ChartsPage';

function App() {
  const [currentPage, setCurrentPage] = useState('home');

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage goToReports={() => setCurrentPage('reports')} goToCharts={() => setCurrentPage('charts')} />;
      case 'reports':
        return <ReportsPage goToHome={() => setCurrentPage('home')} />;
      case 'charts':
        return <ChartsPage goToHome={() => setCurrentPage('home')} />;
      default:
        return <HomePage goToReports={() => setCurrentPage('reports')} goToCharts={() => setCurrentPage('charts')} />;
    }
  };

  return (
    <div>
      {renderPage()}
    </div>
  );
}

export default App;
