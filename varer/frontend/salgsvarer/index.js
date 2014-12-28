(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('salgsvarer', {
            url: '/varer/salgsvarer?q&group',
            templateUrl: 'views/varer/salgsvarer/index.html',
            controller: 'SalgsvarerController as salgsvarer',
            reloadOnSearch: false
        })
    });

    module.controller('SalgsvarerController', function ($filter, $scope, $stateParams, ParamsHelper, SalgsvarerService, VarerHelper) {
        var self = this;

        this.varefilter = {
            'text': $stateParams['q'],
            'group': $stateParams['group']
        };
        var filter = function () {
            if (!self.items) return;
            self.itemsfiltered = $filter('filter')(self.items, self.varefilter.text);
            if (self.varefilter.group) {
                var group = self.groups.filter(function (test) { return test.id == self.varefilter.group; })[0];
                self.itemsfiltered = self.itemsfiltered.filter(function (obj) {
                    return obj.salgskonto[group.compare] == group.compareValue;
                });
            }
        };
        $scope.$watchCollection('salgsvarer.varefilter', filter);

        var lastPage = -1;
        var helper = ParamsHelper.track($scope,
            ['page', 'q', 'group'],
            {
                'salgsvarer.pagination.page': 'page',
                'salgsvarer.varefilter.text': 'q',
                'salgsvarer.varefilter.group': 'group'
            },
            function (params) {
                if (lastPage == -1 || lastPage != params['page']) {
                    lastPage = params['page'];
                    self.items = null;

                    SalgsvarerService.getList({'page': params['page']}).then(function (res) {
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
                } else {
                    filter();
                }
            }
        );

        helper.run();
    });
})();
