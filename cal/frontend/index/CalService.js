angular.module('cyb.cal').factory('CalService', function ($resource) {
    return $resource('api/cal/events/:id/', {
        id: '@id'
    }, {
        query: {
            // no pagination
            isArray: true
        }
    });
});
