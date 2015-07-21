(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('kontoer', {
            url: '/varer/kontoer',
            templateUrl: require('./index.html'),
            controller: 'KontoerController as kontoer'
        })
    });

    module.controller('KontoerController', function (KontoerService) {
        var self = this;

        KontoerService.query(function(res) {
            self.items = res;
        });
    });
})();
