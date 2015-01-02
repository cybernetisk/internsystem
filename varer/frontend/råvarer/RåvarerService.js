(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.factory('RåvarerService', function ($resource, VarerHelper) {
        var obj = $resource('api/råvarer/:id/', {
            id: '@id'
        }, {
            query: {
                isArray: false,
                params: {
                    limit: 300
                }
            }
        });

        obj.getList = function (params, priceDate) {
            if (priceDate) {
                priceDate = new Date(priceDate);
                priceDate.setUTCHours(0, 0, 0);
            }

            return this.query(params).$promise.then(function (res) {
                res.results = res.results.sort(VarerHelper.getSorter('innkjopskonto'));

                res.results = res.results.map(function (item) {
                    // finn aktiv innkjøpspris
                    item.innpris = null;
                    item.priser.forEach(function (pris) {
                        if (pris.aktiv && (!item.innpris || pris.dato >= item.innpris.dato))
                            item.innpris = pris;
                    });

                    // finn aktiv salgspris
                    item.salgspris = null;
                    var itemDate = null;
                    if (item.lenket_salgsvare) {
                        item.lenket_salgsvare.priser.forEach(function (pris) {
                            if (pris.status == 'FOR') return;

                            var xDate = new Date(pris.dato);
                            xDate.setUTCHours(0, 0, 0);

                            if (priceDate && xDate > priceDate) return;
                            if (item.salgspris && itemDate > xDate) return;

                            item.salgspris = pris;
                            itemDate = xDate;
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
