(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.factory('SalgskalkylerService', function ($resource) {
        return $resource('api/salgskalkyler/:id/', {
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
