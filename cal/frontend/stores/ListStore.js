import { Store, toImmutable } from 'nuclear-js'
import {
  RECEIVE_LIST_START,
  RECEIVE_LIST_SUCCESS,
  RECEIVE_LIST_FAILURE
} from '../actionTypes'

export default Store({
  getInitialState() {
    return toImmutable({
      error: null,
      items: [],
      loading: true
    })
  },

  initialize() {
    this.on(RECEIVE_LIST_START, receiveListStart)
    this.on(RECEIVE_LIST_SUCCESS, receiveListSuccess)
    this.on(RECEIVE_LIST_FAILURE, receiveListFailure)
  }
})

function receiveListStart(state) {
  return state
    .set('error', null)
    .set('items', toImmutable({}))
    .set('loading', true)
}

function receiveListSuccess(state, { list }) {
  return state
    .set('items', toImmutable(list)
      .toMap()
      .mapKeys((k, v) => v.get('id')))
    .set('loading', false)
}

function receiveListFailure(state, err) {
  console.log("Receiving list failed", err)
  return state
    .set('error', toImmutable(err))
    .set('loading', false)
}