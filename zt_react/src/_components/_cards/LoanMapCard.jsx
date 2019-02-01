import geoViewport from '@mapbox/geo-viewport';
import * as d3 from "d3";
import 'mapbox-gl/dist/mapbox-gl.css';
import { connect } from 'react-redux';
import { PropTypes } from 'prop-types';
import React, { Component } from 'react';
import MapGL, { NavigationControl } from 'react-map-gl';
import CircleMarker from './CircleMarker';
import LoaderCard from './LoaderCard';

const MAPBOX_MAP_STYLE = 'mapbox://styles/mapbox/light-v9';
const MAPBOX_API_TOKEN = 'pk.eyJ1IjoiZmNlcnV0aSIsImEiOiJjamk0ZndyeWowOHdrM3BzMjNzcXZxd3EwIn0.GgiX4tu7xAVPoLcQXJo_Tw';


const navStyle = {
  position: 'absolute',
  top: 0,
  left: 0,
  padding: '10px',
};

class LoanMap extends Component {
  static propTypes = {
    loans: PropTypes.array,
    loading: PropTypes.bool,
    onBoundsChange: PropTypes.func.isRequired,
    onMarkerClicked: PropTypes.func.isRequired,
  }

  state = {
    currentMapAttr: {},
    initialMapAttr: {},
    initialized: false,
    elementId: 'map-container',
  }

  constructor(props) {
    super(props);
    this.resetViewport = this.resetViewport.bind(this);
    this.updateViewport = this.updateViewport.bind(this);
  }

  componentDidMount() {
    window.addEventListener('resize', this.resetViewport.bind(this));
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.resetViewport.bind(this));
  }

  getContainerDimensions() {
    const { elementId } = this.state;
    const mapContainerEl = document.getElementById(elementId);
    return [mapContainerEl.offsetWidth, mapContainerEl.offsetHeight];
  }

  initializeViewport() {
    const { loans, onBoundsChange } = this.props;
    this.setState({ initialized: true });
    const dimensions = this.getContainerDimensions();
    let maxLat = d3.max(loans, loan => loan.latitude);
    let minLat = d3.min(loans, loan => loan.latitude);
    let maxLng = d3.max(loans, loan => loan.longitude);
    let minLng = d3.min(loans, loan => loan.longitude);

    if (Number.isNaN(maxLat) || maxLat === undefined
       || Number.isNaN(minLat) || minLat === undefined
       || Number.isNaN(maxLng) || maxLng === undefined
       || Number.isNaN(minLng) || minLng === undefined) {
      minLat = 5.7228792694;
      maxLat = 20.6364270387;
      minLng = 35.9341958032;
      maxLng = 47.2895435851;
    }

    const viewport = geoViewport.viewport(
      [minLng, minLat, maxLng, maxLat],
      dimensions,
    );

    const zoom = viewport.zoom * 0.8;
    const bounds = geoViewport.bounds(
      viewport.center,
      zoom,
      dimensions,
      dimensions[0],
    );

    const mapAttr = {
      longitude: viewport.center[0],
      latitude: viewport.center[1],
      zoom,
      width: dimensions[0],
      height: dimensions[1],
    };
    this.setState({
      currentMapAttr: mapAttr,
      initialMapAttr: mapAttr,
    });
    onBoundsChange(bounds);
  }

  resetViewport() {
    const dimensions = this.getContainerDimensions();
    const { initialMapAttr } = this.state;
    const { zoom, latitude, longitude } = initialMapAttr;
    const { onBoundsChange } = this.props;
    const mapAttr = {
      longitude,
      latitude,
      zoom,
      width: dimensions[0],
      height: dimensions[1],
    };
    const bounds = geoViewport.bounds(
      [mapAttr.longitude, mapAttr.latitude],
      mapAttr.zoom,
      dimensions,
      dimensions[0],
    );

    this.setState({ currentMapAttr: mapAttr });
    onBoundsChange(bounds);
  }

  updateViewport(mapAttr) {
    this.setState({ currentMapAttr: mapAttr });
    const dimensions = this.getContainerDimensions();
    const { onBoundsChange } = this.props;
    const bounds = geoViewport.bounds(
      [mapAttr.longitude, mapAttr.latitude],
      mapAttr.zoom,
      dimensions,
      dimensions[0],
    );
    onBoundsChange(bounds);
  }

  render() {
    const { loading, loans } = this.props;
    if (loading) {
      return (
        <div className="card">
          <div className="card-body">
            <div id="map-container" style={{ minHeight: 330 }} />
          </div>
        </div>
      );
    }
    const { initialized, currentMapAttr, initialMapAttr } = this.state;
    if (!initialized) {
      this.initializeViewport();
    }

    const loanScale = d3
      .scaleLinear()
      .domain([
        d3.min(loans, loan => (loan.im_util_cassa)),
        d3.max(loans, loan => (loan.im_util_cassa)),
      ])
      .range([0.3, 1]);

    const hasChanged = currentMapAttr !== initialMapAttr;
    let map = null;
    let totalDisplayingLoans = 0;

    if (Object.prototype.hasOwnProperty.call(currentMapAttr, 'width')
        && Object.prototype.hasOwnProperty.call(currentMapAttr, 'height')) {
      const markers = [];
      const self = this;

      loans.forEach((loan, index) => {
        if (loan !== undefined
            && loan.latitude !== null && loan.latitude !== undefined
            && !Number.isNaN(loan.latitude)
            && loan.longitude !== null && loan.longitude !== undefined
            && !Number.isNaN(loan.longitude)) {
          totalDisplayingLoans += 1;
          const scaledPrincipal = loanScale(loan.im_util_cassa);

          markers.push((
            <CircleMarker
              key={loan.id}
              latitude={loan.latitude}
              longitude={loan.longitude}
              value={loan.im_util_cassa}
              radius={3}
              color={`rgba(255, 0, 0, ${scaledPrincipal})` }
              onClick={self.props.onMarkerClicked.bind(this, loan)}
            />
          ));
        }
      });
      map = (
        <MapGL
          ref="map"
          {...currentMapAttr}
          mapStyle={MAPBOX_MAP_STYLE}
          mapboxApiAccessToken={MAPBOX_API_TOKEN}
          onViewportChange={this.updateViewport}
          transitionDuration={0}
        >
          {markers.slice(0, 500)}
          <div className="nav" style={navStyle}>
            <NavigationControl
              onViewportChange={this.updateViewport}
            />
          </div>
        </MapGL>
      );
    }

    return (
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            Porfolio map
          </h3>
          <div className="card-options">
            {hasChanged
              ? (
                <button onClick={this.resetViewport} className="btn btn-secondary btn-sm ml-2" type="button">
                  Reset
                </button>)
              : null}
          </div>
        </div>
        <div className="card-body">
          <div id="map-container" style={{ minHeight: 330 }}>
            {map}
          </div>
          <p className="text-muted text-right">
            Displaying&nbsp;
            {totalDisplayingLoans}
            &nbsp;out of&nbsp;
            {loans.length}
            &nbsp;loans
          </p>
        </div>
      </div>
    );
  }
}


function mapStateToProps(state) {
  const { loans, loading } = state.loans;
  return {
    loans,
    loading,
  };
}

export default connect(mapStateToProps)(LoanMap);
