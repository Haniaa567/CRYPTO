import React from 'react'
import '../styles/Sections.css'
import Globe from '../components/three.js'
import { useTranslation } from 'react-i18next';
function Section3() {
  const { t } = useTranslation();
  return (
    <div className='section-3'>
      <div className='globe'>
      <Globe/>
      </div>

       <div className='intro-text'>
        <h1>{t('intro-text')}</h1>
        <div className='parag-text'>
          <p>
          {t('parag-text')}
          </p>
        </div>
       </div>
       
    </div>
  )
}

export default Section3