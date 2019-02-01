import React, {Component} from 'react';
import PropTypes from 'prop-types';
import ProgressCircleCell from './ProgressCircleCell.jsx';
import CurrencyCell from './CurrencyCell';
import * as d3 from 'd3';


class RegionsTable extends Component {
  static propTypes = {
    loans: PropTypes.array.isRequired,
    onRegionSelecionChange: PropTypes.func,
  }

  state = {
    selectedRegions: new Set(),
  }

  constructor(props){
    super(props);
    this.onRegionChange = this.onRegionChange.bind(this);
    this.resetRegionSelection = this.resetRegionSelection.bind(this);
  }
  
  onRegionChange(region){
    let selectedRegions = new Set(this.state.selectedRegions);
    if (this.state.selectedRegions.has(region)) {
      selectedRegions.delete(region);
    } else {
      selectedRegions.add(region);
    }
    this.setState({selectedRegions: selectedRegions});
    this.props.onRegionSelecionChange(selectedRegions);
  }

  resetRegionSelection() {
    let selectedRegions = new Set();
    this.setState({selectedRegions: selectedRegions});
    this.props.onRegionSelecionChange(selectedRegions);
  }

  render() {

    var regions = d3.nest()
      .key(loan => loan.region)
      .sortKeys(d3.ascending)
      .rollup(regionLoans => ({
        gross_book_value: d3.sum(regionLoans, loan => loan['display'] === true ? loan.gross_book_value: 0),
        active: d3.sum(regionLoans, loan => loan['display'] === true && loan['active'] === true ? 1: 0),
        payed: d3.sum(regionLoans, loan => loan['display'] === true ? loan.payments_total: 0),
        r6: d3.mean(regionLoans, loan => loan['display'] === true ? loan['neuralnetwork_output_rs_6m']: null),
        r12: d3.mean(regionLoans, loan => loan['display'] === true ? loan['neuralnetwork_output_rs_12m']: null),
        r18: d3.mean(regionLoans, loan => loan['display'] === true ? loan['neuralnetwork_output_rs_18m']: null),
      }))
      .entries(this.props.loans)
    
    let self = this;
    let rows = regions.map((region, index)=> {
      let isChecked = self.state.selectedRegions.has(region.key);

      return (
        <tr key={index}>
          <td><input type="checkbox" checked={isChecked} onChange={()=>self.onRegionChange(region.key)} /></td>
          <td>{region.key}</td>
          <CurrencyCell ammount={region.value.gross_book_value} />
          <CurrencyCell ammount={region.value.payed} />
          <td className="text-right">{region.value.active}</td>
          <ProgressCircleCell percentage={region.value.r6} />
          <ProgressCircleCell percentage={region.value.r12} />
          <ProgressCircleCell percentage={region.value.r18} />
        </tr>
      )
    });
    
    return (
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Loans by region</h3>
          <div className="card-options">
            {this.state.selectedRegions.size > 0 ? <a onClick={this.resetRegionSelection} className="btn btn-secondary btn-sm ml-2">Reset</a>: null}
          </div>
        </div>
        <div className="table-responsive">
          <table className="table card-table table-vcenter text-nowrap">
            <thead>
              <tr>
                <th>-</th>
                <th>Code</th>
                <th>Borrowed</th>
                <th>Payed</th>
                <th>Act</th>
                <th>R6</th>
                <th>R12</th>
                <th>R18</th>
              </tr>
            </thead>
            <tbody>
              {rows}
            </tbody>
          </table>
        </div>
      </div>
    )
  }
}

export default RegionsTable;
