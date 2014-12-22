(function() {
    'use strict';

    var module = angular.module('cyb.varer', [
        'ui.router',
        'ngResource'
    ]);

    module.config(function ($resourceProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
    });

})();
