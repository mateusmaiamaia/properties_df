import React from 'react';

function ChartsPage({ goToHome }) {
  return (
    <div>
      <h1>Charts Page</h1>
      <button onClick={goToHome}>Voltar para Home</button>
    </div>
  );
}

export default ChartsPage;
