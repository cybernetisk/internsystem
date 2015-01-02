(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('varer', {
            url: '/varer',
            templateUrl: 'views/varer/index/index.html',
            controller: 'VarerIndexController'
        });
    });

    module.controller('VarerIndexController', function () {
        console.log("VarerIndexController");
    });

})();
