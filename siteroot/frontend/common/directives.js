(function() {
    'use strict';

    var module = angular.module('cyb.oko');

    /**
     * Set .active on menu elements when state change
     */
    module.directive('navbarCheckActive', function ($state) {
        return {
            restrict: 'A',
            link: function (scope, element) {
                scope.$on('$stateChangeSuccess', function () {
                    element.find('.active').removeClass("active");
                });
                element.find('a[ui-sref]').each(function () {
                    var state = $(this).attr('ui-sref');
                    var elms = $(this).closest('li').add($(this).parents('li.dropdown'));
                    scope.$on('$stateChangeSuccess', function () {
                        if ($state.includes(state)) {
                            elms.addClass('active');
                        }
                    });
                });
            }
        };
    });
})();
