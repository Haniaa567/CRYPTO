import React from 'react'
import '../styles/Sections.css'
import { IoLogoGithub } from "react-icons/io";
import { ImMail4 } from "react-icons/im";
import { FaLinkedin } from "react-icons/fa";
import { useTranslation } from 'react-i18next';

function Section6() {
  const { t } = useTranslation();
  return (
    <div className='section-6'>
       <h1 id='sec6-title'>{t('contact')}</h1>
       <div className='icons'>
              <a className="socials-icons" href=""><IoLogoGithub/></a>
              <a className="socials-icons" href="" ><FaLinkedin/></a>
              <a className="socials-icons" href=""><ImMail4/></a>
       </div>
    </div>
  )
}

export default Section6