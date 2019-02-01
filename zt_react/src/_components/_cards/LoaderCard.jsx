import React from 'react';
import { RingLoader } from 'react-spinners';

const SpinnerStyle = {
  marginTop: 20,
  marginLeft: '-65px',
  paddingLeft: '50%',
  marginBottom: 50,
};


const LoaderCard = () => (
  <div className="card">
    <div className="card-body">
      <div style={SpinnerStyle}>
        <RingLoader
          color="#467fcf"
          size={130}
          margin="30px"
        />
      </div>
    </div>
  </div>
);

export default LoaderCard;
