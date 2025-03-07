import React from 'react'
import './Navbar.css'
import Logo from '../../assets/logo.png';
import Button from 'react-bootstrap/Button';
import { Dropdown, DropdownButton } from 'react-bootstrap';
import Languageselect from '../LanguageSelector';
import { TbSquareArrowRightFilled } from 'react-icons/tb';
import { FaAngleDown } from 'react-icons/fa';
import { Link } from 'react-router';
import { useKeycloak } from '@react-keycloak/web';
import { useCallback } from 'react';
import Userprofile from '../Userprofile';
import { useTranslation } from 'react-i18next';

const Navbar = () => {
  const { keycloak, initialized } = useKeycloak();
  const { t } = useTranslation();


  const login = useCallback(() => {
    keycloak.login({
      redirectUri: 'http://localhost:3000/#/F',
      responseMode: 'query',
      prompt: 'login'
    });
  }, [keycloak]);

  const logout = useCallback(() => {
    keycloak.logout({
      redirectUri: window.location.origin
    });
  }, [keycloak]);

 

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      window.scrollTo({
        top: element.offsetTop,
        behavior: 'smooth',
      });
    }
  };
  return (
    <div className="header">
      <Link className="Logo" to='/#home' onClick={() => scrollToSection('home')}><img src={Logo} alt="" /></Link>

      <nav className="custom-navbar">
        <Link className="links" to='/#home' onClick={() => scrollToSection('home')}>{t('home')}</Link>

        <div className="services-dropdown">
          <Link to='/#services' onClick={() => scrollToSection('services')} className="services-link">
            {t("services")} <FaAngleDown className="dropdown-arrow" />
          </Link>
          <div className="dropdown-menu">
            <Link to="/EncryptDecrypt">{t("encryption/decryption")}</Link>
            <Link to="/Attacks">{t("attack_simulation")}</Link>
            <a href="/Passwordtesting">{t("password_testing")}</a>
            <a href="/Timeprediction">{t("time_prediction")}</a>
          </div>
        </div>
        <Link className="links" to='/#about' onClick={() => scrollToSection('about')} >{t("about")}</Link>
        <Link className="links" to='/#contact' onClick={() => scrollToSection('contact')} >{t("contact")}</Link>
        <Link className="links" to='/#faq' onClick={() => scrollToSection('faq')} >{t("faq")}</Link>
      </nav>

      <div className='buttons'>
        <Languageselect />
        {keycloak.authenticated ? ( //here conditional rendering of component,if hes logged in we show logout button else login button
          <Button
            className="enlarge"
            variant="light"
            onClick={logout}
          >
            {t('logout')} 
          </Button>
        ) : (
          <Button
            className="enlarge"
            variant="light"
            onClick={login}
          >
            {t('Start now')} <TbSquareArrowRightFilled style={{ marginLeft: '8px', color: '#0CB074' }} />
          </Button>
        )}
        {keycloak.authenticated && <Userprofile />}

      </div>

    </div>
  )
}

export default Navbar