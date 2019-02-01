import React, { Component } from 'react';
import { PropTypes } from 'prop-types';
import { connect } from 'react-redux';
import { Route } from 'react-router-dom';

import PortfolioDetailPage from './PortfolioDetailPage';
import UploadPage from './UploadPage';
import PortfolioListPage from './PortfolioListPage';

import { accountActions, alertActions } from '../_actions';
import { Header } from '../_components';


class AppLayout extends Component {
  static defaultProp = {
    user: { loggedIn: false, user: { key: null } },
  }

  static propTypes = {
    user: PropTypes.shape({
      loggedIn: PropTypes.bool,
      user: PropTypes.shape({
        key: PropTypes.string,
      }),
    }).isRequired,
    dispatch: PropTypes.func.isRequired,
  }

  constructor(props) {
    super(props);
    this.closeAlert = this.closeAlert.bind(this);
  }

  closeAlert () {
    const { dispatch } = this.props;
    dispatch(alertActions.clear());
  }

  componentDidMount() {
    const { user, dispatch } = this.props;
    dispatch(accountActions.me(user));
  }

  render() {
    const { alert } = this.props;
    return (
      <div className="page-main">
        <Header />
        {alert.message
          && (
            <div className={`alert ${alert.type}`}>
              <div className="container">
                <button onClick={this.closeAlert} type="button" className="close" data-dismiss="alert" />
                {alert.message}
              </div>
            </div>
          )
        }
        <Route path="/portfolio/upload" component={UploadPage} />
        <Route path="/portfolio/i/:code([0-9a-z-]*)" component={PortfolioDetailPage} />
        <Route path="/portfolio" exact component={PortfolioListPage} />
      </div>
    );
  }
}

function mapStateToProps(state) {
  const { authentication, alert } = state;
  return { user: authentication.user, alert };
}

export default connect(mapStateToProps)(AppLayout);
