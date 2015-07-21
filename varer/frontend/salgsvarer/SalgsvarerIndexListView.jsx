angular.module('cyb.varer').factory('SalgsvarerIndexListView', function ($compile, $filter, PrisDato, PrisMargin, VareMengde) {
    return React.createClass({
        propTypes: {
            itemsfiltered: React.PropTypes.array.isRequired
        },
        render: function () {
            var lastGroup = null;
            return (
                <table className="table table-striped table-condensed varer-table">
                    <thead>
                        <tr>
                            <th>Navn</th>
                            <th>Kasse#</th>
                            <th>Intern</th>
                            <th>Ekstern</th>
                            <th>Råvarer (priser eks mva)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.props.itemsfiltered.reduce(function (prev, item) {
                            if (lastGroup != item.salgskonto.gruppe) {
                                lastGroup = item.salgskonto.gruppe;
                                prev.push((
                                    <tr className="group-row" key={item.salgskonto.gruppe}>
                                        <th colSpan="5">{item.salgskonto.gruppe}</th>
                                    </tr>
                                ));
                            }

                            prev.push((
                                <tr key={item.id}>
                                    <td>
                                        {item.kategori ? item.kategori + ': ' : ''}
                                        {/*<a ui-sref="salgsvare({id:item.id})">{item.navn}</a>*/}
                                        <a href={'admin/varer/salgsvare/' + item.id + '/'} target="_self">{item.navn}</a>
                                        {item.status != 'OK' ? <span> <span className="status-text">{item.status}</span></span> : ''}
                                        <br/>
                                        <a className="gruppe-link" href={'admin/kontoer/'+item.salgskonto.id} title={item.salgskonto.navn}>{item.salgskonto.navn}</a>
                                    </td>
                                    <td>{item.kassenr}</td>
                                    <td>
                                        {item.salgspris && item.salgspris.pris_intern ?
                                            <span>
                                                {$filter('price')(item.salgspris.pris_intern, 0)}
                                                {item.innpris ?
                                                    <span>
                                                        <br/>
                                                        <PrisMargin innPris={item.innpris} utPris={item.salgspris.pris_intern} utMva={item.salgspris.mva} />
                                                    </span> : ''}
                                            </span> : 'Se ekstern'}
                                    </td>
                                    <td>
                                        {item.salgspris && item.salgspris.pris_ekstern ?
                                            <span>
                                                {$filter('price')(item.salgspris.pris_ekstern, 0)}
                                                {item.innpris ?
                                                    <span>
                                                        <br/>
                                                        <PrisMargin innPris={item.innpris} utPris={item.salgspris.pris_ekstern} utMva={item.salgspris.mva} />
                                                    </span> : ''}
                                            </span> : 'Ikke salg'}
                                    </td>
                                    <td>
                                        <ul>
                                            {item.raavarer.map(function (meta) {
                                                return (
                                                    <li key={meta.id}>
                                                        {/*<span ng-show="::meta.raavare.kategori">{meta.raavare.kategori}: </span>*/}
                                                        {/*<span ng-if="meta.mengde == meta.raavare.mengde">1 stk</span>*/}
                                                        {meta.mengde != meta.raavare.mengde ? <span><VareMengde verdi={meta.mengde} enhet={meta.raavare.enhet} /> </span> : ''}
                                                        <a href={'varer/råvarer/'+meta.raavare.id}>{meta.raavare.navn}</a>

                                                        {meta.innpris ? <span>
                                                            &nbsp;({$filter('price')(meta.innpris_accurate)} <PrisDato dato={meta.innpris.dato} />)
                                                        </span> : ''}
                                                    </li>);
                                            })}
                                        </ul>
                                    </td>
                                </tr>));

                            return prev;
                        }, [])}
                    </tbody>
                </table>
            );
        }
    });
});
