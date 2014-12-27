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

    module.controller('RåvarerController', function ($filter, $location, $scope, $stateParams, ParamsHelper, RåvarerService, VarerHelper) {
        var self = this;

        this.varefilter = {};
        var filter = function () {
            self.itemsfiltered = $filter('filter')(self.items, self.varefilter.text);
            if (self.varefilter.group) {
                self.itemsfiltered = self.itemsfiltered.filter(function (obj) {
                    return obj.innkjopskonto[self.varefilter.group.compare] == self.varefilter.group.compareValue;
                });
            }
        };
        $scope.$watchCollection('raavarer.varefilter', filter);

        var helper = ParamsHelper.track($scope,
            ['page'],
            {'raavarer.pagination.page': 'page'},
            function (params) {
                self.items = null;

                RåvarerService.getList(params).then(function (res) {
                    self.items = res.results;
                    self.pagination = res.pagination;

                    self.groups = VarerHelper.extractGroups(self.items, 'innkjopskonto');

                    filter();
                });
            }
        );

        helper.run();
    });
})();
