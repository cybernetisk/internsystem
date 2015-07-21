angular.module('cyb.varer').factory('VaretellingerItemNewVare', function () {
    return React.createClass({
        propTypes: {
            item: React.PropTypes.object.isRequired,
            ctrl: React.PropTypes.object.isRequired
        },
        removeMe: function () {
            this.props.item.remove();
        },
        saveMe: function (e) {
            e.preventDefault();
            this.props.item.store({
                antall: math.eval(this.refs.antall.getDOMNode().value.replace(",", ".")),
                antallpant: math.eval(this.refs.antallpant.getDOMNode().value.replace(",", ".")),
                kommentar: this.refs.kommentar.getDOMNode().value,
                sted: this.refs.sted.getDOMNode().value
            });
        },
        render: function () {
            return (
                <form className="form-inline" onSubmit={this.saveMe}>
                    <p>
                        <div className="form-group">
                            <input className="form-control" type="text" placeholder="Antall" ref="antall" required autoFocus />
                        </div>
                        {' '}
                        <div className="form-group">
                            <input className="form-control" type="text" placeholder="Antall hele" ref="antallpant" />
                        </div>
                        {' '}
                        <div className="form-group">
                            <input className="form-control telling-sted" type="text" placeholder="Sted" defaultValue={this.props.ctrl.newitem_place} ref="sted" required />
                        </div>
                    </p>
                    <p>
                        <div className="form-group">
                            <input className="form-control telling-kommentar" type="text" placeholder="Kommentar" ref="kommentar" />
                        </div>
                        {' '}
                        <div className="form-group">
                            <a className="btn btn-danger" onClick={this.removeMe}><i className="glyphicon glyphicon-remove"></i></a>
                        </div>
                        <input type="submit" />
                    </p>
                </form>
            );
        }
    });
});
