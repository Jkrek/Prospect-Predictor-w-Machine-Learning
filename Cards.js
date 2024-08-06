import React from 'react';
import './Cards.css';
import CardItem from './CardItem';

// Correct image paths relative to src/components
import bondImg from '../images/Bond.png';
import hunterImg from '../images/Hunter.jpg';
import jamesPearceImg from '../images/james-pearce.jpg';
import img4 from '../images/eugene-wilson.jpg';
import img8 from '../images/kirby.jpg';

function Cards() {
  return (
    <div className='cards'>
      <h1>Check out how it works!</h1>
      <div className='cards__container'>
        <div className='cards__wrapper'>
          <ul className='cards__items'>
            <CardItem
              src={bondImg}
              text='Explore the hidden waterfall deep inside the Amazon Jungle'
              label='Offense'
              path='/services'
            />
            <CardItem
              src={hunterImg}
              text='Travel through the Islands of Bali in a Private Cruise'
              label='Flex'
              path='/services'
            />
          </ul>
          <ul className='cards__items'>
            <CardItem
              src={jamesPearceImg}
              text='Set Sail in the Atlantic Ocean visiting Uncharted Waters'
              label='Defense'
              path='/services'
            />
            <CardItem
              src={img4}
              text='Experience Football on Top of the Himilayan Mountains'
              label='Quarterback'
              path='/products'
            />
            <CardItem
              src={img8}
              text='Ride through the Sahara Desert on a guided camel tour'
              label='Coach'
              path='/sign-up'
            />
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Cards;
