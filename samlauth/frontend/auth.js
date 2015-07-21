const angular = require('angular');

module.exports = 'cyb.auth';

(function() {
    'use strict';

    var module = angular.module('cyb.auth', [
        require('ui.router')
    ]);

    require('./profile/ProfileController');

    module.config(function($stateProvider) {
        $stateProvider.state('login', {
            url: '/login',
            template: 'Går til logg inn side',
            controller: function() {
                window.location.href = 'saml/?sso';
            }
        }).
        state('logout', {
            url: '/logout',
            template: 'Logger ut',
            controller: function() {
                window.location.href = 'saml/?slo';
            }
        });
    });

    module.run(function($rootScope, AuthService) {
        // create a global binding that can be used by templates
        $rootScope.AuthService = AuthService;
    });

    module.factory("AuthService", function($location) {
        var logged_in = window.logged_in;
        var user = window.user;
        var metadata = window.user_metadata; // SAML-data
        var roles = ['all']; // TODO: combine this in django somehow

        return {
            isLoggedIn: function() {
                return logged_in;
            },

            hasRole: function(role) {
                return roles.indexOf('all') != -1;
                // FIXME
                //return roles.indexOf(role) != -1;
            },

            getUser: function() {
                return user;
            },

            getMetadata: function () {
                return metadata;
            },

            requireUser: function() {
                if (!logged_in) {
                    window.location.href = '/saml/?sso&url='+encodeURIComponent($location.path());
                    return false;
                }
                return true;
            }
        };
    });

    module.factory("AuthRequireResolver", function($q, AuthService) {
        return $q(function(resolve, reject) {
            if (AuthService.requireUser()) {
                resolve();
            } else {
                reject();
            }
        });
    });
})();
