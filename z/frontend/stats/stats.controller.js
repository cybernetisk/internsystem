(function() {
    'use strict';

    var module = angular.module('cyb.z');

    module.config(function ($stateProvider) {
        $stateProvider.state('zstats', {
            url: '/z/stats',
            templateUrl: require('./index.html'),
            controller: 'ZStatsController'
        });
    });

    module.controller('ZStatsController', function () {
        console.log("ZStatsController");
    });

})();
