import { createBrowserHistory } from 'history';

const history = createBrowserHistory({
  basename: process.env.SUBDIRECTORY,
});

export default history;
