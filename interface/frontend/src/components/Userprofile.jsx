import React, { useState, useEffect } from 'react';
import { FaUserCircle } from 'react-icons/fa';
import { Offcanvas } from 'react-bootstrap';
import { useKeycloak } from '@react-keycloak/web';
import '../styles/Userprofile.css';
import { useTranslation } from 'react-i18next';

const Userprofile = () => {
  const [show, setShow] = useState(false);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
   const { t } = useTranslation();
  
  const { keycloak } = useKeycloak();
  const userInfo = keycloak.tokenParsed;

  const fetchHistory = async () => {
    try {
      if (!userInfo || !userInfo.sub) {
        throw new Error('User ID not available');
      }

      setLoading(true);
      setError(null);
      
      const response = await fetch(`http://localhost:8001/features/gethistorique/${userInfo.sub}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${keycloak.token}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch history');
      }
      
      const data = await response.json();
      setHistory(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (keycloak.authenticated && userInfo) {
      fetchHistory();
    }
  }, [keycloak.authenticated, userInfo]);

  const handleClose = () => {
    setShow(false);
    document.body.classList.remove('no-scroll');
  };

  const handleShow = () => {
    setShow(true);
    document.body.classList.add('no-scroll');
  };

  return (
    <div className="user-menu">
      <FaUserCircle
        size={30}
        onClick={handleShow}
        style={{ cursor: 'pointer', marginLeft: '15px', color: '#0CB074' }}
      />
      
      <Offcanvas show={show} onHide={handleClose} placement="end" className="offcanvas-main" scroll={true}>
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>{t('profil')}</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
          <div className="container-menu-profile">
            <div className="user-profile">
              <h4>{t('user-info')}</h4>
              <p><strong>{t('email')}:</strong> {userInfo.email}</p>
              <p><strong>{t('firstname')}:</strong> {userInfo.given_name}</p>
              <p><strong>{t('lastname')}:</strong> {userInfo.family_name}</p>
              <p><strong>{t('username')}:</strong> {userInfo.preferred_username}</p>
            </div>
            <div className="history">
              <h4>{t('history')}</h4>
              {loading && <p>{t('loading')}</p>}
              {error && <p className="error">{t('error')} {error}</p>}
              <div className="history-titles">
                {history.map((item, index) => (
                  <div className="hist1" key={item.id}>
                    <div className="main-hist-content">
                      <div className="icon-line">
                        <div className="line"></div>
                        <div className="service-icon">
                          {item.type === 'encrypt' ? '🔒' : '🔍'}
                        </div>
                      </div>
                      <div className="history-content">
                        <p>{t("password")}:</p>
                        <p>{item.entree}</p>
                        <p>{t('resultt')}:</p>
                        <p>{item.sortie}</p>
                        <p>{t('service-name')}:</p>
                        <p>{item.nom}</p>
                        <p>{t('datetime')}:</p>
                        <p>{new Date(item.date_creation).toLocaleString()}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Offcanvas.Body>
      </Offcanvas>
    </div>
  );
};

export default Userprofile;










/*
import React, { useState } from 'react';
import { FaUserCircle } from 'react-icons/fa'; // User icon
import { Offcanvas } from 'react-bootstrap'; // Import Offcanvas from React Bootstrap
import { useKeycloak } from '@react-keycloak/web';
import '../styles/Userprofile.css';

const Userprofile = () => {
  const [show, setShow] = useState(false);
  const { keycloak } = useKeycloak();
  const userInfo = keycloak.tokenParsed;

  const handleClose = () => {
    setShow(false);
    document.body.classList.remove('no-scroll');
  };

  const handleShow = () => {
    setShow(true);
    document.body.classList.add('no-scroll');
  };

  return (
    <div className="user-menu">
      { User Icon }
      <FaUserCircle 
        size={30} 
        onClick={handleShow} 
        style={{ cursor: 'pointer', marginLeft: '15px', color: '#0CB074' }} 
      />

      {Offcanvas }
      <Offcanvas show={show} onHide={handleClose} placement="end" className="offcanvas-main" scroll={true}>
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>My profile</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
            <div className="container-menu-profile">
          <div className="user-profile">
              <h4>User Information</h4>
              <p><strong>Email:</strong> {userInfo.email}</p>
              <p><strong>First Name:</strong> {userInfo.given_name}</p>
              <p><strong>Last Name:</strong> {userInfo.family_name}</p>
              <p><strong>Username:</strong> {userInfo.preferred_username}</p>
          </div>
          <div className="history">
            <h4>History</h4>
            <div className="history-titles">
                <div class="hist1">
               
                <div class="main-hist-content">
                    <div className="icon-line"> 
                        <div class="line"></div>
                        <div class="service-icon">
                    logo 
                    </div>
                    </div>
                    
                <div class="history-content">
                   <p>password </p>
                   <p>result </p>  
                   <p>service-name</p>
                   <p>time</p>
                    </div>
                    </div>
                     
                    </div>
                
            </div>
          
          </div>
          </div>
        </Offcanvas.Body>
      </Offcanvas>
    </div>
  );
};

export default Userprofile;*/
