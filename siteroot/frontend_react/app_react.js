import '../frontend/app.scss';

import domready from 'domready'
import React from 'react';
import Router from 'react-router';
import { DefaultRoute, Link, Route, RouteHandler } from 'react-router';

import Root from './components/Root';
import Index from './components/Index';

import Cal from '../../cal/frontend';

let routes = (
  <Route handler={Root}>
    <Route name="index" path="/" handler={Index} />
    {Cal}
  </Route>
);

let rootInstance;
Router.run(routes, Router.HistoryLocation, Handler => {
  domready(() => {
    rootInstance = React.render(<Handler/>, document.getElementById('react_container'));
  });
});

if (module.hot) {
  require('react-hot-loader/Injection').RootInstanceProvider.injectProvider({
    getRootInstances: function () {
      // Help React Hot Loader figure out the root component instances on the page:
      return [rootInstance];
    }
  });
}
