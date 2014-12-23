(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.factory('SalgsvarerService', function ($resource) {
        return $resource('api/salgsvarer/:id/', {
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
