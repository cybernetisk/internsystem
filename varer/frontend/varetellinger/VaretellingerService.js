(function() {
    'use strict';

    var module = angular.module('cyb.varer');

    module.factory('VaretellingerService', function ($resource) {
        var obj = $resource('api/varetellinger/:id/', {
            id: '@id'
        }, {
            query: {
                isArray: false,
                params: {
                    limit: 30
                }
            }
        });

        obj.makeSummer = function (parent) {
            this.count = 0;
            this.sum = 0;
            this.pant = 0;
            this.parent = parent;
            this.add = function (count, sum, pant) {
                this.count += count;
                this.sum += Math.round(sum*100)/100;
                this.pant += Math.round(pant*100)/100;
                if (this.parent) this.parent.add(count, sum, pant);
            };
            this.new = function () {
                return new obj.makeSummer(this);
            };
        };

        return obj;
    });
})();
