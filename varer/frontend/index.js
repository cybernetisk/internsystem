module.exports = 'cyb.varer';

(function() {
    'use strict';

    require('ngReact');

    var module = angular.module('cyb.varer', [
        require('ui.router'),
        require('angular-resource'),
        'react'
    ]);

    module.config(function ($resourceProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
    });

    require('./index/VarerIndexController');
    require('./common/CompileDirective');
    require('./common/prisdato.directive');
    require('./common/PrisDato');
    require('./common/prismargin.directive');
    require('./common/PrisMargin');
    require('./common/VareMengde');
    require('./common/VarerHelper');

    require('./kontoer/KontoerController');
    require('./kontoer/KontoerItemController');
    require('./kontoer/KontoerService');

    require('./leverandører/LeverandørerController');
    require('./leverandører/LeverandørerService');

    require('./råvarer/RåvarerController');
    require('./råvarer/RåvarerEditController');
    require('./råvarer/RåvarerIndexListView');
    require('./råvarer/RåvarerItemController');
    require('./råvarer/RåvarerService');

    require('./salgskalkyler/SalgskalkylerController');
    require('./salgskalkyler/SalgskalkylerService');

    require('./salgsvarer/SalgsvarerController');
    require('./salgsvarer/SalgsvarerIndexListView');
    require('./salgsvarer/SalgsvarerService');

    require('./varetellinger/VaretellingerController');
    require('./varetellinger/VaretellingerItemController');
    require('./varetellinger/VaretellingerItemListView');
    require('./varetellinger/VaretellingerItemNewVare');
    require('./varetellinger/VaretellingerService');
    require('./varetellinger/VaretellingVareService');

})();
