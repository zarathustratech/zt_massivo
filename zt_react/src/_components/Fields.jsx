import React, {Component} from 'react';
import PropTypes from 'prop-types';


export class FormField extends Component {
  static propTypes = {
    type: PropTypes.oneOf(['password', 'email', 'text']).isRequired,
    name: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    submitted: PropTypes.bool.isRequired,
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    tabIndex: PropTypes.number,
    isRequired: PropTypes.bool,
    onChange: PropTypes.func.isRequired,
    errors: PropTypes.array,
  }

  static defaultPropTypes = {
    tabIndex: "1",
    isRequired: true,
  }

  render () {
    let fieldId = `${this.props.name}_field`;

    let errors = null;
    if (this.props.errors) {
      errors = this.props.errors.map((error, index) =>
        <div className="invalid-feedback" key={index}>{error}</div>
      );
    }
    return (
      <div className="form-group">
        <label className="form-label" htmlFor={fieldId}>{this.props.label}</label>
        <input
          id={fieldId}
          type={this.props.type}
          className={this.props.submitted && errors ? 'form-control is-invalid' : 'form-control' }
          name={this.props.name}
          tabIndex={this.props.tabIndex}
          value={this.props.value}
          onChange={this.props.onChange} />
        { errors }
      </div>
    )
  }
}

export class NonFieldErrors extends Component {

  render() {
    let { errors } = this.props;
    let errorMessage = null;
    if (errors && errors.hasOwnProperty('non_field_errors')) {
      errorMessage = errors['non_field_errors'].map((error, index) =>
        <div className="alert alert-danger" key={index}>{error}</div>
      );
    }
    return errorMessage;
  }
}