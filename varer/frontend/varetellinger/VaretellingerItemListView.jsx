angular.module('cyb.varer').factory('VaretellingerItemListView', function ($filter, PrisDato, VareMengde, VaretellingerItemNewVare) {
  return React.createClass({
    propTypes: {
      raavarerfiltered: React.PropTypes.array.isRequired,
      vis_varer: React.PropTypes.string.isRequired,
      newItem: React.PropTypes.func.isRequired,
      newitems: React.PropTypes.object.isRequired
    },
    render: function () {
      var self = this;
      var gruppe = null;
      return (
        <table className="table table-condensed table-striped varer-table">
          <thead>
            <tr>
              <th>Betegnelse</th>
              <th>Mengde</th>
              <th>Pris eks mva</th>
              <th>Tellinger</th>
            </tr>
          </thead>
          <tbody>
            {this.props.raavarerfiltered.reduce(function (prev, raavare) {
              if (gruppe != raavare.innkjopskonto) {
                gruppe = raavare.innkjopskonto;

                var showGroupLabel = self.props.vis_varer != 'TELLING' || gruppe.summer.count > 0;
                if (showGroupLabel) {
                  prev.push((
                    <tr className="group-row" key={'gruppe-' + gruppe.id}>
                      <th colSpan="3">{gruppe.gruppe}: <a className="gruppe-link" href={'varer/kontoer/'+gruppe.id}>{gruppe.navn}</a></th>
                      <th>
                        {$filter('price')(gruppe.summer.sum, 2)} + {$filter('price')(gruppe.summer.pant, 2)} i pant
                      </th>
                    </tr>
                  ));
                }
              }

              if (self.props.vis_varer != 'GRUPPER') {
                if (self.props.vis_varer != 'ALT' && raavare.tellinger.length == 0 && !self.props.newitems[raavare.id]) return prev;

                var newItemEvent = self.props.newItem.bind(null, raavare);

                prev.push((
                    <tr key={'raavare-' + raavare.id}>
                      <td>
                        {raavare.kategori ? raavare.kategori + ': ' : ''}
                        <a href={'varer/råvarer/'+raavare.id}>{raavare.navn}</a>
                        {raavare.status != 'OK' ? <span> <span className="status-text">{raavare.status}</span></span> : ''}
                      </td>
                      <td>
                        <VareMengde verdi={raavare.mengde} enhet={raavare.enhet} />
                        {raavare.antall != 1 ? <span className="vare-antall"><br />
                          ({raavare.antall} stk)
                        </span> : ''}
                        {raavare.mengde_svinn ? <span className="svinn-info"><br/>
                          ca. <VareMengde verdi={raavare.mengde_svinn} enhet={raavare.enhet} /> = svinn
                        </span> : ''}
                      </td>
                      <td>
                        {raavare.innpris ?
                        <span>
                          {$filter('price')(raavare.innpris.pris)}
                          {raavare.innpris.pant ? <span className="pris-pant"><br/>
                            + {$filter('price')(raavare.innpris.pant)} i pant
                          </span> : ''}<br />
                          <PrisDato dato={raavare.innpris.dato} />
                        </span> : ''}
                      </td>
                      <td>
                        <div className="tellinger">
                          <ul>
                            {raavare.tellinger.map(function (telling) {
                              return (
                                <li key={'telling-'+telling.id}>
                                  <a href={'admin/varer/varetellingvare/' + telling.id + '/'} target="_self">
                                    {$filter('antall')(telling.antall)}{' '}
                                    ({$filter('price')(telling.summer.sum)}{telling.summer.pant != 0 ? <span> + {$filter('price')(telling.summer.pant)} {telling.antallpant ? <span>({telling.antallpant})</span> : ''} i pant</span> : ''}){' '}
                                    {telling.kommentar} ({telling.sted})
                                  </a>
                                </li>
                              );
                            })}
                            {(self.props.newitems[raavare.id]||[]).map(function (item) {
                              return (
                                  <li>
                                    <VaretellingerItemNewVare item={item} ctrl={self.props} />
                                  </li>
                              );
                            })}
                          </ul>
                          <span className="nytelling"><a onClick={newItemEvent}><i className="glyphicon glyphicon-plus" /></a></span>
                        </div>
                      </td>
                    </tr>));
              }

              return prev;
            }, [])}
          </tbody>
        </table>);
    }
  });
});
