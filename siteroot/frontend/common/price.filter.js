angular.module('cyb.oko').filter('price', function() {
    return function(amount, decimals, in_nok) {
        if (typeof decimals == 'boolean') {
            in_nok = decimals;
            decimals = 0;
        }

        decimals = decimals || 0;

        if (decimals == 0 && amount.toFixed(0) != amount) {
            decimals = 2;
        }

        var formatNumber = function(number, decimals)
        {
            number = number.toFixed(decimals) + '';
            var x = number.split('.');
            var x1 = x[0];
            var x2 = x.length > 1 ? ',' + x[1] : '';
            var rgx = /(\d+)(\d{3})/;
            while (rgx.test(x1)) {
                x1 = x1.replace(rgx, '$1' + ' ' + '$2');
            }
            return x1 + x2;
        };

        if (typeof(decimals) != "number") decimals = 0;
        return (in_nok ? 'NOK ' : 'kr ') + formatNumber(parseFloat(amount), decimals);
    };
});
