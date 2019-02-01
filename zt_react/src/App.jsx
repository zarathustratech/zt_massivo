import React from 'react';
import { Router, Route, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';

import { history } from './_helpers';
import AppLayout from './Pages/AppLayout';
import LoginPage from './Pages/LoginPage';
import RegisterPage from './Pages/RegisterPage';
import { PrivateRoute, Footer } from './_components';


class App extends React.Component {
  constructor(props) {
    super(props);

    const { dispatch } = this.props;
    history.listen((location, action) => {
      // clear alert on location change
      // dispatch(alertActions.clear());
    });
  }

  render() {
    const { user } = this.props;

    return (
      <Router history={history} basename={process.env.SUBDIRECTORY}>
        <div className="page">
          <Route
            exact
            path="/"
            render={() => (
              user
                ? <Redirect to="/portfolio" />
                : <Redirect to="/login" />
            )}
          />
          <PrivateRoute
            path="/portfolio"
            component={AppLayout}
          />
          <Route
            path="/login"
            component={LoginPage}
          />
          <Route
            path="/register"
            component={RegisterPage}
          />
          <Footer />
        </div>
      </Router>
    );
  }
}

function mapStateToProps(state) {
  const { authentication } = state;
  return {
    user: authentication.user,
  };
}

const connectedApp = connect(mapStateToProps)(App);
export default connectedApp;
