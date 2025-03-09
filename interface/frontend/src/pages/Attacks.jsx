import React, { useEffect, useRef, useState } from 'react';
import Swiper from 'swiper';
import 'swiper/css';
import Navbar2 from '../components/Navbar/Navbar2';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';
import '../styles/Services.css';
import { VscDebugRestart } from "react-icons/vsc";
import Spinner from 'react-bootstrap/Spinner';
import { useKeycloak } from '@react-keycloak/web';
import { useTranslation } from 'react-i18next';

function Page1() {
  const { keycloak } = useKeycloak();
  const swiperRef = useRef(null);
  const prevButtonRef = useRef(null);
  const nextButtonRef = useRef(null);
  const { t } = useTranslation();

  const [flippedCardId, setFlippedCardId] = useState(null);
  const [clickedCardId, setClickedCardId] = useState(null);
  const [canFlip, setCanFlip] = useState(true);
  const [showHashMethod, setShowHashMethod] = useState(false);
  const [selectedHashMethod, setSelectedHashMethod] = useState('md5');
  const [loading, setLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [inputValue, setInputValue] = useState("");
  
  // State variables
  const [useMatrix, setUseMatrix] = useState(false);
  const [matrixValues, setMatrixValues] = useState(["", "", "", ""]);
  const [responseMessage4, setResponseMessage4] = useState("");
  
  // New state variables
  const [decryptWithoutKey, setDecryptWithoutKey] = useState(false);
  const [withKnownWord, setWithKnownWord] = useState(false);
  const [knownWord, setKnownWord] = useState("");
  const [knownWordHash, setKnownWordHash] = useState("");

  const getUserId = () => {
    return keycloak.tokenParsed?.sub || '';
  };
  
  const handleCardClick = (id, event) => {
    if (!canFlip) return;
    event.stopPropagation();

    if (clickedCardId === id) {
      setClickedCardId(null);
    } else {
      setClickedCardId(id);
    }
    setFlippedCardId(flippedCardId === id ? null : id);
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        flippedCardId &&
        !event.target.closest('.back') &&
        !event.target.closest('.swiper-button-prev') &&
        !event.target.closest('.swiper-button-next') &&
        canFlip === false
      ) {
        setFlippedCardId(null);
        setClickedCardId(null);
      }
    };

    document.addEventListener('click', handleClickOutside);

    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, [flippedCardId, canFlip]);

  useEffect(() => {
    if (flippedCardId) {
      setCanFlip(false);
    } else {
      setCanFlip(true);
    }
  }, [flippedCardId]);

  const handleIconClick = () => {
    setInputValue("");
    setMatrixValues(["", "", "", ""]);
    setUseMatrix(false);
    setDecryptWithoutKey(false);
    setWithKnownWord(false);
    setKnownWord("");
    setKnownWordHash("");
    setResponseMessage4("");
    setIsSubmitted(false);
    setLoading(false);
  };

  const handleHashMethodChange = (e) => {
    setSelectedHashMethod(e.target.value);
  };

  const handleMatrixInputChange = (index, value) => {
    const newMatrixValues = [...matrixValues];
    newMatrixValues[index] = value;
    setMatrixValues(newMatrixValues);
  };

  const handleSubmitHybrid = async() => {
    if (!keycloak.authenticated) {
      console.log("User not authenticated");
      keycloak.login();
      return;
    }
    try {
      setIsSubmitted(true);
      setLoading(true);
      const hashedPassword = document.getElementById(`hash-4`).value;
      
      // Prepare request body based on whether matrix is used
      const requestBody = {
        hashed_password: hashedPassword,
        hash_algorithm: selectedHashMethod,
        enregistrement: true,
        iduser: getUserId(),
      };
      
      // Add matrix values if checkbox is checked
      if (useMatrix) {
        requestBody.matrix_key = matrixValues;
      }
      
      // Add decrypt without key flag if checkbox is checked
      if (decryptWithoutKey) {
        requestBody.decrypt_without_key = true;
      }
      
      // Add known word and its hash if checkbox is checked
      if (withKnownWord) {
        requestBody.known_word = knownWord;
        requestBody.known_word_hash = knownWordHash;
      }
    
      const hybrid = await fetch('http://127.0.0.1:8001/attaque/hybrid', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${keycloak.token}`
        },
        body: JSON.stringify(requestBody),
      })
      if (!hybrid.ok) {
        const errorText = await hybrid.text();
        console.error('Response error:', errorText);
        throw new Error(`HTTP error! status: ${hybrid.status}, message: ${errorText}`);
      }
  
      const data = await hybrid.json();
      
      if (data.success) {
        setResponseMessage4(`Your password is : ${data.password_found}`);
      } else {
        setResponseMessage4("Password not found !");
      }
    } catch (error) {
      console.error('Error:', error);
      setResponseMessage4("An error occurred during the request!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div id="Attacks">
      <div className="navbar-container">
        <Navbar2 />
      </div>

      <div className="centered-card-container">
        {/* Single Card */}
        <div
          className={`card-slide ${flippedCardId === '4' ? 'flipped' : ''} ${clickedCardId === '4' ? 'selected' : ''}`}
          onClick={(e) => handleCardClick('4', e)}
        >
          <div className="slide-content">
            <div className="front">
              <div className='about'>
                <h1 className='front-title'>{t('Hill Cipher')}</h1>
                <h1 id='ab'>{t('about')}</h1>
                <p id='description'>
                  {t('hybrid-desc')}
                </p>
              </div>
            </div>
            <div className="back">
              <div className="input-content"> 
                <h1 id='attack-title'>{t('Hill')}</h1>
                <input 
                  type="text" 
                  id='hash-4' 
                  placeholder={t('hash-placeholder')} 
                  value={inputValue} 
                  onChange={(e) => setInputValue(e.target.value)} 
                />
                
                {/* Checkbox for matrix key */}
                <div className="checkbox-container">
                  <input 
                    type="checkbox" 
                    id="use-matrix" 
                    checked={useMatrix}
                    onChange={(e) => {e.stopPropagation(); setUseMatrix(e.target.checked)}}
                  />
                  <label id='key-title' htmlFor="use-matrix">Use Matrix Key</label>
                </div>
                
                {/* Matrix input fields */}
                {useMatrix && (
                  <div className="matrix-container">
                    {matrixValues.map((value, index) => (
                      <input
                        key={index}
                        type="text"
                        className="matrix-input"
                        placeholder={`Value ${index + 1}`}
                        value={value}
                        onChange={(e) => {e.stopPropagation(); handleMatrixInputChange(index, e.target.value)}}
                      />
                    ))}
                  </div>
                )}
                
                {/* New checkbox for decrypt without key */}
                <div className="checkbox-container">
                  <input 
                    type="checkbox" 
                    id="decrypt-without-key" 
                    checked={decryptWithoutKey}
                    onChange={(e) => {e.stopPropagation(); setDecryptWithoutKey(e.target.checked)}}
                  />
                  <label id='key-title' htmlFor="decrypt-without-key">Decrypt Without Key</label>
                </div>
                
                {/* New checkbox for with a known word */}
                <div className="checkbox-container">
                  <input 
                    type="checkbox" 
                    id="with-known-word" 
                    checked={withKnownWord}
                    onChange={(e) => {e.stopPropagation(); setWithKnownWord(e.target.checked)}}
                  />
                  <label id='key-title' htmlFor="with-known-word">With a Known Word</label>
                </div>
                
                {/* Input fields for known word and its hash */}
                {withKnownWord && (
                  <div className="known-word-container">
                    <input
                      type="text"
                      className="known-word-input"
                      placeholder="Enter known word"
                      value={knownWord}
                      onChange={(e) => {e.stopPropagation(); setKnownWord(e.target.value)}}
                    />
                    <input
                      type="text"
                      className="known-word-input"
                      placeholder="Enter known word hash"
                      value={knownWordHash}
                      onChange={(e) => {e.stopPropagation(); setKnownWordHash(e.target.value)}}
                    />
                  </div>
                )}
    
                {!isSubmitted && !loading && (
                  <button onClick={(e) => {e.stopPropagation(); handleSubmitHybrid()}}>
                    {t('attack-btn')}
                  </button>
                )}  
                {loading ? (
                  <div className="response-message4">
                    <Spinner animation="border" variant="success" size='sm' />
                  </div>
                ) : (
                  <div className="response-message4">
                    <p>{responseMessage4}</p>
                    {responseMessage4 && !loading && (
                      <VscDebugRestart 
                        style={{ fontSize: "20px", cursor: "pointer" }} 
                        onClick={(e) => {e.stopPropagation(); handleIconClick()}}
                      />
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Page1;
/*
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

export default CardApp;*/