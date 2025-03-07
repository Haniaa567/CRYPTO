import React, { useState, useEffect } from 'react';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import { FaGlobe } from 'react-icons/fa';
import { useTranslation } from 'react-i18next';

function LanguageSelector() {
  const { i18n } = useTranslation();
   const { t } = useTranslation();
  const [language, setLanguage] = useState(i18n.language);  // Set default language

  // Check if there's a saved language preference in localStorage when the component mounts
  useEffect(() => {
    const savedLanguage = localStorage.getItem('language');
    if (savedLanguage) {
      i18n.changeLanguage(savedLanguage);
      setLanguage(savedLanguage);
    }
  }, [i18n]);

  const handleSelect = (selectedLanguage) => {
    setLanguage(selectedLanguage);
    i18n.changeLanguage(selectedLanguage.toLowerCase());  // Update the language
    localStorage.setItem('language', selectedLanguage.toLowerCase());  // Save selected language to localStorage
  };

  return (
    <DropdownButton
      variant="outline-light"
      id="dropdown-basic-button"
      title={
        <>
          <FaGlobe style={{ marginRight: '8px' }} /> {language}
        </>
      }
      onSelect={handleSelect}
    >
      <Dropdown.Item eventKey="en">{t("english")}</Dropdown.Item>
      <Dropdown.Item eventKey="fr">{t("french")}</Dropdown.Item>
    </DropdownButton>
  );
}

export default LanguageSelector;
