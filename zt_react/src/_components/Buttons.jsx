import React, { Component } from 'react';
import PropTypes from 'prop-types';


class LoadingButton extends Component {
  defaultProp = {
    tabIndex: 1,
  }

  static propTypes = {
    text: PropTypes.string.isRequired,
    isLoading: PropTypes.bool.isRequired,
    tabIndex: PropTypes.number,
  }


  render() {
    const { text, isLoading, tabIndex } = this.props;
    return (
      <button
        type="submit"
        tabIndex={tabIndex}
        className="btn btn-primary btn-block"
        disabled={isLoading}
      >
        {text}
        {isLoading
          ? (
            <span>
              &nbsp;
              <i className="fe fe-loader spinner" />
            </span>)
          : null}
      </button>
    );
  }
}

export default LoadingButton;
