import React from 'react';

function HomePage({ goToReports, goToCharts }) {
  return (
    <div style={styles.container}>
      <div style={styles.buttonGroup}>
        <h1>Home Page</h1>
        <button style={styles.button} onClick={goToReports}>Exportar Relatórios</button>
        <button style={styles.button} onClick={goToCharts}>Ver Gráficos</button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
  },
  buttonGroup: {
    textAlign: 'center',
  },
  button: {
    margin: '10px',
    padding: '10px 20px',
    fontSize: '16px',
  },
};

export default HomePage;
