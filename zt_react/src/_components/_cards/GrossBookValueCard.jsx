import numeral from 'numeral';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import LoaderCard from './LoaderCard';
import IconCard from './IconCard';


const Card = (props) => {
  const { loans, loading } = props;
  if (loading) {
    return <LoaderCard />;
  }

  let totalLoaned = 0;
  for (let i = 0; i < loans.length; i++) {
    totalLoaned += loans[i].principal;
  }
  return (
    <IconCard
      iconClass="fe fe-dollar-sign"
      bgColor="red"
      text={'€' + numeral(totalLoaned).format('0,0')}
      mutedText="Nominal value"
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
