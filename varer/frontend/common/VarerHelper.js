angular.module('cyb.varer').factory('VarerHelper', function ($filter) {
    var VarerHelper = {
        /**
         * Hent ut liste over grupper beregnet for <select>
         */
        extractGroups: function (items, groupKey) {
            var groupCount = {};

            return items.reduce(function (prev, cur) {
                if (!prev.some(function (obj) {
                        return obj.id == cur[groupKey].id;
                    })) {
                    groupCount[cur[groupKey].gruppe] = (groupCount[cur[groupKey].gruppe] || 0) + 1;
                    prev.push(cur[groupKey]);
                }
                return prev;
            }, []).sort(function (left, right) {
                return left.gruppe == right.gruppe
                    ? left.navn.localeCompare(right.navn)
                    : left.gruppe.localeCompare(right.gruppe);
            }).reduce(function (prev, cur) {
                if ((prev.length == 0 || prev[prev.length-1].gruppe != cur.gruppe) && groupCount[cur.gruppe] > 1) {
                    prev.push({
                        id: cur.gruppe,
                        compare: 'gruppe',
                        compareValue: cur.gruppe,
                        gruppe: cur.gruppe,
                        navn: cur.gruppe + ' (alt)'
                    });
                }
                prev.push({
                    id: cur.id,
                    compare: 'id',
                    compareValue: cur.id,
                    gruppe: cur.gruppe,
                    navn: cur.navn
                });
                return prev;
            }, []);
        },

        /**
         * Filtrering av varer
         */
        createFilter: function (scope, filters, filtergroup, kontonavn, input, output) {
            var run = function () {
                var items = input();
                if (!items) return;
                var g = VarerHelper.extractGroups(items, kontonavn);

                var res = $filter('filter')(items, filters.text);
                if (filters.group) {
                    var group = g.filter(function (test) { return test.id == filters.group; })[0];
                    res = res.filter(function (obj) {
                        return obj[kontonavn][group.compare] == group.compareValue;
                    });
                }

                output(res);
            };

            scope.$watchCollection(filtergroup, run);

            return run;
        },

        /**
         * Sortering av råvarer/salgsvarer
         */
        getSorter: function (kontoname, subGroup) {
            return function (left, right) {
                if (left[kontoname].gruppe != right[kontoname].gruppe)
                    return left[kontoname].gruppe.localeCompare(right[kontoname].gruppe);

                if (subGroup && left[kontoname].navn != right[kontoname].navn)
                    return left[kontoname].navn.localeCompare(right[kontoname].navn);

                if (left.kategori != right.kategori && left.kategori != null && right.kategori != null)
                    return left.kategori.localeCompare(right.kategori);

                return left.navn.localeCompare(right.navn);
            };
        }
    };

    return VarerHelper;
});
