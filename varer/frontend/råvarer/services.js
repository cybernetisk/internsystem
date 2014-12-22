(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.factory('RåvarerService', function ($resource) {
        return $resource('api/råvarer/:id/', {
            id: '@id'
        }, {
            query: {
                isArray: false
            }
        });
    });
})();
