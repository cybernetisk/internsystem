var gulp = require('gulp'),
    gutil = require("gulp-util"),
    webpack = require('webpack'),
    WebpackDevServer = require('webpack-dev-server'),
    webpackConfigDev = require('./webpack.config.js'),
    webpackConfigDist = require('./webpack.dist.config.js');

var webpackBuild = function(callback, config, name) {
    webpack(config, function(err, stats) {
        if (err) throw new gutil.PluginError(name, err);
        gutil.log("["+name+"]", stats.toString({
           colors: true
        }));
        callback();
    });
};

gulp.task("webpack:build", function(callback) {
    webpackBuild(callback, webpackConfigDist, "webpack:build");
});

gulp.task("webpack:build-dev", function(callback) {
    webpackBuild(callback, webpackConfigDev, "webpack:build-dev");
});

gulp.task("webpack-dev-server", function(callback) {
    var webpackPort = 3000;
    var webpackHost = 'localhost:' + webpackPort;
    var djangoHost = 'localhost:8000';

    new WebpackDevServer(webpack(webpackConfigDev), {
        publicPath: 'http://' + webpackHost,
        contentBase: 'http://' + djangoHost
    }).listen(webpackPort, "localhost", function(err) {
        if (err) throw new gutil.PluginError("webpack-dev-server", err);
        gutil.log("[webpack-dev-server]", "Go to http://" + webpackHost + "/webpack-dev-server/index.html !");
    });
});

gulp.task('build', ['webpack:build']);
gulp.task('build-dev', ['webpack:build-dev']);
gulp.task('default', ['webpack-dev-server']);
