import { Store, toImmutable } from 'nuclear-js'
import {
  RECEIVE_EVENT_START,
  RECEIVE_EVENT_SUCCESS,
  RECEIVE_EVENT_FAILURE
} from '../actionTypes'

export default Store({
  getInitialState() {
    return toImmutable({
      data: null,
      error: null,
      isLoading: true
    })
  },

  initialize() {
    this.on(RECEIVE_EVENT_START, receiveEventStart)
    this.on(RECEIVE_EVENT_SUCCESS, receiveEventSuccess)
    this.on(RECEIVE_EVENT_FAILURE, receiveEventFailure)
  }
})

function receiveEventStart(state) {
  return state
    .set('data', null)
    .set('error', null)
    .set('isLoading', true)
}

function receiveEventSuccess(state, { event }) {
  return state
    .set('data', toImmutable(event))
    .set('isLoading', false)
}

function receiveEventFailure(state, err) {
  console.log("Receiving list failed", err)
  return state
    .set('error', toImmutable(err))
    .set('isLoading', false)
}