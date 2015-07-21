(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('råvarer', {
            url: '/varer/råvarer?q&group',
            templateUrl: require('./index.html'),
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

        var filter = VarerHelper.createFilter(
            $scope,
            self.varefilter,
            'raavarer.varefilter',
            'innkjopskonto',
            function () { return self.items; },
            function (res) { self.itemsfiltered = res; }
        );

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
                        self.items = res.results;
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
