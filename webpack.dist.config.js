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

  entry: {
    'app': [
      './siteroot/frontend/app.js',
    ],
    'app_react': [
      './siteroot/frontend_react/app_react.js',
    ],
  },
  output: {
    path: __dirname + '/siteroot/static_build/',
    filename: '[name].js',
    publicPath: '/static/'
  },
  module: {
    loaders: [
      {test: /\.jsx?$/, exclude: /node_modules/, loaders: ['babel?stage=0']},
      {test: /\.css$/, loader: 'style!css'},
      {test: /\.scss$/, loader: 'style!css!sass'},
      {test: /\.woff2?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "url-loader?limit=10000&minetype=application/font-woff"},
      {test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "file-loader"},
      {test: /\.html$/, loader: "ngtemplate?module=cyb.oko&relativeTo=" + (path.resolve(__dirname, './')) + "/!html"},
      {test: /\.json$/, loader: 'json'},
    ]
  },
  externals: {
    angular: 'angular',
    'bootstrap-sass': '"bootstrap-sass"',
    'ui.router': '"ui.router"',
    'angular-resource': '"ngResource"',
    'angular-animate': '"ngAnimate"',
    jquery: 'jQuery',
    mathjs: 'mathjs',
    ngReact: 'ngReact',
    react: 'React',
  },
  resolve: {
    modulesDirectories: ['node_modules'],
    extensions: ['', '.js', '.jsx'],
  },
  plugins: [
    new ngAnnotatePlugin({
      add: true,
      // other ng-annotate options here
    }),
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.UglifyJsPlugin({sourceMap: false}),
    new webpack.NoErrorsPlugin(),
    new BundleTracker({filename: './webpack-stats.json'}),

    // keeps hashes consistent between compilations
    new webpack.optimize.OccurenceOrderPlugin(),

    // removes a lot of debugging code in React
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('production')
      }}),

    new webpack.optimize.CommonsChunkPlugin("common.js"),

    new webpack.DefinePlugin({
      DEBUG: false,
    }),
  ]
};
