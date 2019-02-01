import React, {Component} from 'react';
import PropTypes from 'prop-types';
import numeral from 'numeral';


class CurrencyCell extends Component {
  static propTypes = {
    ammount: PropTypes.number.isRequired,
  }
  render() {
    return (
      <td className="text-right">€{numeral(this.props.ammount).format('0,0')}</td>
    )
  }
}

export default CurrencyCell;
