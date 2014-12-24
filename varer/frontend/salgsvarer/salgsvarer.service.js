(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.factory('SalgsvarerService', function ($resource) {
        var obj = $resource('api/salgsvarer/:id/', {
            id: '@id'
        }, {
            query: {
                isArray: false,
                params: {
                    limit: 300
                }
            }
        });

        obj.getList = function (params) {
            return this.query(params).$promise.then(function (res) {
                res.result = res.results.map(function (item) {
                    // finn aktive innkjøpspriser
                    item.innpris = 0;
                    item.raavarer.forEach(function (meta) {
                        meta.innpris = null;
                        meta.innpris_accurate = 0;
                        meta.raavare.priser.forEach(function (pris) {
                            if (pris.aktiv && (!meta.raavare.innpris || pris.dato >= meta.raavare.innpris.dato)) {
                                meta.innpris = pris;
                                meta.innpris_accurate = pris.pris / meta.raavare.mengde * meta.mengde;
                            }
                        });
                        item.innpris += meta.innpris_accurate || 0;
                    });

                    // finn aktiv salgspris
                    item.salgspris = null;
                    item.priser.forEach(function (pris) {
                        if (pris.status != 'FOR' && (!item.salgspris || pris.dato >= item.salgspris.dato))
                            item.salgspris = pris;
                    });

                    return item;
                });

                return res;
            });
        };

        return obj;
    });
})();
