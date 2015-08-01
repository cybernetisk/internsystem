import React from 'react';
import { Link, RouteHandler } from 'react-router';

import Nav from './Nav';

export default class Root extends React.Component {

  render() {
    return (
      <div>
        <Nav />
        <div className='container'>
          <RouteHandler />
        </div>
      </div>
    );
  }
}
