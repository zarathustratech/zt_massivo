import numeral from 'numeral';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import LoaderCard from './LoaderCard';
import ProgressCard from './ProgressCard';


const Card = (props) => {
  const { loans, loading } = props;
  if (loading) {
    return <LoaderCard />;
  }

  let totalLoaned = 0;
  let totalPayed = 0;
  for (let i = 0; i < loans.length; i++) {
    totalLoaned += loans[i].principal;
    totalPayed += loans[i].total_payed;
  }

  let paymentPercentage = 0;
  if (totalLoaned > 0) {
    paymentPercentage = totalPayed / totalLoaned;
  }

  return (
    <ProgressCard
      name="Total payed so far"
      value={'€' + numeral(totalPayed).format('0,')}
      percentage={paymentPercentage}
    />
  );
};

Card.propTypes = {
  loans: PropTypes.array,
  loading: PropTypes.bool,
};


function mapStateToProps(state) {
  const { loans, loading } = state.loans;
  return {
    loans,
    loading,
  };
}

export default connect(mapStateToProps)(Card);
