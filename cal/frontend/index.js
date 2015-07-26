module.exports = 'cyb.cal';

(function() {
    'use strict';

    require('ngReact');

    var module = angular.module('cyb.cal', [
        require('ui.router'),
        require('angular-resource'),
        'react'
    ]);

    module.config(function ($resourceProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
    });

    require('./index/CalIndexController');
    require('./index/CalEventController');

})();
