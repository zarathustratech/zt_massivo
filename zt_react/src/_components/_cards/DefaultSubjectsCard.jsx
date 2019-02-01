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

  let defaultCases = 0;
  for (let i = 0; i < loans.length; i++) {
      if (loans[i].prediction == '1') {
          defaultCases++;
      }
  }
  return (
    <IconCard
      iconClass="fe"
      bgColor="red"
      text={defaultCases}
      mutedText="Predicted Default Cases"
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