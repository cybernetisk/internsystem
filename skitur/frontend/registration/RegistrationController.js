(function() {
    'use strict';

    var module = angular.module('cyb.skitur');

    module.config(function ($stateProvider) {
        $stateProvider.state('skitur', {
            url: '/skitur/registration',
            templateUrl: 'views/skitur/registration/index.html',
            controller: 'SkiturRegistrationController'
        });
    });

    module.controller('SkiturRegistrationController', function () {
        console.log('SkiturRegistrationController');
    });
})();
