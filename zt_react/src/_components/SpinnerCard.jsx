import React from 'react';
import { RingLoader } from 'react-spinners';

const SpinnerStyle = {
  marginTop: 20,
  marginLeft: '-65px',
  paddingLeft: '50%',
  marginBottom: 50,
};


const SpinnerCard = () => (
  <div className="card">
    <div className="card-body">
      <div style={SpinnerStyle}>
        <RingLoader
          color="#467fcf"
          size={130}
          margin="30px"
        />
      </div>
      <h5 className="text-center">
        Upload in progress
      </h5>
      <p className="text-center">
        We are processing your request and should take no longer than a minute.
      </p>
    </div>
  </div>
);

export default SpinnerCard;
