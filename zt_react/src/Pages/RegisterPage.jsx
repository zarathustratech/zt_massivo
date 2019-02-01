import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import logo from '../Assets/Images/logo_tall.png';
import { accountActions } from '../_actions';
import { FormField, LoadingButton, NonFieldErrors } from '../_components';


class RegisterPage extends React.Component {
  state = {
    user: {
      first_name: '',
      last_name: '',
      company: '',
      email: '',
      password1: '',
      password2: '',
    },
    submitted: false
  }

  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    const { name, value } = event.target;
    const { user } = this.state;
    this.setState({
      user: {
        ...user,
        [name]: value
      }
    });
  }

  handleSubmit(event) {
    event.preventDefault();
    this.setState({ submitted: true });
    this.props.dispatch(accountActions.register(this.state.user));
  }

  render() {
    const { loading, errors  } = this.props;
    const { user, submitted } = this.state;

    return (
      <div className="page-single">
        <div className="container">
          <div className="row">
            <div className="col col-login mx-auto">
              <div className="text-center mb-6">
                <img src={logo} className="app-logo" alt="Zarathustra technologies" />
              </div>
              <form className="card" onSubmit={this.handleSubmit}>
                <div className="card-body p-6">
                  <div className="card-title">Login to your account</div>
                  <NonFieldErrors errors={errors} />
                  <FormField
                    type="text"
                    name="company"
                    label="Company"
                    tabIndex={1}
                    isRequired={true}
                    value={user.company}
                    errors={errors.company}
                    submitted={submitted}
                    onChange={this.handleChange}
                  />
                  <FormField
                    type="text"
                    name="first_name"
                    label="First name"
                    tabIndex={2}
                    isRequired={true}
                    value={user.first_name}
                    errors={errors.first_name}
                    submitted={submitted}
                    onChange={this.handleChange}
                  />
                  <FormField
                    type="text"
                    name="last_name"
                    label="Last name"
                    tabIndex={3}
                    isRequired={true}
                    value={user.last_name}
                    errors={errors.last_name}
                    submitted={submitted}
                    onChange={this.handleChange}
                  />
                  <FormField
                    type="email"
                    name="email"
                    label="Email address"
                    tabIndex={4}
                    isRequired={true}
                    value={user.email}
                    errors={errors.email}
                    submitted={submitted}
                    onChange={this.handleChange}
                  />
                  <FormField
                    type="password"
                    name="password1"
                    label="Password"
                    tabIndex={5}
                    isRequired={true}
                    value={user.password1}
                    errors={errors.password1}
                    submitted={submitted}
                    onChange={this.handleChange}
                  />
                  <FormField
                    type="password"
                    name="password2"
                    label="Repeat password"
                    tabIndex={6}
                    isRequired={true}
                    value={user.password2}
                    errors={errors.password2}
                    submitted={submitted}
                    onChange={this.handleChange}
                  />

                  <div className="form-footer">
                    <LoadingButton
                      text="Sign in"
                      isLoading={loading ? true : false}
                      tabIndex={7}
                    />
                  </div>
                </div>
              </form>
              <div className="text-center text-muted">
                Already have an account? <Link to='/login'>Login now</Link>.
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

function mapStateToProps(state) {
  const { registering, errors } = state.registration;
  return {
    loading: registering,
    errors: errors
  };
}

export default connect(mapStateToProps)(RegisterPage);
