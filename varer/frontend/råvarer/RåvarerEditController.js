(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('råvare.edit', {
            url: '/edit',
            templateUrl: require('./edit.html'),
            controller: 'RåvarerEditController as edit'
        });
    });

    module.controller('RåvarerEditController', function ($scope, $stateParams, RåvarerService) {
        console.log("RåvarerEditController", $stateParams);
        console.log("item:", $scope.item);
    });
})();
