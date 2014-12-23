(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.factory('VaretellingerService', function ($resource) {
        return $resource('api/varetellinger/:id/', {
            id: '@id'
        }, {
            query: {
                isArray: false,
                params: {
                    limit: 30
                }
            }
        });
    });
})();
