import moment from '../../../siteroot/frontend_react/moment'
import React from 'react'
import { Link } from 'react-router'
import { nuclearComponent } from 'nuclear-js-react-addons'

import actions from '../actions'
import getters from '../getters'

import PageLoader from '../../../siteroot/frontend_react/components/PageLoader'

@nuclearComponent({
  event: getters.event
})
export default class Event extends React.Component {
  componentDidMount() {
    actions.fetchEvent(this.props.params.eventId)
  }

  renderIncomplete() {
    return (
      <PageLoader
        error={this.props.event.get('error')}
        isLoading={this.props.event.get('isLoading')}
        title='Arrangement'/>
    )
  }

  render() {
    let event = this.props.event.get('data')
    if (event === null) {
      return this.renderIncomplete()
    }

    event = event.toJS()

    let start, end;
    if (event.is_allday) {
      start = moment(event.start).utc().format("dddd DD. MMM YYYY");
      end = moment(event.end).utc().format("dddd DD. MMM YYYY");
    } else {
      start = moment(event.start).format("dddd DD. MMM YYYY HH:mm");
      end = moment(event.end).format("dddd DD. MMM YYYY HH:mm");
    }

    return (
      <div>
        <h1>Arrangement: {event.title}</h1>

        <p><Link to='cal/list'>Tilbake</Link></p>

        <p>{start === end ? start : `${start} til ${end}`}</p>

        {event.description !== '' ? (
          <p>Beskrivelse: {event.description}</p>
        ) : ''}

        <dl>
          <dt>I Escape?</dt>
          <dd>{event.in_escape ? 'Ja' : 'Nei'}</dd>
          <dt>Kansellert?</dt>
          <dd>{event.is_cancelled ? 'Ja' : 'Nei'}</dd>
          <dt>Eksternt arr?</dt>
          <dd>{event.is_external ? 'Ja' : 'Nei'}</dd>
          <dt>Public?</dt>
          <dd>{event.is_published ? 'Ja' : 'Nei'}</dd>
          <dt>Link</dt>
          <dd>{event.link !== '' ? event.link : 'ingen'}</dd>
          <dt>Organizer</dt>
          <dd>{event.organizer ? event.organizer.realname : 'ingen'}</dd>
        </dl>

        <p><a target="_self" href={`cal/events/${event.id}.ics`}>.ics</a></p>
      </div>
    )
  }
}
