const loaderTemplate = require('./loader.html');

/**
 * Set loading message if variables is null
 */
var module = angular.module('cyb.oko').directive('loader', function () {
    return {
        restrict: 'E',
        scope: {
            var: '='
        },
        templateUrl: loaderTemplate,
        transclude: true
    };
});
