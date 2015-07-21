(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('råvare', {
            url: '/varer/råvarer/:id',
            templateUrl: require('./item.html'),
            controller: 'RåvarerItemController as item'
        });
    });

    module.controller('RåvarerItemController', function ($scope, $stateParams, $window, RåvarerService) {
        $window.location.href = '/admin/varer/råvare/' + parseInt($stateParams['id']) + '/';
        return;

        console.log("RåvarerItemController", $stateParams);
        var self = this;

        RåvarerService.get({id: $stateParams['id']}, function(res) {
            console.log(res);
            self.data = res;
        });
    });
})();
