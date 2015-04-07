(function () {
    'use strict';

    angular.module('cyb.bong')
        .controller('Bong', Bong);

    function Bong() {
        var vm = this;
        vm.test = 'bongolongo';
        console.log('titt tei');
    }
})();