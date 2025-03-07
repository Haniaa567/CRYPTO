import React, { useState } from 'react';
import Navbar2 from '../components/Navbar/Navbar2';
import '../styles/Services.css';
import { useTranslation } from 'react-i18next';
import { t } from 'i18next';

function Timeprediction() {
  const [password, setPassword] = useState(""); // To store the entered password
  const [timeEstimation, setTimeEstimation] = useState(null); // To store the backend response
  const [error, setError] = useState(null); // To handle errors
  const [isPopupOpen, setIsPopupOpen] = useState(false); // To manage pop-up state
  const [isLoading, setIsLoading] = useState(false); // To track loading status
  const { t } = useTranslation();

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = async () => {
    setIsLoading(true); // Start loading
    try {
      const response = await fetch('http://127.0.0.1:8001/attaque/check-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password }),
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la connexion au serveur');
      }

      const data = await response.json();
      if (data.success) {
        setTimeEstimation(data.timeestimation);
        setError(null);
        setIsPopupOpen(true); // Open the pop-up
      } else {
        setError(t('time-pred-error'));
      }
    } catch (err) {
      setError(err.message);
      setTimeEstimation(null);
    } finally {
      setIsLoading(false); // End loading
    }
  };

  const handleClosePopup = () => {
    setIsPopupOpen(false); // Close the pop-up
  };

  return (
    <div id='timeprediction'>
      <div className="navbar-container">
        <Navbar2 />
      </div>

      <div className="test-container">
        <div className="test-container1">
          <h1>{t('time_prediction')}</h1>
          <p>{t("time-pred-text")}</p>
          <input
            type="text"
            placeholder={t('pw-placeholder')}
            value={password}
            onChange={handlePasswordChange}
          />
          <button onClick={handleSubmit} disabled={isLoading}>
            {t('start')}
          </button>


          {error && <p className="error-message">{error}</p>}
        </div>
      </div>

      {isLoading && (
        <div className="loading-message">
          <p>{t('loading-msg')}</p>
        </div>
      )}
      {isPopupOpen && timeEstimation && !isLoading &&(
        <Popup timeEstimation={timeEstimation} onClose={handleClosePopup} />
      )}
    </div>
  );
}

// Pop-up component
const Popup = ({ timeEstimation, onClose }) => {
  // Separate days, hours, minutes, and seconds
  const [days, hours, minutes, seconds] = parseTimeEstimation(timeEstimation);

  return (
    
    <div className="popup2">
      <div className="popup-content2">
        <h2>{t('time_estimation')}</h2>
        <div className="chronometer">
          <div className="time-box">
            <h3>{days}</h3>
            <p>{t('days')}</p>
          </div>
          <div className="time-box">
            <h3>{hours}</h3>
            <p>{t('hours')}</p>
          </div>
          <div className="time-box">
            <h3>{minutes}</h3>
            <p>{t('minutes')}</p>
          </div>
          <div className="time-box">
            <h3>{seconds}</h3>
            <p>{t('seconds')}</p>
          </div>
        </div>
        <button className="close-button" onClick={onClose}>
          {t('close')}
        </button>
      </div>
    </div>
  );
};

// Function to parse time estimation (separate into days, hours, minutes, and seconds)
const parseTimeEstimation = (timeString) => {
  const timeParts = timeString.match(/\d+/g); // Extract numbers
  const [days, hours, minutes, seconds] = timeParts.map((t) => parseInt(t, 10));
  return [days || 0, hours || 0, minutes || 0, seconds || 0];
};

export default Timeprediction;
