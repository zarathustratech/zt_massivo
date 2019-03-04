import moment from 'moment';
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { Link, Redirect } from 'react-router-dom';
import { Loader, PageTitle } from '../_components';
import { portfolioService } from '../_services';


const PortfolioShape = PropTypes.shape({
  state: PropTypes.string.isRequired,
  code: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
});


const PortfolioState = ({ state }) => {
      return (
        <div className="tag tag-green">
          Ready
          <span className="tag-addon">
            <i className="fe fe-check" />
          </span>
        </div>
      );
  }

const PortfolioRow = ({ portfolio }) => {
  const createdAt = moment(portfolio.created_at).format('MMMM Do YYYY');
  return (
    <tr>
      <td>
        { portfolio.name
          ? portfolio.name
          : (
            <span>
              No name set
            </span>
          )}
      </td>
      <td>
        <PortfolioState state={portfolio.state} />
      </td>
      <td>
        { portfolio.n_loans
          ? portfolio.n_loans.toLocaleString()
          : '--'}
      </td>
      <td>
        { createdAt }
      </td>
      <td>
        <Link to={`/portfolio/i/${portfolio.code}`}>
          <i className="fe fe-lock" />
          { portfolio.code }
        </Link>
      </td>
    </tr>
  );
};

PortfolioRow.propType = {
  portfolio: PortfolioShape,
};


const PortfolioTable = ({ portfolios }) => {
  const portfolioRows = portfolios.map(portfolio => (
    <PortfolioRow
      portfolio={portfolio}
      key={portfolio.code}
    />
  ));
  return (
    <div className="card">
      <div className="table-responsive">
        <table className="table table-hover table-outline table-vcenter text-nowrap card-table">
          <thead>
            <tr>
              <th>
                Name
              </th>
              <th>
                Status
              </th>
              <th>
                N Loans
              </th>
              <th>
                Created at
              </th>
              <th>
                Secure link
              </th>
            </tr>
          </thead>
          <tbody>
            {portfolioRows}
          </tbody>
        </table>
      </div>
    </div>
  );
};

PortfolioTable.propType = {
  portfolios: PropTypes.arrayOf(PortfolioShape),
};


class PortfolioListPage extends Component {
  state = {
    isLoading: true,
    portfolios: [],
  }

  componentDidMount() {
    portfolioService.list().then((response) => {
      this.setState({
        portfolios: response.data.results,
        isLoading: false,
      });
    });
  }

  render() {
    const { isLoading, portfolios } = this.state;
    const btn = (
      <Link
        to="/portfolio/upload"
        className="btn btn-success btn-sm"
        style={{ float: 'right', marginTop: 8 }}
      >
        <i className="fe fe-plus" />
        Add new
      </Link>
    );

    return (
      <div>
        {isLoading
          ? <Loader />
          : (
            <div className="container">
              {portfolios.length === 0
                ? <Redirect to="/portfolio/upload" />
                : (
                  <div>
                    <PageTitle title="Portfolios" btn={btn} />
                    <PortfolioTable portfolios={portfolios} />
                  </div>
                )}
            </div>
          )}
      </div>
    );
  }
}

export default PortfolioListPage;
