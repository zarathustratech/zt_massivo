import React, { Component } from 'react';
import { PropTypes } from 'prop-types'


class AvatarCell extends Component {

  static propTypes = {
    active: PropTypes.bool.isRequired,
    name: PropTypes.string.isRequired,
  }

  render() {
    var initials = [];

    this.props.name.split(' ').forEach(element => {
      initials.push(element.charAt(0));
    });
    initials = initials.slice(0, 2);

    var statusClassName = this.props.active === true ? 'avatar-status bg-green' : 'avatar-status bg-red';
    return (
      <td className="text-center">
        <div className="avatar d-block">  {/* style="background-image: url(demo/faces/female/26.jpg)" */}
          {initials.join('')} <span className={statusClassName}></span>
        </div>
      </td>
    )
  }
}

export default AvatarCell;
