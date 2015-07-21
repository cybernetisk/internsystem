const paginationTemplate = require('./pagination.html');

angular.module('cyb.oko').directive('pagination', function () {
    return {
        restrict: 'E',
        scope: {
            'data': '='
        },
        templateUrl: paginationTemplate,
        link: function (scope) {
            scope.changePage = function(to) {
                if (to < 1 || to > scope.data.pages) return;
                scope.data.page = to;
            };
        }
    };
});
