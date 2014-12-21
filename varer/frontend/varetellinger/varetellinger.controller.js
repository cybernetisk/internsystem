(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('varetellinger', {
            url: '/varer/varetellinger',
            templateUrl: 'views/varetellinger/index.html',
            controller: 'VaretellingerController'
        })
    });

    module.controller('VaretellingerController', function () {
        console.log("VaretellingerController");
    });
})();
