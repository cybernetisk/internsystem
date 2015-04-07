(function () {
    'use strict';

    angular.module('cyb.bong')
        .config(function ($stateProvider) {
            $stateProvider.state('bong', {
                url: '/bong/:id',
                templateUrl: 'views/bong/bong/index.html',
                controller: 'BongController',
                controllerAs: 'bong'
            });
        });
})();
