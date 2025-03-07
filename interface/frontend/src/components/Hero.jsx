import React from 'react'
import '../styles/Sections.css';
import Icon1 from '../assets/icon1.svg';
import Icon2 from '../assets/icon2.svg';
import Icon3 from '../assets/icon3.svg';
import Icon4 from '../assets/icon4.svg';
import Icon5 from '../assets/icon5.svg';
import { useTranslation } from 'react-i18next';

function Hero() {
  const { t } = useTranslation();
  return (
    <div>
        <div className='slogan'>
            <h1 id='main-slogan'>{t('main-slogan')}</h1>
            <h1 id='slogan-shiny'>{t('slogan-shiny')}</h1>

        </div>
        <div className='serv'>
            <label className='serv-icons'><img src={Icon5}  />{t('encrypt')}   </label>
            <label className='serv-icons'><img src={Icon4}  />{t('decrypt')}</label>
            <label className='serv-icons'><img src={Icon3}  />{t('attack_simulation')}</label>
            <label className='serv-icons'><img src={Icon2}  />{t("password_testing")}</label>
            <label className='serv-icons'> <img src={Icon1}  />{t("time_prediction")}</label>
        </div>
        
    </div>
  )
}

export default Hero