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

    module.controller('SalgsvarerController', function ($filter, $scope, ParamsHelper, SalgsvarerService, VarerHelper) {
        var self = this;

        this.varefilter = {};
        var filter = function () {
            self.itemsfiltered = $filter('filter')(self.items, self.varefilter.text);
            if (self.varefilter.group) {
                self.itemsfiltered = self.itemsfiltered.filter(function (obj) {
                    return obj.salgskonto[self.varefilter.group.compare] == self.varefilter.group.compareValue;
                });
            }
        };
        $scope.$watchCollection('salgsvarer.varefilter', filter);

        var helper = ParamsHelper.track($scope,
            ['page'],
            {'salgsvarer.pagination.page': 'page'},
            function (params) {
                self.items = null;

                SalgsvarerService.getList(params).then(function (res) {
                    self.items = res.results.sort(function (left, right) {
                        return left.salgskonto.gruppe == right.salgskonto.gruppe
                            ? (left.kategori == right.kategori || left.kategori == null || right.kategori == null
                                ? left.navn.localeCompare(right.navn)
                                : left.kategori.localeCompare(right.kategori))
                            : left.salgskonto.gruppe.localeCompare(right.salgskonto.gruppe);
                    });

                    self.pagination = res.pagination;
                    self.groups = VarerHelper.extractGroups(self.items, 'salgskonto');

                    filter();
                });
            }
        );

        helper.run();
    });
})();
