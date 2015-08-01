import React from 'react'
import { Route, RouteHandler } from 'react-router'
import { provideReactor } from 'nuclear-js-react-addons'

import reactor from './reactor'

import Event from './components/Event'
import List from './components/List'

import EventStore from './stores/EventStore'
import ListStore from './stores/ListStore'

reactor.registerStores({
  list: ListStore,
  event: EventStore
})

@provideReactor
class ReactorWrapper extends React.Component {
  render() {
    return <RouteHandler />;
  }
}

class CalRoot extends React.Component {
  render() {
    return <ReactorWrapper reactor={reactor} />;
  }
}

module.exports = (
  <Route handler={CalRoot}>
    <Route name="cal/list" path="/cal" handler={List} />
    <Route name="cal/event" path="/cal/event/:eventId" handler={Event} />
  </Route>
)
