(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('salgskalkyler', {
            url: '/varer/salgskalkyler',
            templateUrl: 'views/varer/salgskalkyler/index.html',
            controller: 'SalgskalkylerController'
        })
    });

    module.controller('SalgskalkylerController', function () {
        console.log("SalgskalkylerController");
    });
})();
