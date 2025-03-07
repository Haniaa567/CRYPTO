import React from 'react'
import '../styles/Sections.css'
import { useTranslation } from 'react-i18next';

function Footer() {
  const { t } = useTranslation();
  
  return (
    
    <div className='footer'>
        <p>&copy; {t("footer_text")}</p>
    </div>
  )
}

export default Footer