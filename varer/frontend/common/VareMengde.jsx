angular.module('cyb.varer').factory('VareMengde', function ($filter) {
    return React.createClass({
        propTypes: {
            verdi: React.PropTypes.number.isRequired,
            enhet: React.PropTypes.string
        },

        render: function () {
            var verdi = this.props.verdi;
            var enhet = this.props.enhet;

            verdi = $filter('antall')(verdi);

            return (
                <span>{verdi}{enhet ? ' ' + enhet : ''}</span>
            );
        }
    });
});
