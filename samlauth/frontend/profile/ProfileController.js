(function() {
    'use strict';

    var module = angular.module('cyb.auth');

    module.config(function ($stateProvider) {
        $stateProvider.state('profile', {
            url: '/profile',
            templateUrl: 'views/samlauth/profile/index.html',
            controller: 'AuthProfileController as ctrl'
        });
    });

    module.controller('AuthProfileController', function (AuthService) {
        console.log("AuthProfileController");

        this.is_authed = AuthService.isLoggedIn();
        if (this.is_authed) {
            this.user = AuthService.getUser();
            this.metadata = AuthService.getMetadata();
        }
    });

})();
