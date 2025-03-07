import React from 'react'
import Background from '../components/Background';
import '../styles/Sections.css'
import Hero from '../components/Hero';

function Section1() {
  return (
    <div className='section-1'>
       <div className='bg'>
        <Background />
      </div>
       <div className='main-text'>
        <Hero/>
        
       </div>
       <div class="hscroll-line"></div>
       <div class="hscroll-line1"></div>
       <div class="hscroll-line2"></div>
    </div>
  )
}

export default Section1