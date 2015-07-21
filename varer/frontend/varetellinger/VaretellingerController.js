(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('varetellinger', {
            url: '/varer/varetellinger',
            templateUrl: require('./index.html'),
            controller: 'VaretellingerController as varetellinger'
        })
    });

    module.controller('VaretellingerController', function ($scope, ParamsHelper, VaretellingerService) {
        var self = this;

        var helper = ParamsHelper.track($scope,
            ['page'],
            {'salgskalkyler.pagination.page': 'page'},
            function (params) {
                self.items = null;

                VaretellingerService.query(params, function (res) {
                    self.items = res.results;
                    self.pagination = res.pagination;
                });
            }
        );

        helper.run();
    });
})();
