angular.module('cyb.varer').factory('KontoerService', function ($resource) {
    return $resource('api/kontoer/:id/', {
        id: '@id'
    }, {
        query: {
            // no pagination
            isArray: true
        }
    });
});
