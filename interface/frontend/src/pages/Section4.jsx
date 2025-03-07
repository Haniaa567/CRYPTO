import React from 'react'
import '../styles/Sections.css'
import Icon6 from '../assets/icon6.svg';
import Icon7 from '../assets/icon7.svg';
import Icon8 from '../assets/icon8.svg';
import Icon9 from '../assets/icon9.svg';
import { useTranslation } from 'react-i18next';

function Section4() {
  const { t } = useTranslation();
  return (
    <div className='section-4'>
       <h1 id='sec4-title'>{t("sec4-title")}</h1>
       <div className='services'>
         <div className='service'>
            <img src={Icon8}  className='img-serv' />
          <h1>{t('password_testing')} </h1>
          <p>{t('description1')}</p>
       </div>
       <div className='service'>
          <img src={Icon6}  className='img-center' />
          <h1>{t('attack_simulation')}</h1>
          <p> {t('description2')}</p>
       </div>
       <div className='service'>
       <img  className='img-serv' src={Icon9}  />
        <h1>{t('Encryption and Decryption')}</h1>
        <p>{t('description3')}</p>
       </div>
       <div className='service'>
       <img src={Icon7} className='img-center'  />
      
        <h1>{t('time_estimation')}</h1>
        <p>{t('description4')}</p>
       
        
       </div>
       </div>
      
    </div>
  )
}

export default Section4