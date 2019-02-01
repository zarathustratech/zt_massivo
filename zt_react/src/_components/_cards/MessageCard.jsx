import PropTypes from 'prop-types';
import React from 'react';


const MessageCard = ({ row1, row2, row3 }) => (
  <div className="card">
    <div className="card-body p-3 text-center">
      <div className="text-muted">
        {row1}
      </div>
      <div className="h1 m-0">
        {row2}
      </div>
      <div className="text-muted">
        {row3}
      </div>
    </div>
  </div>
);

MessageCard.propTypes = {
  row1: PropTypes.string.isRequired,
  row2: PropTypes.string.isRequired,
  row3: PropTypes.string.isRequired,
};

export default MessageCard;
