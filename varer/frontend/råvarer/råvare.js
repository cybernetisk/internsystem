(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('råvare', {
            url: '/varer/råvarer/:id',
            templateUrl: 'views/varer/råvarer/item.html',
            controller: 'RåvarerItemController as item'
        });
        $stateProvider.state('råvare.edit', {
            url: '/edit',
            templateUrl: 'views/varer/råvarer/edit.html',
            controller: 'RåvarerEditController as edit'
        });
    });

    module.controller('RåvarerItemController', function ($scope, $stateParams, RåvarerService) {
        console.log("RåvarerItemController", $stateParams);
        var self = this;

        RåvarerService.get({id: $stateParams['id']}, function(res) {
            console.log(res);
            self.data = res;
        });
    });

    module.controller('RåvarerEditController', function ($scope, $stateParams, RåvarerService) {
        console.log("RåvarerEditController", $stateParams);
        console.log("item:", $scope.item);
    });
})();
