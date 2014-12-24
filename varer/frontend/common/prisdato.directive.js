angular.module('cyb.varer').directive('prisdato', function () {
    return {
        restrict: 'E',
        scope: {
            dato: '='
        },
        replace: true,
        template: '<span class="prisdato" ng-class="ctrl.class">{{::ctrl.dato}}</span>',
        controller: function ($scope) {
            var days = ((new Date)-(new Date($scope.dato)))/86400000;
            this.dato = $scope.dato;

            if (days < 0)
                this.class = 'prisdato-error';
            //else if (this.dato == '2000-01-01')
            //    this.class = 'prisdato-static';
            else if (days < 30)
                this.class = 'prisdato-age1';
            else if (days < 100)
                this.class = 'prisdato-age2';
            else if (days < 180)
                this.class = 'prisdato-age3';
            else if (days < 300)
                this.class = 'prisdato-age4';
            else if (days < 400)
                this.class = 'prisdato-age5';
            else
                this.class = 'prisdato-age6';

        },
        controllerAs: 'ctrl'
    };
});
