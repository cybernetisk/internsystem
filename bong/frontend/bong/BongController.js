(function() {
    'use strict';

    var module = angular.module('cyb.bong');

    module.config(function ($stateProvider) {
        $stateProvider.state('bong', {
            url: '/bong/:id',
            templateUrl: 'views/bong/bong/index.html',
            controller: 'BongController'
        });
    });

    module.controller('BongController', function () {
        console.log("BongController");
    });

})();
