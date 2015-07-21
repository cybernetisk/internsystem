/**
 * Check for directives in a React-element
 *
 * Usage:
 * <CompileDirective elm={<a ui-sref="demo">text</a>}></CompileDirective>
 *
 * NB: Currently bound to rootScope
 */
angular.module('cyb.varer').factory('CompileDirective', function ($compile, $rootScope) {
    return React.createClass({
        propTypes: {
            elm: React.PropTypes.node.isRequired
        },

        render: function () {
            return this.props.elm;
        },

        componentDidMount: function () {
            $compile(this.getDOMNode())($rootScope);
        },

        componentDidUpdate: function () {
            $compile(this.getDOMNode())($rootScope);
        }
    });
});
