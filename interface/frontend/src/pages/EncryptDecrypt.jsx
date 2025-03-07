import React, { useState } from 'react';
import Navbar2 from '../components/Navbar/Navbar2';
import '../styles/Services.css';
import { useKeycloak } from '@react-keycloak/web';
import { useTranslation } from 'react-i18next';

function EncryptDecrypt() {
  const { keycloak } = useKeycloak();
  const [encryptionMessage, setEncryptionMessage] = useState('');
  const [decryptionMessage, setDecryptionMessage] = useState('');
  const [encryptionKey, setEncryptionKey] = useState('');
  const [decryptionKey, setDecryptionKey] = useState('');
  const [encryptionResult, setEncryptionResult] = useState('');
  const [decryptionResult, setDecryptionResult] = useState('');
  const [algorithm, setAlgorithm] = useState('AES');
  const { t } = useTranslation();

  const getUserId = () => {
    return keycloak.tokenParsed?.sub || '';
  };
  // Fonction pour générer une clé
  const generateKey = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8001/encrypt/generate-key/${algorithm}`);
      if (response.ok) {
        const data = await response.text();
        // Retirer uniquement les guillemets au début et à la fin
        const sanitizedKey = data.replace(/^"|"$/g, '');
        setEncryptionKey(sanitizedKey); // Remplir le champ clé avec la clé générée
      } else {
        console.error('Erreur lors de la génération de la clé');
      }
    } catch (error) {
      console.error('Erreur réseau:', error);
    }
  };
  

  // Fonction pour chiffrer un message
  const encryptMessage = async () => {
    // Vérifier d'abord l'authentification
    if (!keycloak.authenticated) {
      console.log("User not authenticated");
      keycloak.login(); // Rediriger vers la page de login si non authentifié
      return;
    }
    try {

      const body = {
        message: encryptionMessage,
        key: encryptionKey,
        enregistrement: true, // Par défaut, remplacez si nécessaire
        iduser: getUserId(), // Remplacez par un ID utilisateur réel
      };
      
      console.log('Données envoyées pour le chiffrement:', body);
      const response = await fetch(`http://127.0.0.1:8001/encrypt/encrypt/${algorithm}`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json' ,
          'Authorization': `Bearer ${keycloak.token}` // Ajouter le token ici aussi si nécessaire

        },
        body: JSON.stringify(body),
      });

      if (response.ok) {
        const data = await response.json();
        const sanitizedResult = data.encrypted_message.replace(/^"|"$/g, '');
        setEncryptionResult(sanitizedResult); // Afficher le résultat chiffré
      } else {
        const errorText = await response.text();
        console.error('Response error:', errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

    } catch (error) {
      console.error('Error:', error);
    } 
  };

  // Fonction pour déchiffrer un message
  const decryptMessage = async () => {
    // Vérifier d'abord l'authentification
    if (!keycloak.authenticated) {
      console.log("User not authenticated");
      keycloak.login(); // Rediriger vers la page de login si non authentifié
      return;
    }
  
    try {

      const body = {
        encrypted_message: decryptionMessage,
        key: decryptionKey,
        enregistrement: true, // Par défaut, remplacez si nécessaire
        iduser:getUserId(), // Remplacez par un ID utilisateur réel
      };

      const response = await fetch(`http://127.0.0.1:8001/encrypt/decrypt/${algorithm}`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${keycloak.token}` // Ajouter le token ici aussi si nécessaire

         },
        body: JSON.stringify(body),
      });

      if (response.ok) {
        const data = await response.json(); 
        const sanitizedResult = data.encrypted_message.replace(/^"|"$/g, '');
        setDecryptionResult(sanitizedResult); // Afficher le résultat déchiffré
      } else {
        const errorText = await response.text();
        console.error('Response error:', errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }
      
    } catch (error) {
      console.error('Error:', error);
    } 
  };

  return (
    <div id='encryptdecrypt'>
      <div className="navbar-container">
        <Navbar2 />
      </div>

      <div className='container'>
        {/* Encryption Section */}
        <div className='encrypt'>
          <h1>{t('encryption')}</h1>
          <textarea
            className="entry"
            rows={5}
            placeholder={t('placeholder-encrypt-input')}
            value={encryptionMessage}
            onChange={(e) => setEncryptionMessage(e.target.value)}
          ></textarea>
          <select
            className="select"
            value={algorithm}
            onChange={(e) => setAlgorithm(e.target.value)}
          >
            <option value="AES">AES</option>
            <option value="3DES">3DES</option>
            <option value="RC4">RC4</option>
            <option value="RSA">RSA</option>
            <option value="Chacha20">Chacha20</option>
          </select>
          <div className='key-container'>
            <input
              type="text"
              className='key'
              placeholder={t('placeholder-key-encrypt')}
              value={encryptionKey}
              onChange={(e) => setEncryptionKey(e.target.value)}
            />
            <button className='gen-key-btn' onClick={generateKey}>{t('generate-key')}</button>
          </div>
          <textarea
            className="output"
            rows={5}
            placeholder={t('placeholder-encrypt-output')}
            value={encryptionResult}
            disabled
          ></textarea>
          <button className='sub-btn' onClick={encryptMessage}>{t('encrypt')}</button>
        </div>

        {/* Decryption Section */}
        <div className='decrypt'>
          <h1>{t('decryption')}</h1>
          <textarea
            className="entry"
            rows={5}
            placeholder={t('placeholder-decrypt-input')}
            value={decryptionMessage}
            onChange={(e) => setDecryptionMessage(e.target.value)}
          ></textarea>
          <select
            className="select"
            value={algorithm}
            onChange={(e) => setAlgorithm(e.target.value)}
          >
            <option value="AES">AES</option>
            <option value="3DES">3DES</option>
            <option value="RC4">RC4</option>
            <option value="RSA">RSA</option>
            <option value="Chacha20">Chacha20</option>
          </select>
          <input
            type="text"
            className='key'
            placeholder={t('placeholder-key-decrypt')}
            value={decryptionKey}
            onChange={(e) => setDecryptionKey(e.target.value)}
          />
          <textarea
            className="output"
            rows={5}
            placeholder={t('placeholder-decrypt-output')}
            value={decryptionResult}
            disabled
          ></textarea>
          <button className='sub-btn' onClick={decryptMessage}>{t('decrypt')}</button>
        </div>
      </div>
    </div>
  );
}

export default EncryptDecrypt;
