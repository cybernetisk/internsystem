var module = angular.module('cyb.varer');

module.config(function ($stateProvider) {
    $stateProvider.state('konto', {
        url: '/varer/kontoer/:id',
        templateUrl: require('./item.html'),
        controller: 'KontoerItemController as item'
    });
});

module.controller('KontoerItemController', function ($scope, $stateParams, KontoerService) {
    var self = this;

    KontoerService.get({id: $stateParams['id']}, function(res) {
        self.data = res;
    });
});
