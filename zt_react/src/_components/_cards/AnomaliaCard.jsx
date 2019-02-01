import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import LoaderCard from './LoaderCard';
import BarChart from 'react-bar-chart';


const Card = (props) => {
  const { loans, loading, selectedCd } = props;
  if (loading || selectedCd==0) {
    return <LoaderCard />;
  }

  const filteredLoans = loans.filter(item => item.ngr_cd === selectedCd);

  const anomalia_codes = filteredLoans
          .map(dataItem => dataItem.cd_anomalia)
          .filter((anomalia_cd, index, array) => array.indexOf(anomalia_cd) === index);

  let data = [];
  let totalAnomalias = anomalia_codes.length;
  for (let i = 0; i < totalAnomalias; i++) {
      const anomalia_cd = anomalia_codes[i];
      const some_loans = filteredLoans.filter(item => item.cd_anomalia === anomalia_cd);
      const dummyLoan = some_loans[0];
      data.push({
          text: dummyLoan.ds_anomalia,
          value: some_loans.length,
      });
    };

  const margin = {top: 20, right: 20, bottom: 30, left: 40};

  return (
    <div>
        <div style={{width: '50%'}}>
            <BarChart ylabel='Num Events'
                      margin={margin}
                      width={800}
                      height={500}
                      data={data}/>
        </div>
    </div>
  );
};

Card.propTypes = {
  loans: PropTypes.array,
  loading: PropTypes.bool,
  selectedCd: PropTypes.number,
};


function mapStateToProps(state) {
  const { loans, loading } = state.loans;
  return {
    loans,
    loading,
  };
}

export default connect(mapStateToProps)(Card);
