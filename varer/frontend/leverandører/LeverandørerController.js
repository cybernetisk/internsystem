(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('leverandører', {
            url: '/varer/leverandører',
            templateUrl: require('./index.html'),
            controller: 'LeverandørerController as leverandorer'
        })
    });

    module.controller('LeverandørerController', function (LeverandørerService) {
        var self = this;
        LeverandørerService.query(function (res) {
            self.items = res;
        });
    });
})();
