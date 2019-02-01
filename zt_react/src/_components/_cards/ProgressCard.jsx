import React from 'react';
import PropTypes from 'prop-types';
import numeral from 'numeral';


const ProgressCard = ({ name, value, percentage }) => (
  <div className="card">
    <div className="card-body text-center">
      <div className="h5">
        {name}
      </div>
      <div className="h1 mb-4">
        {value}
      </div>
      <div className="progress progress-sm">
        <div className="progress-bar bg-green" style={{ width: numeral(percentage).format('%0') }} />
      </div>
    </div>
  </div>
);


ProgressCard.propTypes = {
  name: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  percentage: PropTypes.number.isRequired,
};

export default ProgressCard;
