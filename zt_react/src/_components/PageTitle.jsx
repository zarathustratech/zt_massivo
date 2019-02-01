import React from 'react';
import PropTypes from 'prop-types';


const PageTitle = (props) => {
  const { btn, title, subtitle } = props;
  return (
    <div className="page-header">
      <h1 className="page-title">
        {btn}
        {title}
      </h1>
      {subtitle
        ? (
          <p className="page-subtitle">
            {subtitle}
          </p>
        )
        : null}
    </div>
  );
};

PageTitle.propTypes = {
  title: PropTypes.string.isRequired,
  subtitle: PropTypes.string,
  btn: PropTypes.element,
};

PageTitle.defaultProps = {
  subtitle: null,
  btn: null,
};


export default PageTitle;
