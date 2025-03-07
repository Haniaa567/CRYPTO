import React, { useState } from 'react';
import { BsFillPlusSquareFill, BsFillDashSquareFill } from "react-icons/bs"; 
import '../styles/Sections.css';
import { useTranslation } from 'react-i18next';

function Section5() {
  const [activeIndex, setActiveIndex] = useState(null);
  const { t } = useTranslation();

  const questions = [
    { question: t("q1"), answer: t("a1") },
    { question: t("q2"), answer: t("a2") },
    { question: t("q3"), answer: t("a3") }
  ];

  const handleToggle = (index) => {
    if (index === activeIndex) {
      setActiveIndex(null); // Close the active item if clicked again
    } else {
      setActiveIndex(index); // Open the clicked item
    }
  };

  return (
    <div className="section-5">
      <h1 id='sec5-title'>{t('sec5-title')}</h1>
      <div className="accordion">
        {questions.map((item, index) => (
          <div key={index} className="accordion-item">
            <div className="accordion-header" onClick={() => handleToggle(index)}>
              <h3>{item.question}</h3>
              <span className="accordion-icon">{activeIndex === index ? <BsFillDashSquareFill /> : <BsFillPlusSquareFill />}</span>
            </div>
            {activeIndex === index && (
              <div className="accordion-content">
                <p>{item.answer}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Section5;
