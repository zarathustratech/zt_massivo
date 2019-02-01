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

  let performingCases = 0;
  for (let i = 0; i < loans.length; i++) {
      if (loans[i].prediction == '0') {
          performingCases++;
      }
  }
  return (
    <IconCard
      iconClass="fe"
      bgColor="blue"
      text={performingCases}
      mutedText="Predicted Performing Cases"
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