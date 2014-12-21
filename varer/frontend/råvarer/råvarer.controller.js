(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('råvarer', {
            url: '/varer/råvarer',
            templateUrl: 'views/råvarer/index.html',
            controller: 'RåvarerController'
        })
    });

    module.controller('RåvarerController', function () {
        console.log("RåvarerController");
    });
})();
