import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { Link, Redirect } from 'react-router-dom';
import { alertActions } from '../_actions';
import { portfolioConstants } from '../_constants';
import { SpinnerCard, UploaderCard } from '../_components';


const UploadPage = (props) => {
  const { portfolio, loading, dispatch } = props;

  if (portfolio !== null && portfolio !== undefined) {
    dispatch(alertActions.success('The portfolio was created. We will let you know by email when the data processing is ready, it could take several hours.'));
    dispatch({ type:portfolioConstants.CLEAR });
    return <Redirect to="/portfolio" />;
  }
  return (
    <div className="container">
      <div className="page-header">
        <p>
          <Link to="/portfolio">
            <i className="fe fe-arrow-left" />
            My portfolios
          </Link>
        </p>
        <h1 className="page-title">
          Upload portfolio
        </h1>
      </div>
      <div className="row">
        <div className="col-6">
          {loading
            ? <SpinnerCard />
            : <UploaderCard />
          }
        </div>
        {/* This is completely optional */}
        <div className="col-5">
          <div style={{ padding: 30 }}>
            <h5 className="upload-bullets-title">
              Things to consider
            </h5>
            <ul className="upload-bullets">
              <li>
                <i className="fe fe-file-text bullet-icon" />
                We do our best to support multiple file formats,
                but if yours is not working contact our ...
              </li>
              <li>
                <i className="fe fe-shield bullet-icon" />
                We will protect your data. It&#39;s strictly confidential.
                For more information read our privacy policy.
              </li>
              <li>
                <i className="fe fe-help-circle bullet-icon" />
                What to do if you need help. Maybe send an email
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

UploadPage.propTypes = {
  dispatch: PropTypes.func.isRequired,
  portfolio: PropTypes.shape({
    code: PropTypes.string.isRequired,
  }),
  loading: PropTypes.bool,
};

UploadPage.defaultProps = {
  portfolio: null,
  loading: false,
};


function mapStateToProps(state) {
  const { createPortfolio, createLoading } = state.portfolio;
  return {
    portfolio: createPortfolio,
    loading: createLoading,
  };
}

export default connect(mapStateToProps)(UploadPage);
