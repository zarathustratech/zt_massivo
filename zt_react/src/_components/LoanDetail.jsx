import React, { Component } from 'react';
import numeral from 'numeral';
import moment from 'moment';

class LoanDetail extends Component {

  render() {
    if(this.props.loan === null)
      return null;
    var loan = this.props.loan;
    return (
      <div>
        <h3>Loan detail</h3>
        <h4>Basic information</h4>
        <table className="table table-stripped">
          <tbody>
            <tr><th>Id</th><td>{loan.loan_id}</td></tr>
            <tr><th>Company</th><td>{loan.company_name}</td></tr>
            <tr><th>Is active?</th><td>{loan.active ? <div><i class="fe fe-check-circle text-green"></i> Yes</div>: <div><i class="fe fe-x-circle text-red"></i> No</div>}</td></tr>
            <tr><th>Borrowed</th><td>€{numeral(loan.gross_book_value).format('0,0')}</td></tr>
            <tr><th>Payed</th><td>€{numeral(loan.payments_total).format('0,0')}</td></tr>
            <tr><th>Last payment</th><td>{moment(loan.last_payment).format('MMM Do YYYY')}</td></tr>
            <tr><th>Financial Event</th><td>{moment(loan.financial_event).format('MMM Do YYYY')}</td></tr>
            <tr><th>Legal Event</th><td>{moment(loan.legal_event).format('MMM Do YYYY')}</td></tr>
          </tbody>
        </table>
        <h4>Predictions</h4>
        <table className="table table-stripped">
          <tbody>
            <tr><th>Recovery 6 months</th><td>{numeral(loan.neuralnetwork_output_rs_6m).format('%0')}</td></tr>
            <tr><th>Recovery 12 months</th><td>{numeral(loan.neuralnetwork_output_rs_12m).format('%0')}</td></tr>
            <tr><th>Recovery 18 months</th><td>{numeral(loan.neuralnetwork_output_rs_18m).format('%0')}</td></tr>
          </tbody>
        </table>
      </div>
    )
  }
}

export default LoanDetail;
