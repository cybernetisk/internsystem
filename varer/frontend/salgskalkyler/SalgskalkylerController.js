(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('salgskalkyler', {
            url: '/varer/salgskalkyler',
            templateUrl: require('./index.html'),
            controller: 'SalgskalkylerController as salgskalkyler'
        })
    });

    module.controller('SalgskalkylerController', function ($scope, ParamsHelper, SalgskalkylerService) {
        var self = this;

        var helper = ParamsHelper.track($scope,
            ['page'],
            {'salgskalkyler.pagination.page': 'page'},
            function (params) {
                self.items = null;

                SalgskalkylerService.query(params, function (res) {
                    self.items = res.results;
                    self.pagination = res.pagination;
                });
            }
        );

        helper.run();
    });
})();
