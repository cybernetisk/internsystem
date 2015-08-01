import React from 'react'

import Loader from './Loader'

export default class PageLoader extends React.Component {

  PropTypes = {
    children: React.PropTypes.node,
    error: React.PropTypes.string,
    isEmpty: React.PropTypes.bool,
    isLoading: React.PropTypes.bool.isRequired,
    title: React.PropTypes.string.isRequired
  }

  render() {
    return (
      <div>
        <h1>{this.props.title}</h1>
        {this.props.children}
        <Loader {...this.props} />
      </div>
    )
  }
}
