angular.module('cyb.varer').directive('prismargin', function () {
    return {
        restrict: 'E',
        scope: {
            innPris: '=',
            utPris: '=',
            utMva: '='
        },
        replace: true,
        // TODO: fargelegge marginene
        template: '<span>{{::ctrl.margin}} %</span>',
        controller: function ($scope) {
            var eksmva = $scope.utPris / (1 + $scope.utMva/100);
            this.margin = (((eksmva - $scope.innPris) / eksmva) * 100).toFixed(1).toString().replace('.', ',');
        },
        controllerAs: 'ctrl'
    };
});
