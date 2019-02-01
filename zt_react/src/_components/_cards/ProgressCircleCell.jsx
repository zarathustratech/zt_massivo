import React, { Component } from 'react';
import CircularProgressbar from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import './ProgressCircleCell.css';

import numeral from 'numeral';


const ProgressCircleCell = (props) => {
  const { percentage } = props;
  if (percentage === undefined || percentage === null || Number.isNaN(percentage)) {
    return <td>--</td>;
  }
  const formattedPercentage = numeral(percentage).multiply(100).format('0');

  let color = '#cd201f';
  if (formattedPercentage > 40 && formattedPercentage <= 70) color = '#f1c40f';
  if (formattedPercentage > 70) color = '#5eba00';

  return (
    <td className="text-center">
      <CircularProgressbar
        percentage={formattedPercentage}
        styles={{ path: { stroke: color } }}
        text={`${formattedPercentage}%`}
      />
    </td>
  );
};

export default ProgressCircleCell;
