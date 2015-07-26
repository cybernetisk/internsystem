'use strict';

const angular = require('angular');

const module = angular.module('cyb.cal');
const CalService = require('./CalService');

module.config(($stateProvider) => {
  $stateProvider.state('cal/event', {
    url: '/cal/event/:id',
    templateUrl: require('./event.html'),
    controller: 'CalEventController as cal'
  });
});

module.controller('CalEventController', function (CalService, $stateParams) {
  console.log("CalEventController");

  CalService.get({id: $stateParams['id']}, (res) => {
    this.item = res;
  });
});
