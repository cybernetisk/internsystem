(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('råvarer', {
            url: '/varer/råvarer?q&group',
            templateUrl: 'views/varer/råvarer/index.html',
            controller: 'RåvarerController as raavarer',
            reloadOnSearch: false
        })
    });

    module.controller('RåvarerController', function ($filter, $location, $scope, $stateParams, ParamsHelper, RåvarerService, VarerHelper) {
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
                    return obj.innkjopskonto[group.compare] == group.compareValue;
                });
            }
        };
        $scope.$watchCollection('raavarer.varefilter', filter);

        var lastPage = -1;
        var helper = ParamsHelper.track($scope,
            ['page', 'q', 'group'],
            {
                'raavarer.pagination.page': 'page',
                'raavarer.varefilter.text': 'q',
                'raavarer.varefilter.group': 'group'
            },
            function (params) {
                if (lastPage == -1 || lastPage != params['page']) {
                    lastPage = params['page'];
                    self.items = null;

                    RåvarerService.getList({'page': params['page']}).then(function (res) {
                        self.items = res.results.sort(function (left, right) {
                            return left.innkjopskonto.gruppe == right.innkjopskonto.gruppe
                                ? (left.kategori == right.kategori || left.kategori == null || right.kategori == null
                                    ? left.navn.localeCompare(right.navn)
                                    : left.kategori.localeCompare(right.kategori))
                                : left.innkjopskonto.gruppe.localeCompare(right.innkjopskonto.gruppe);
                        });

                        self.pagination = res.pagination;
                        self.groups = VarerHelper.extractGroups(self.items, 'innkjopskonto');

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
