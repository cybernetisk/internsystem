(function() {
    'use strict';

    const indexTemplate = require('./index.html');

    var module = angular.module('cyb.oko');

    module.config(function ($stateProvider) {
        $stateProvider.state('index', {
            url: '/',
            templateUrl: indexTemplate,
            controller: 'IndexController'
        });
    });

    module.controller('IndexController', function () {
        console.log("IndexController");
    });

})();
