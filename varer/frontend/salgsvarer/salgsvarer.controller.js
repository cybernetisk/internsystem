(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('salgsvarer', {
            url: '/varer/salgsvarer',
            templateUrl: 'views/salgsvarer/index.html',
            controller: 'SalgsvarerController'
        })
    });

    module.controller('SalgsvarerController', function () {
        console.log("SalgsvarerController");
    });
})();
