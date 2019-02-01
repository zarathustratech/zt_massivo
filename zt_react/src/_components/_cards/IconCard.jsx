import React from 'react';
import PropTypes from 'prop-types';


const IconCard = ({ iconClass, bgColor, text, mutedText }) => (
  <div className="card p-3">
    <div className="d-flex align-items-center">
      <span className={`stamp stamp-md mr-3 bg-${bgColor}`}>
        <i className={iconClass} />
      </span>
      <div>
        <h4 className="m-0">
          {text}
        </h4>
        <small className="text-muted">
          {mutedText}
        </small>
      </div>
    </div>
  </div>
);


IconCard.propTypes = {
  iconClass: PropTypes.string.isRequired,
  bgColor: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
  mutedText: PropTypes.string.isRequired,
};

export default IconCard;
