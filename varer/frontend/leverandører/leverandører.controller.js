(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('leverandører', {
            url: '/varer/leverandører',
            templateUrl: 'views/leverandører/index.html',
            controller: 'LeverandørerController'
        })
    });

    module.controller('LeverandørerController', function () {
        console.log("LeverandørerController");
    });
})();
