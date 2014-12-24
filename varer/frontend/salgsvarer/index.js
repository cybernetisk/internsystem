(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('salgsvarer', {
            url: '/varer/salgsvarer',
            templateUrl: 'views/varer/salgsvarer/index.html',
            controller: 'SalgsvarerController as salgsvarer'
        })
    });

    module.controller('SalgsvarerController', function (ParamsHelper, SalgsvarerService, $scope) {
        var self = this;

        var helper = ParamsHelper.track($scope,
            ['page'],
            {'salgsvarer.pagination.page': 'page'},
            function (params) {
                self.items = null;

                SalgsvarerService.getList(params).then(function (res) {
                    self.items = res.results;
                    self.pagination = res.pagination;
                });
            }
        );

        helper.run();
    });
})();
