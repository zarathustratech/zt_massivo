import { PropTypes } from 'prop-types';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import logo from '../Assets/Images/logo_tall.png';
import { accountActions } from '../_actions';
import { FormField, LoadingButton, NonFieldErrors } from '../_components';


class LoginPage extends Component {
  static propTypes = {
    loading: PropTypes.bool,
    errors: PropTypes.shape(),
    alert: PropTypes.shape(),
    dispatch: PropTypes.func.isRequired,
  }

  static defaultProps = {
    errors: {},
    loading: false,
  }

  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.closeAlert = this.closeAlert.bind(this);
  }

  closeAlert () {
    const { dispatch } = this.props;
    dispatch(alertActions.clear());
  }


  state = {
    email: '',
    password: '',
    submitted: false,
  }

  handleChange(e) {
    const { name, value } = e.target;
    this.setState({ [name]: value });
  }

  handleSubmit(e) {
    e.preventDefault();
    this.setState({ submitted: true });
    const { email, password } = this.state;
    if (email && password) {
      const { dispatch } = this.props;
      dispatch(accountActions.login(email, password));
    }
  }


  render() {
    const { loading, errors, alert } = this.props;
    const { email, password, submitted } = this.state;

    var alertBox = null;
    if (alert && alert.type) {
      alertBox = (
        <div className={`alert ${alert.type}`}>
          <div className="container">
            <button onClick={this.closeAlert} type="button" className="close" data-dismiss="alert" />
            {alert.message}
          </div>
        </div>
      );
    }

    return (
      <div className="page-single">
        <div className="container">
          <div className="row">
            <div className="col col-login mx-auto">
              <div className="text-center mb-6">
                <img src={logo} className="app-logo" alt="Zarathustra technologies" />
              </div>
              {alertBox}
              <form className="card" onSubmit={this.handleSubmit}>
                <div className="card-body p-6">
                  <div className="card-title">
                    Login to your account
                  </div>
                  <NonFieldErrors errors={errors} />
                  <FormField
                    type="text"
                    name="email"
                    label="Email address"
                    tabIndex={1}
                    value={email}
                    submitted={submitted}
                    onChange={this.handleChange}
                    errors={errors.email}
                  />
                  <FormField
                    type="password"
                    name="password"
                    label="Password"
                    tabIndex={2}
                    value={password}
                    submitted={submitted}
                    onChange={this.handleChange}
                    errors={errors.password}
                  />

                  <div className="form-footer">
                    <LoadingButton
                      text="Sign in"
                      isLoading={loading}
                      tabIndex={3}
                    />
                  </div>
                </div>
              </form>
              <div className="text-center text-muted">
                Don&apos;t have account yet?&nbsp;
                <Link to="/register">
                  Register
                </Link>
                .
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

function mapStateToProps(state) {
  const { loggingIn, loggingError } = state.authentication;
  const { alert } = state;

  return {
    loading: loggingIn,
    errors: loggingError,
    alert,
  };
}

export default connect(mapStateToProps)(LoginPage);
