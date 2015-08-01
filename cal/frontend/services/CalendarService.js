import reqwest from 'reqwest';

class CalendarService {

  getEventList() {
    return reqwest({
      url: 'api/cal/events/',
      type: 'json'
    });
  }

  getEvent(eventId) {
    return reqwest({
      url: 'api/cal/events/' + eventId + '/',
      type: 'json'
    });
  }
}

export default new CalendarService();
