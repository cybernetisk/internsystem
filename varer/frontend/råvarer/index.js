(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('råvarer', {
            url: '/varer/råvarer?page',
            templateUrl: 'views/varer/råvarer/index.html',
            controller: 'RåvarerController as raavarer',
            reloadOnSearch: false
        })
    });

    module.controller('RåvarerController', function ($location, $scope, $stateParams, ParamsHelper, RåvarerService) {
        var self = this;

        var helper = ParamsHelper.track($scope,
            ['page'],
            {'raavarer.pagination.page': 'page'},
            function (params) {
                self.items = null;

                RåvarerService.getList(params).then(function (res) {
                    self.items = res.results;
                    self.pagination = res.pagination;
                });
            }
        );

        helper.run();
    });
})();
