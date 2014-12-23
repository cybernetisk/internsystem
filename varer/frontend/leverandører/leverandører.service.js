(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.factory('LeverandørerService', function ($resource) {
        return $resource('api/leverandører/:id/', {
            id: '@id'
        }, {
            query: {
                // no pagination
                isArray: true
            }
        });
    });
})();
