'use strict';

module.exports = 'cyb.z';

angular.module('cyb.z', [
  require('ui.router')
]);

require('./index/index.controller.js');
require('./stats/stats.controller.js');
