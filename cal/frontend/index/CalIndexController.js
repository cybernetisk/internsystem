(function() {
    'use strict';

    var module = angular.module('cyb.cal');
    const CalService = require('./CalService');

    module.config(function ($stateProvider) {
        $stateProvider.state('cal', {
            url: '/cal',
            templateUrl: require('./index.html'),
            controller: 'CalIndexController as cal'
        });
    });

    module.controller('CalIndexController', function (CalService) {
        console.log("CalIndexController");

        CalService.query(function(res) {
            this.items = res;
        }.bind(this));
    });

})();
