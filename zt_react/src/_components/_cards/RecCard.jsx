import numeral from 'numeral';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import LoaderCard from './LoaderCard';
import MessageCard from './MessageCard';


const Card = (props) => {
  const { loans, loading, recN } = props;
  if (loading) {
    return <LoaderCard />;
  }

  let totalRec;
  let totalPrincipal = 0;
  for (let i = 0; i < loans.length; i++) {
    const rec = loans[i][`rec_${recN}`];
    const principal = loans[i].principal;
    totalPrincipal += principal;
    if (!isNaN(rec)) {
      totalRec += principal * rec;
    }
  }
  let recPercentage = 0;
  if (totalPrincipal > 0) {
    recPercentage = totalRec / totalPrincipal;
  }

  return (
    <MessageCard
      row1="Recoverability"
      row2={numeral(recPercentage).format('%0')}
      row3={`${recN} months`}
    />
  );
};

Card.propTypes = {
  loans: PropTypes.array,
  loading: PropTypes.bool,
  rec_n: PropTypes.string,
};


function mapStateToProps(state) {
  const { loans, loading } = state.loans;
  return {
    loans,
    loading,
  };
}

export default connect(mapStateToProps)(Card);
