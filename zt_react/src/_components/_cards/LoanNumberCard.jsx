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

  return (
    <IconCard
      iconClass="fe fe-users"
      bgColor="blue"
      text={'€' + numeral(loans.length).format('0,0')}
      mutedText="Number of loans"
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
