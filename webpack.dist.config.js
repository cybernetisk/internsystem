var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var ngAnnotatePlugin = require('ng-annotate-webpack-plugin');

module.exports = {
  cache: false,
  debug: false,
  devtool: false,

  stats: {
    colors: true,
    reasons: false
  },

  entry: [
    './siteroot/frontend/app.js'
  ],
  output: {
    path: __dirname + '/siteroot/static_build/',
    filename: 'bundle.js',
    publicPath: '/static/' // Tell django to use this URL to load packages and not use STATIC_URL + bundle_name
  },
  module: {
    loaders: [
      {test: /\.jsx?$/, exclude: /node_modules/, loaders: ['babel']},
      {test: /\.css$/, loader: 'style!css'},
      {test: /\.scss$/, loader: 'style!css!sass'},
      {test: /\.woff2?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "url-loader?limit=10000&minetype=application/font-woff"},
      {test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "file-loader"},
      {test: /\.html$/, loader: "ngtemplate?module=cyb.oko&relativeTo=" + (path.resolve(__dirname, './')) + "/!html"}
    ]
  },
  resolve: {
    modulesDirectories: ['node_modules'],
    extensions: ['', '.js', '.jsx'],
    alias: {
      //jquery: "jquery/src/jquery.js",
      mathjs: 'mathjs/dist/math.js',
    }
  },
  plugins: [
    new ngAnnotatePlugin({
      add: true,
      // other ng-annotate options here
    }),
		new webpack.optimize.DedupePlugin(),
    new webpack.optimize.UglifyJsPlugin(),
    new webpack.NoErrorsPlugin(),
    new BundleTracker({filename: './webpack-stats.json'}),

    // keeps hashes consistent between compilations
    new webpack.optimize.OccurenceOrderPlugin(),

    // removes a lot of debugging code in React
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('production')
      }}),
  ]
};
