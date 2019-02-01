import React from 'react';
import { PropTypes } from 'prop-types';
import { Marker } from 'react-map-gl';
import './CircleMarker.css';


const CircleMarker = (props) => {
  const {
    longitude, latitude, radius, color, onClick,
  } = props;

  return (
    <Marker
      longitude={longitude}
      latitude={latitude}
    >
      <svg
        height={radius * 2}
        width={radius * 2}
        className="circle-marker"
      >
        <circle
          cx={radius}
          cy={radius}
          r={radius}
          fill={color}
          onClick={onClick}
        />
      </svg>
    </Marker>
  );
};

CircleMarker.propTypes = {
  longitude: PropTypes.number.isRequired,
  latitude: PropTypes.number.isRequired,
  radius: PropTypes.number,
  color: PropTypes.string,
  onClick: PropTypes.func,
};

CircleMarker.defaultProps = {
  radius: 2,
  color: 'red',
  onClick: () => {},
};

export default CircleMarker;
