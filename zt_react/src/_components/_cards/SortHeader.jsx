import React from 'react';
import PropTypes from 'prop-types';


const SortHeader = (props) => {
  const {
    sortingBy, sortKey, sortingDir, colSpan, name, sortClicked,
  } = props;
  const isSorting = sortingBy === sortKey;
  let icon;
  if (isSorting === true) {
    icon = (sortingDir === 'asc') ? <i className="fe fe-arrow-up" /> : <i className="fe fe-arrow-down" />;
  } else {
    icon = <i className="fe fe-minus" />;
  }

  return (
    <th
      colSpan={colSpan}
      onClick={() => sortClicked(sortKey)}
      style={{ cursor: 'pointer' }}
    >
      { name }
      <div className="text-right d-inline ">
        { icon }
      </div>
    </th>
  );
};

SortHeader.propTypes = {
  sortingBy: PropTypes.string.isRequired,
  sortKey: PropTypes.string.isRequired,
  sortingDir: PropTypes.string.isRequired,
  sortClicked: PropTypes.func.isRequired,
  name: PropTypes.string.isRequired,
  colSpan: PropTypes.number,
};

SortHeader.defaultProps = {
  colSpan: 1,
};

export default SortHeader;
