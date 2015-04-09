(function() {
    'use strict';

    var module = angular.module('cyb.cal', [
        'ui.router',
        'ngResource',
        'react'
    ]);

    module.config(function ($resourceProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
    });

})();
