angular.module('cyb.varer').factory('VarerHelper', function () {
    return {
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
        }
    }
});
