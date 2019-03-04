import React, { Component } from 'react';
import { connect } from 'react-redux';
import PageTitle from './PageTitle';
import {
  LoansTableCard,
} from './_cards';


class PortfolioDashboard extends Component {
  constructor(props) {
    super(props);
    this.onMarkerClicked = this.onMarkerClicked.bind(this);
    this.onBoundsChange = this.onBoundsChange.bind(this);
  }

  state = {
    filterBounds: {},
  }

  onMarkerClicked(loan) {
    // console.log(this, loan);
  }

  onBoundsChange(bounds) {
    // console.log(this, bounds);
    this.setState({ filterBounds: bounds });
    const { loans } = this.props;
  }

  render() {
    const { portfolio } = this.props;
    if (portfolio === undefined || portfolio === null || portfolio === {}) {
      return (
        <div className="my-3 my-md-5">
          <div className="container">
            <h1>
              Loading data ...
            </h1>
          </div>
        </div>
      );
    }

    return (
      <div className="container">
        <PageTitle title={portfolio.name} subtitle={portfolio.code} />
        <div className="row row-cards">
          <div className="col-12">
            <LoansTableCard />
          </div>
        </div>
      </div>
    );
  }
}

function mapStateToProps(state) {
  const { detailPortfolio, detailLoading } = state.portfolio;
  return {
    portfolio: detailPortfolio,
    loading: detailLoading,
  };
}

export default connect(mapStateToProps)(PortfolioDashboard);
