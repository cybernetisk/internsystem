(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('salgsvarer', {
            url: '/varer/salgsvarer',
            templateUrl: 'views/varer/salgsvarer/index.html',
            controller: 'SalgsvarerController as salgsvarer'
        })
    });

    module.controller('SalgsvarerController', function (SalgsvarerService) {
        var self = this;
        SalgsvarerService.query(function(res) {
            self.items = res.results;
            self.pagination = res.pagination;
        });
    });
})();
