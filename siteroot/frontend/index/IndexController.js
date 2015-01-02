(function() {
    'use strict';

    var module = angular.module('cyb.oko');

    module.config(function ($stateProvider) {
        $stateProvider.state('index', {
            url: '/',
            templateUrl: 'views/siteroot/index/index.html',
            controller: 'IndexController'
        });
    });

    module.controller('IndexController', function () {
        console.log("IndexController");
    });

})();
