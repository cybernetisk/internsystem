(function() {
    'use strict';

    require('./app.scss');

    window.jQuery = window.$ = require('jquery');
    window.React = require('react');
    window.angular = require('angular');
    require('bootstrap-sass');
    window.math = require('mathjs');

    var module = angular.module('cyb.oko', [
        require('ui.router'),
        require('../../varer/frontend/'),
        require('../../z/frontend/'),
        require('../../samlauth/frontend/'),
    ]);

    module.config(function ($locationProvider, $urlRouterProvider, $httpProvider) {
        $locationProvider.html5Mode(true);

        $urlRouterProvider
            .otherwise(function() {
                console.log("unknown route");
            });

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });

    require('./common/antall.filter');
    require('./common/directives');
    require('./common/loader.directive');
    require('./common/pagination.directive');
    require('./common/ParamsHelper');
    require('./common/price.filter');
})();
