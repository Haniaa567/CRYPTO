import React, { useState } from 'react';
import Navbar2 from '../components/Navbar/Navbar2';
import '../styles/Services.css';
import { useTranslation } from 'react-i18next';

function Passwordtesting() {
  const [password, setPassword] = useState(''); // État pour le mot de passe
  const [popupContent, setPopupContent] = useState(''); // Contenu de la popup
  const [showPopup, setShowPopup] = useState(false); // État pour afficher/masquer la popup
  const [isLoading, setIsLoading] = useState(false); // État pour le chargement
  const { t } = useTranslation();

  // Fonction pour tester le mot de passe
  const handleTestPassword = async () => {
    setIsLoading(true); // Démarre le chargement
    setPopupContent(''); // Réinitialise le contenu précédent
    try {
      const response = await fetch('http://127.0.0.1:8001/attaque/check-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password }),
      });

      if (!response.ok) {
        throw new Error('Error during the request to the backend');
      }

      const data = await response.json();
      setPopupContent(`${data.message} `); // Met à jour le contenu de la popup
    } catch (error) {
      console.error('Erreur:', error);
      setPopupContent(t('pw-test-error')); // Met à jour le contenu de la popup
    } finally {
      setIsLoading(false); // Arrête le chargement
      setShowPopup(true); // Affiche la popup
    }
  };

  // Fonction pour fermer la popup
  const handleClosePopup = () => {
    setShowPopup(false);
  };

  return (
    <div id="passwordtesting">
      <div className={`main-content ${showPopup || isLoading ? 'blur' : ''}`}>
        <div className="navbar-container">
          <Navbar2 />
        </div>
        <div className="container-2">
          <div className="container-3">
            <h1>{t('password_testing')}</h1>
            <p>
              {t('pw-test-text')}
            </p>
            <input
              type="text"
              placeholder={t('pw-placeholder')}
              value={password}
              onChange={(e) => setPassword(e.target.value)} // Met à jour l'état avec la valeur saisie
            />
            <button onClick={handleTestPassword} disabled={isLoading}>
              {isLoading ? 'Testing...' : 'Test password'}
            </button>
          </div>
        </div>
      </div>

      {/* Message de traitement */}
      {isLoading && (
        <div className="loading-message">
          <p>{t('loading-msg')}</p>
        </div>
      )}

      {/* Popup Window */}
      {showPopup && !isLoading && (
        <>
          <div className="overlay"></div>
          <div className="popup">
            <div className="popup-content">
              <h2>{t('result')}</h2>
              <p>{popupContent}</p>
              <button onClick={handleClosePopup}>{t('close')}</button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default Passwordtesting;

