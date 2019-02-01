import React from 'react';
import { PropTypes } from 'prop-types'
import moment from 'moment';

const DateCell = (props) => {
  const { date } = props;
  if (date.isValid()) {
    return (
      <td>
        <div className="small text-muted">{date.fromNow()}</div>
        <div>{date.format('MMM Do YYYY')}</div>
      </td>
    )
  }
  return <td>--</td>
};

export default DateCell;
