import React from 'react';

function ReportsPage({ goToHome }) {
  return (
    <div style={styles.container}>
      <div style={styles.content}>
        <h1>Reports Page</h1>
        <button style={styles.button} onClick={goToHome}>Voltar para Home</button>
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
  content: {
    textAlign: 'center',
  },
  button: {
    margin: '10px',
    padding: '10px 20px',
    fontSize: '16px',
  },
};

export default ReportsPage;
