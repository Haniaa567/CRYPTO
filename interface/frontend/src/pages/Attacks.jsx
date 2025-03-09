import React, { useState } from 'react';
import Navbar2 from '../components/Navbar/Navbar2';
import '../styles/Services.css';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';
const CardComponent = () => {
  const [isFlipped, setIsFlipped] = useState(false);
  const [visibleMatrices, setVisibleMatrices] = useState({
    matrix1: false,
    matrix2: false,
    matrix3: false
  });

  const flipCard = (e) => {
    setIsFlipped(!isFlipped);
  };

  const stopPropagation = (e) => {
    e.stopPropagation();
  };

  const toggleMatrix = (matrixId, isChecked) => {
    setVisibleMatrices({
      ...visibleMatrices,
      [matrixId]: isChecked
    });
  };

  const lancerOperation = (e) => {
    e.stopPropagation();
    alert("Opération lancée !");
    // Ajoutez ici votre code pour traiter les données
  };

  return (
  <div className="Attack">
      <div className="navbar-container">
          <Navbar2 /> 
      </div>
    <div className="card-container">
      <div className={`card ${isFlipped ? 'flipped' : ''}`}>
        <div className="card-front" onClick={flipCard}>
          <h2 className="card-title">Cliquez pour retourner la carte</h2>
        </div>
        <div className="card-back" onClick={flipCard}>
          <h2 className="card-title">Information</h2>
          <textarea 
            className="large-textarea" 
            placeholder="Entrez votre texte ici..." 
            onClick={stopPropagation}
          />
          
          <div className="checkbox-container">
            <div className="checkbox-item">
              <div className="checkbox-label">
                <input 
                  type="checkbox" 
                  id="key1" 
                  onChange={(e) => toggleMatrix('matrix1', e.target.checked)} 
                  onClick={stopPropagation}
                />
                <label htmlFor="key1">Clé 1</label>
              </div>
              <div className={`matrix-container ${visibleMatrices.matrix1 ? 'visible' : ''}`}>
                <input type="text" className="matrix-input" placeholder="Valeur 1" onClick={stopPropagation} />
                <input type="text" className="matrix-input" placeholder="Valeur 2" onClick={stopPropagation} />
                <input type="text" className="matrix-input" placeholder="Valeur 3" onClick={stopPropagation} />
                <input type="text" className="matrix-input" placeholder="Valeur 4" onClick={stopPropagation} />
              </div>
            </div>
            
            <div className="checkbox-item">
              <div className="checkbox-label">
                <input 
                  type="checkbox" 
                  id="key2" 
                  onChange={(e) => toggleMatrix('matrix2', e.target.checked)} 
                  onClick={stopPropagation}
                />
                <label htmlFor="key2">Clé 2</label>
              </div>
              <div className={`matrix-container ${visibleMatrices.matrix2 ? 'visible' : ''}`}>
                <input type="text" className="matrix-input" placeholder="Valeur 1" onClick={stopPropagation} />
                <input type="text" className="matrix-input" placeholder="Valeur 2" onClick={stopPropagation} />
                <input type="text" className="matrix-input" placeholder="Valeur 3" onClick={stopPropagation} />
                <input type="text" className="matrix-input" placeholder="Valeur 4" onClick={stopPropagation} />
              </div>
            </div>
            
            <div className="checkbox-item">
              <div className="checkbox-label">
                <input 
                  type="checkbox" 
                  id="key3" 
                  onChange={(e) => toggleMatrix('matrix3', e.target.checked)} 
                  onClick={stopPropagation}
                />
                <label htmlFor="key3">Clé 3</label>
              </div>
              <div className={`matrix-container ${visibleMatrices.matrix3 ? 'visible' : ''}`}>
                <input type="text" className="matrix-input" placeholder="Valeur 1" onClick={stopPropagation} />
                <input type="text" className="matrix-input" placeholder="Valeur 2" onClick={stopPropagation} />
                <input type="text" className="matrix-input" placeholder="Valeur 3" onClick={stopPropagation} />
                <input type="text" className="matrix-input" placeholder="Valeur 4" onClick={stopPropagation} />
              </div>
            </div>
          </div>
          
          <button className="launch-button" onClick={lancerOperation}>LANCER</button>
        </div>
      </div>
    </div>
    </div>
  );
};

// Styles CSS pour le composant
const styles = `
  .card-container {
    perspective: 1000px;
    width: 500px;
    height: 600px;
  }

  .card {
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transition: transform 0.8s;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    border-radius: 15px;
    cursor: pointer;
  }

  .card.flipped {
    transform: rotateY(180deg);
  }

  .card-front, .card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 15px;
    padding: 20px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
  }

  .card-front {
    background-color: #2D372F;
    justify-content: center;
    align-items: center;
  }

  .card-back {
    background-color: #2D372F;
    transform: rotateY(180deg);
  }

  .card-title {
    font-size: 24px;
    margin-bottom: 20px;
    text-align: center;
  }

  .large-textarea {
    width: 100%;
    height: 240px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 16px;
    resize: none;
    margin-bottom: 20px;
  }

  .checkbox-container {
    margin-top: 10px;
    margin-bottom: 20px;
  }

  .checkbox-item {
    display: flex;
    align-items: flex-start;
    flex-direction: column;
    margin-bottom: 15px;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
  }

  .checkbox-label label {
    margin-left: 10px;
    font-size: 16px;
  }

  .matrix-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-gap: 10px;
    margin-top: 10px;
    margin-left: 25px;
    width: calc(100% - 25px);
    display: none;
  }

  .matrix-container.visible {
    display: grid;
  }

  .matrix-input {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    cursor: text;
  }

  input, textarea {
    cursor: text;
  }

  .launch-button {
    padding: 12px 24px;
    background-color: #1EA86E;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    margin-top: auto;
    align-self: center;
    width: 180px;
    transition: background-color 0.3s, transform 0.2s;
  }

  .launch-button:hover {
    background-color: #1EA86E;
    transform: scale(1.05);
  }

  .launch-button:active {
    transform: scale(0.95);
  }
`;

// Ajout du style au head du document
const StyleComponent = () => {
  return <style>{styles}</style>;
};

// Composant principal à exporter
const CardApp = () => {
  return (
    <div style={{ 
      fontFamily: 'Arial, sans-serif',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      backgroundColor: '#1B2D1F',
      margin: 0,
      padding: '20px'
    }}>
      <StyleComponent />
      <CardComponent />
    </div>
  );
};

export default CardApp;