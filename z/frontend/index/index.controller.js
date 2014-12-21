(function() {
    'use strict';

    var module = angular.module('cyb.z');

    module.config(function ($stateProvider) {
        $stateProvider.state('z', {
            url: '/z',
            templateUrl: 'views/z/index/index.html',
            controller: 'ZIndexController'
        });
    });

    module.controller('ZIndexController', function () {
        console.log("ZIndexController");
    });

})();
