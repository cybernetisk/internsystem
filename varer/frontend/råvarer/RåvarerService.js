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
                    // velg siste prisen før prisdato, evt. første pris tilgjengelig etter
                    var existing_date = null;
                    var existing_date_valid = null;
                    item.innpris = null;
                    item.priser.forEach(function (pris) {
                        if (!pris.aktiv) return;

                        // ingen pris: legg til uansett
                        // eksisterende egentlig ugyldig, ny er tidligere => erstatt
                        // begge er gyldige, ny har senere dato => erstatt

                        var current_date = new Date(pris.dato);
                        var current_date_valid = !priceDate ? true : current_date <= priceDate;

                        // hopp kun over pris dersom det allerede eksisterer en
                        if (item.innpris) {
                            // hvis eksisterende pris er før ønsket dato, ikke tillatt ugyldig dato eller eldre dato
                            if (existing_date_valid) {
                                if (!current_date_valid) return;
                                if (current_date <= existing_date) return;
                            }

                            // hvis eksisterende pris er etter ønsket dato, ikke tillatt enda nyere dato
                            else {
                                if (current_date >= existing_date) return;
                            }
                        }

                        item.innpris = pris;
                        existing_date = current_date;
                        existing_date_valid = current_date_valid;
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
