import React from 'react';
import { Button } from './button'; // Make sure the file name and import name match, including case-sensitivity
import './HeroSection.css';
import '../App.css';

function HeroSection() {
  return (
    <div className='hero-container'>
      <video className='background-video' src='/videos/footballvid.mp4' autoPlay loop muted />
      <h1>FUTURE STAR PREDICTOR</h1>
      <p>CJ STROUD OR JAMARCUS RUSSELL?</p>
      <p>FIND THE NEXT STAR</p>
      <div className="hero-btns">
        <Button className='btns' buttonStyle='btn--outline' buttonSize='btn--large'>
          GET STARTED
        </Button>
        <Button className='btns' buttonStyle='btn--primary' buttonSize='btn--large'>
          WATCH TRAILER <i className='far fa-play-circle' />
        </Button>
      </div>
    </div>
  );
}

export default HeroSection;
