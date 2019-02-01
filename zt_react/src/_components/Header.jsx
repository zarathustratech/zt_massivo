import React, { Component } from 'react';
import PropType from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { accountActions, alertActions } from '../_actions';
import logo from '../Assets/Images/logo_wide.png';


class Header extends Component {
  static propTypes = {
    dispatch: PropType.func.isRequired,
    account: PropType.shape({
      first_name: PropType.string,
      last_name: PropType.string,
      company: PropType.string,
    }),
  }

  static defaultProps = {
    account: { first_name: '', last_name: '', company: '' },
  }

  onLogoutClicked() {
    const { dispatch } = this.props;
    dispatch(accountActions.logout());
  }

  render() {
    const { account } = this.props;
    const { first_name, last_name, company } = account;

    let initials = '';
    if (first_name) initials += first_name.charAt(0);
    if (last_name) initials += last_name.charAt(0);

    return (
      <div className="header">
        <div className="container">
          <div className="d-flex">
            {/* Logo */}
            <Link to="/portfolio" className="header-brand">
              <img src={logo} alt="Zarathustra Technologies" className="dashboard-logo" />
            </Link>
            <div className="d-flex order-lg-2 ml-auto">
              {/* User profile */}

              <div className="dropdown">
                <a className="nav-link pr-0 leading-none" data-toggle="dropdown" aria-expanded="false">
                  <span className="avatar">
                    {initials}
                  </span>
                  <span className="ml-2 d-none d-lg-block">
                    <span className="text-default">
                      {first_name} {last_name}
                    </span>
                    <small className="text-muted d-block mt-1">
                      {company}
                    </small>
                  </span>
                </a>
              </div>
              <div className="dropdown d-none d-md-flex">
                <a onClick={this.onLogoutClicked.bind(this)} className="nav-link icon log-out-btn">
                  <i className="fe fe-log-out" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

function mapStateToProps(state) {
  const { account } = state;
  return { account: account.account ? account.account : {} };
}

const connectedHeader = connect(mapStateToProps)(Header);
export { connectedHeader as default };
