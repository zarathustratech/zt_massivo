import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import 'tabler-ui/dist/assets/css/dashboard.css';
import App from './App';
import './Assets/Styles/main.sass';
import { store } from './_helpers';


// registerServiceWorker();

render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root'),
);
