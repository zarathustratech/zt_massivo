import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Dropzone from 'react-dropzone';
import { portfolioActions } from '../_actions';


class UploaderCard extends Component {
  static propTypes = {
    dispatch: PropTypes.func.isRequired,
    errors: PropTypes.object,
  }

  static defaultProps = {
    errors: null,
  }

  constructor(props) {
    super(props);
    this.onDrop = this.onDrop.bind(this);
  }

  onDrop(acceptedFiles, rejectedFiles) {
    const { dispatch } = this.props;
    dispatch(portfolioActions.create(acceptedFiles, ''));
  }

  render() {
    const { errors } = this.props;

    let errorElements = null;
    if (errors !== undefined && errors !== null) {
      const createErrorElement = (error) => {
        const errMsgs = Object.values(error).join(', ');
        return (
          <div className="alert alert-danger">
            {errMsgs}
          </div>
        );
      };
      if (errors instanceof Array) {
        errorElements = errors.map(error => createErrorElement(error));
      }
      if (errors instanceof Object) {
        errorElements = createErrorElement(errors);
      }
    }

    return (
      <div className="card">
        <div className="card-body">
          {errorElements}
          <Dropzone onDrop={this.onDrop} className="dropzone">
            <p className="big-text">
              Upload file
            </p>
            <p className="dragndrop-icon">
              <i className="fe fe-upload-cloud" />
            </p>
            <p className="dragndrop-legend color-primary">
              Drag & drop
            </p>
            <p className="big-text">
              or
            </p>
            <button type="submit" className="btn btn-outline-primary dragndrop-btn">
              Browse file
            </button>
          </Dropzone>
        </div>
      </div>
    );
  }
}

function mapStateToProps(state) {
  const { createErrors } = state.portfolio;
  return {
    errors: createErrors,
  };
}

export default connect(mapStateToProps)(UploaderCard);
