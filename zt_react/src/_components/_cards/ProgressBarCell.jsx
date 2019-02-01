import React, {Component} from 'react';
import { PropTypes } from 'prop-types'
import numeral from 'numeral';
import moment from 'moment';


class ProgressBarCell extends Component {
	render () {
		var progressValue = this.props.total > 0 ?
			this.props.progress / this.props.total : 0;

		var percentage = numeral(progressValue).multiply(100);
		var formatedPercentage = numeral(progressValue).format('0%');

		var barClass = 'progress-bar bg-green';
		var diffDays = (new Date() - this.props.last_payment) / (1000 * 3600 * 24);
		if (diffDays > 60) barClass = 'progress-bar bg-yellow';
		if (diffDays > 200 ) barClass = 'progress-bar bg-red';

		const { last_payment } = this.props;
		return (
			<td>
				<div className="clearfix">
					<div className="float-left">
						<strong>{formatedPercentage}</strong>
					</div>
					<div className="float-right">
						<small className="text-muted">Last pay: {last_payment.format('MMM Do YYYY')}</small>
					</div>
				</div>
				<div className="progress progress-xs">
					<div className={barClass} role="progressbar" style={{ width: formatedPercentage }} aria-valuenow={percentage} aria-valuemin="0" aria-valuemax="100"></div>
				</div>
			</td>
		)
	}
}

export default ProgressBarCell;
