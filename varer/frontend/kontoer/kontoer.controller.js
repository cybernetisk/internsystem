(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('kontoer', {
            url: '/varer/kontoer',
            templateUrl: 'views/kontoer/index.html',
            controller: 'KontoerController'
        })
    });

    module.controller('KontoerController', function () {
        console.log("KontoerController");
    });
})();
