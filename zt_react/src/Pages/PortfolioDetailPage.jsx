import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Route, Redirect } from 'react-router-dom';
import { Navbar, PortfolioDashboard, PageTitle } from '../_components';
import { portfolioActions } from '../_actions';


class PortfolioDetailPage extends Component {
  componentDidMount() {
    const { dispatch, match } = this.props;
    dispatch(portfolioActions.fetchDetail(match.params.code));
  }

  render() {
    const { portfolio, loading, dispatch, match } = this.props;

    if (loading === false && portfolio && !portfolio.code) {
      return <Redirect to="/portfolio" />;
    }

    if (loading === true || portfolio === undefined) {
      return <h1>Loading...</h1>;
    }

    if (portfolio.state === 'UPLOADED') {
      dispatch(portfolioActions.fetchLoans(match.params.code));
      return (
        <div>
          <Route path="/portfolio/i/:code([0-9a-z-]*)" exact component={PortfolioDashboard} />
        </div>
      );
    }
    return (
      <div className="container">
        <PageTitle title={portfolio.name} subtitle={portfolio.code} />
        <div className="alert alert-primary">
          We are in the proccess of analyzing your portfolio.
          We will let you know by email when this is done.
        </div>
      </div>
    );
  }
}

function mapStateToProps(state) {
  const { detailLoading, detailPortfolio } = state.portfolio;
  return {
    portfolio: detailPortfolio,
    loading: detailLoading,
  };
}

export default connect(mapStateToProps)(PortfolioDetailPage);
