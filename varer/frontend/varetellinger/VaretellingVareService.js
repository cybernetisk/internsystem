(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.factory('VaretellingVareService', function ($resource) {
        var obj = $resource('api/varetellingvarer/:id/', {
            id: '@id'
        }, {
            query: {
                isArray: false,
                params: {
                    limit: 30
                }
            }
        });

        return obj;
    });
})();
