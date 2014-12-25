angular.module('cyb.varer').factory('RåvarerIndexListView', function ($filter, PrisDato, PrisMargin) {
    return React.createClass({
        render: function () {
            // TODO: filter: ng-repeat="item in raavarer.items|filter:raavarer.varefilter"
            return (
                <table className="table table-condensed table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Betegnelse</th>
                            <th>Mengde</th>
                            <th>Svinn</th>
                            <th>Status</th>
                            <th>Gruppe</th>
                            <th className="text-right">Pris ex mva</th>
                            <th className="text-center">Pris intern/ekstern</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.props.items.map(function (item) {
                            return (
                                <tr key={item.id}>
                                    <td>{item.id}</td>
                                    <td>
                                        {item.kategori ? item.kategori + ' ' : ''}
                                        <a ui-sref={'råvare({id:'+item.id+'})'}>{item.navn}</a>
                                    </td>
                                    <td>{item.mengde} {item.enhet}</td>
                                    <td>
                                        {item.mengde_svinn ? <span>
                                            {item.mengde_svinn} {item.enhet}
                                        </span> : ''}
                                    </td>
                                    <td>{item.status}</td>
                                    <td>
                                        <a ui-sref="konto(\{id:{item.innkjopskonto.id}\})">{item.innkjopskonto.navn}</a><br/>
                                        {item.innkjopskonto.gruppe}
                                    </td>
                                    <td className="text-right">
                                        {item.innpris ?
                                            <span>
                                                {$filter('price')(item.innpris.pris, 2)} (<PrisDato dato={item.innpris.dato} />)
                                            </span> : ''}
                                    </td>
                                    <td className="text-center">
                                        {item.salgspris ?
                                            <span>
                                                {item.salgspris.pris_intern} / {item.salgspris.pris_ekstern}
                                                <span ng-show="item.innpris">
                                                    <br/>
                                                    (<PrisMargin innPris={item.innpris.pris} utPris={item.salgspris.pris_intern} utMva={item.salgspris.mva} />
                                                &nbsp;/&nbsp;
                                                    <PrisMargin innPris={item.innpris.pris} utPris={item.salgspris.pris_ekstern} utMva={item.salgspris.mva} />
                                                </span>
                                            </span> : ''}
                                    </td>
                                </tr>);
                        })}
                    </tbody>
                </table>);
        }
    });
});
