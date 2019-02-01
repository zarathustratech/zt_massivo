import React, {Component} from 'react';
import {connect} from 'react-redux';


class PortfolioDetailDashboardPage extends Component {
  render () {
    const {portfolio, loading, errors} = this.props;
    return (
      <h1>Porfolio #{portfolio ? portfolio.id: null}</h1>
    )
  }
}

function mapStateToProps(state) {
  const { detailLoading, detailPortfolio, detailErrors } = state.portfolio;
  return {
    portfolio: detailPortfolio,
    loading: detailLoading,
    errors: detailErrors,
  };
}

export default connect(mapStateToProps)(PortfolioDetailDashboardPage);
