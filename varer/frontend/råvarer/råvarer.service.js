(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.factory('RåvarerService', function ($resource) {
        var obj = $resource('api/råvarer/:id/', {
            id: '@id'
        }, {
            query: {
                isArray: false,
                params: {
                    limit: 30
                }
            }
        });

        obj.getList = function (params) {
            return this.query(params).$promise.then(function (res) {
                res.result = res.results.map(function (item) {
                    // finn aktiv innkjøpspris
                    item.innpris = null;
                    item.priser.forEach(function (pris) {
                        if (pris.aktiv && (!item.innpris || pris.dato >= item.innpris.dato))
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

                return res;
            });
        };

        return obj;
    });
})();
