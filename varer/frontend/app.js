(function() {
    'use strict';

    var module = angular.module('cyb.varer', [
        'ui.router'
    ]);

    module.config(function ($locationProvider, $urlRouterProvider) {
        $locationProvider.html5Mode(true);

        $urlRouterProvider
            .when('/', '/varer')
            .otherwise(function() {
                console.log("unknown route");
            });
    })
})();
