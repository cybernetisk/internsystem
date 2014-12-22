(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.config(function ($stateProvider) {
        $stateProvider.state('råvarer', {
            url: '/varer/råvarer',
            templateUrl: 'views/varer/råvarer/index.html',
            controller: 'RåvarerController as raavarer'
        })
    });

    module.controller('RåvarerController', function ($scope, RåvarerService) {
        var self = this;
        console.log("RåvarerController");

        RåvarerService.query(function(res) {
            self.items = res.results.map(function(item) {
                // finn aktiv innkjøpspris
                item.innpris = null;
                item.priser.forEach(function (pris) {
                    if (!item.innpris || pris.dato >= item.innpris.dato)
                        item.innpris = pris;
                });

                // finn aktiv salgspris
                item.salgspris = null;
                if (item.lenket_salgsvare) {
                    item.lenket_salgsvare.priser.forEach(function (pris) {
                        if (!item.salgspris || pris.dato >= item.salgspris.dato)
                            item.salgspris = pris;
                    });
                }

                return item;
            });
        });
    });
})();
