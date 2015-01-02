(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('råvare', {
            url: '/varer/råvarer/:id',
            templateUrl: 'views/varer/råvarer/item.html',
            controller: 'RåvarerItemController as item'
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
})();
