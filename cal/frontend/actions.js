import reactor from './reactor'
import CalendarService from './services/CalendarService'

import {
  RECEIVE_LIST_START,
  RECEIVE_LIST_SUCCESS,
  RECEIVE_LIST_FAILURE,
  RECEIVE_EVENT_START,
  RECEIVE_EVENT_SUCCESS,
  RECEIVE_EVENT_FAILURE,
} from './actionTypes'

export default {
  fetchList() {
    reactor.dispatch(RECEIVE_LIST_START)

    CalendarService.getEventList().then((list) => {
      reactor.dispatch(RECEIVE_LIST_SUCCESS, {list})
    }).catch((err) => {
      reactor.dispatch(RECEIVE_LIST_FAILURE, err)
    })
  },

  fetchEvent(eventId) {
    reactor.dispatch(RECEIVE_EVENT_START)

    CalendarService.getEvent(eventId).then((event) => {
      reactor.dispatch(RECEIVE_EVENT_SUCCESS, {event})
    }).catch((err) => {
      let msg = err.statusText
      if (err.status === 404) {
        msg = 'Data ble ikke funnet'
      }
      reactor.dispatch(RECEIVE_EVENT_FAILURE, msg)
    })
  }
}
