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
        template: '<span class="prismargin" ng-class="ctrl.class">{{::ctrl.margin}} %</span>',
        controller: function ($scope) {
            var eksmva = $scope.utPris / (1 + $scope.utMva/100);
            var margin = (((eksmva - $scope.innPris) / eksmva) * 100);

            this.margin = margin.toFixed(1).toString().replace('.', ',');

            if (margin > 150)
                this.class = 'prismargin-veryhigh';
            else if (margin > 100)
                this.class = 'prismargin-higher';
            else if (margin > 50)
                this.class = 'prismargin-high';
            else if (margin > 20)
                this.class = 'prismargin-ok';
            else if (margin > 10)
                this.class = 'prismargin-low';
            else if (margin < 0)
                this.class = 'prismargin-subzero';
            else
                this.class = 'prismargin-verylow';
        },
        controllerAs: 'ctrl'
    };
});
