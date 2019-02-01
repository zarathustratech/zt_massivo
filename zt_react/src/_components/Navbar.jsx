import React, { Component } from 'react'
import { NavLink, Link } from 'react-router-dom';
import { connect } from 'react-redux';


class Navbar extends Component {
  render() {
    let {portfolio, loading, errors } = this.props;

    if(loading || portfolio === undefined || portfolio === null){
      return null;
    }

    return (
      <div className="header collapse d-lg-flex p-0" id="headerMenuCollapse">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg order-lg-first">
              <ul className="nav nav-tabs border-0 flex-column flex-lg-row">
                <li className="nav-item">
                  <NavLink to={`/portfolio/${portfolio.code}/`} className="nav-link" activeClassName="active"><i className="fe fe-home"></i> Dashboard</NavLink>
                </li>
                <li className="nav-item">
                  <NavLink to={`/portfolio/${portfolio.code}/map/`} className="nav-link" activeClassName="active"><i className="fe fe-map"></i> Map</NavLink>
                </li>
                <li className="nav-item">
                  <NavLink to={`/portfolio/${portfolio.code}/loans/`} className="nav-link" activeClassName="active"><i className="fe fe-dollar-sign"></i> Loans</NavLink>
                </li>
                <li className="nav-item">
                  <NavLink to={`/portfolio/${portfolio.code}/borrowers/`} className="nav-link" activeClassName="active"><i className="fe fe-users"></i> Borrowers</NavLink>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    );

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

const connectedNavbar = connect(mapStateToProps)(Navbar);
export { connectedNavbar as default };