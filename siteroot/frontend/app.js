(function() {
    'use strict';

    var module = angular.module('cyb.oko', [
        'ui.router',
        'cyb.varer'
    ]);

    module.config(function ($locationProvider, $urlRouterProvider) {
        $locationProvider.html5Mode(true);

        $urlRouterProvider
            .otherwise(function() {
                console.log("unknown route");
            });
    })
})();
