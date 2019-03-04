import * as d3 from "d3";
import { isMoment } from 'moment';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import LoaderCard from './LoaderCard';
import LoanRow from './LoanRow';
import SortHeader from './SortHeader';


class LoanTable extends Component {
  state = {
    sortBy: 'id',
    sortDir: 'asc',
    page: 1,
    pageSize: 20,
  }

  onSortClicked(key) {
    const { sortBy, sortDir } = this.state;
    if (sortBy === key) {
      if (sortDir === 'asc') {
        this.setState({ sortDir: 'desc' });
      } else {
        this.setState({ sortDir: 'asc' });
      }
    } else {
      this.setState({ sortBy: key, sortDir: 'asc' });
    }
  }

  render() {
    let rows = [];
    const { loans, loading } = this.props;
    if (loading === true) {
      return <LoaderCard />;
    }
    const {
      sortBy, sortDir, page, pageSize,
    } = this.state;

    if (sortBy !== null) {
      loans.sort((a, b) => {
        const val1 = a[sortBy];
        const val2 = b[sortBy];
        if (isMoment(val1)) {
          if (val1 === null || val1 === undefined || (val1 instanceof Date && Number.isNaN(val1))) return -1;
          if (val2 === null || val2 === undefined || (val2 instanceof Date && Number.isNaN(val2))) return 1;
        } else {
          if (val1 === null || val1 === undefined) return 1;
          if (val2 === null || val2 === undefined) return -1;
        }
        if (val1 === val2) return 0;
        if (val1 > val2) return 1;
        if (val1 < val2) return -1;
        return 0;
      });
      if (sortDir === 'asc') {
        loans.reverse();
      }
    }

    const totalLoans = loans.length;
    const fromLoan = ((page - 1) * pageSize);
    const toLoan = d3.min([(page - 1) * pageSize + pageSize, totalLoans]);

    for (let i = fromLoan; i < toLoan; i++) {
      const loan = loans[i];
      rows.push(
        <LoanRow
          loan={loan}
          key={i}
        />
      );
    };

    const hasNext = toLoan < totalLoans;
    const hasPrev = fromLoan > 1;

    return (
      <div className="row row-cards row-deck">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Loans detail</h3>
            </div>
            <div className="table-responsive">
              <table className="table card-table table-vcenter text-nowrap">
                <thead>
                  <tr>
                    <SortHeader
                      name="NGR Code"
                      sortKey="ngr_code"
                      sortingBy={sortBy}
                      sortingDir={sortDir}
                      sortClicked={this.onSortClicked.bind(this)}/>
                    <SortHeader
                      name="Client Type"
                      sortKey="cli_type"
                      sortingBy={sortBy}
                      sortingDir={sortDir}
                      sortClicked={this.onSortClicked.bind(this)} />
                    <SortHeader
                      name="Init Date"
                      sortKey="init_date"
                      sortingBy={sortBy}
                      sortingDir={sortDir}
                      sortClicked={this.onSortClicked.bind(this)} />
                    <SortHeader
                      name="End Date"
                      sortKey="end_date"
                      sortingBy={sortBy}
                      sortingDir={sortDir}
                      sortClicked={this.onSortClicked.bind(this)} />
                    <SortHeader
                      name="Initial Balance"
                      sortKey="init_balance"
                      sortingBy={sortBy}
                      sortingDir={sortDir}
                      sortClicked={this.onSortClicked.bind(this)} />
                    <SortHeader
                      name="Default Interests"
                      sortKey="default_interest"
                      sortingBy={sortBy}
                      sortingDir={sortDir}
                      sortClicked={this.onSortClicked.bind(this)} />
                    <SortHeader
                      name="Net Balance"
                      sortKey="net_balance"
                      sortingBy={sortBy}
                      sortingDir={sortDir}
                      sortClicked={this.onSortClicked.bind(this)} />
                    <SortHeader
                      name="Real Guarantee"
                      sortKey="real_guarantee"
                      sortingBy={sortBy}
                      sortingDir={sortDir}
                      sortClicked={this.onSortClicked.bind(this)} />
                    <SortHeader
                      name="Personal Guarantee"
                      sortKey="personal_guarantee"
                      sortingBy={sortBy}
                      sortingDir={sortDir}
                      sortClicked={this.onSortClicked.bind(this)} />
                    <SortHeader
                      name="Other Guarantee"
                      sortKey="other_guarantee"
                      sortingBy={sortBy}
                      sortingDir={sortDir}
                      sortClicked={this.onSortClicked.bind(this)} />
                    <SortHeader
                      name="Forbearance"
                      sortKey="flag_forb"
                      sortingBy={sortBy}
                      sortingDir={sortDir}
                      sortClicked={this.onSortClicked.bind(this)} />
                  </tr>
                </thead>
                <tbody>
                  {rows}
                </tbody>
              </table>
            </div>
            <div className="card-footer text-center">
              <div className="row">
                <div className="col-4 text-left">
                  {hasPrev ? <a className="btn btn-secondary btn-sm" onClick={() => { this.setState({ page: this.state.page -1 }) }}><i className="fe fe-arrow-left"></i> Previews</a> : null}
                </div>
                <div className="col-4">
                  Displaying {fromLoan + 1} to {toLoan} of {totalLoans} loans.
                </div>
                <div className="col-4 text-right">
                  {hasNext ? <a className="btn btn-secondary btn-sm" onClick={()=>{this.setState({page: this.state.page + 1})}}>Next <i className="fe fe-arrow-right"></i></a> : null}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };
}


function mapStateToProps(state) {
  const { loans, loading } = state.loans;
  return {
    loans,
    loading,
  };
}

export default connect(mapStateToProps)(LoanTable);
