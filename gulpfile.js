var concat = require('gulp-concat'),
    gulp = require('gulp'),
    gutil = require("gulp-util"),
    uglify = require('gulp-uglify'),
    webpack = require('webpack'),
    WebpackDevServer = require('webpack-dev-server'),
    webpackConfigDev = require('./webpack.config.js'),
    webpackConfigDist = require('./webpack.dist.config.js');

var js_files_library = [
    'node_modules/jquery/dist/jquery.min.js',
    'node_modules/bootstrap-sass/assets/javascripts/bootstrap.min.js',
    'node_modules/angular/angular.min.js',
    'node_modules/angular-ui-router/release/angular-ui-router.min.js',
    'node_modules/angular-animate/angular-animate.min.js',
    'node_modules/angular-resource/angular-resource.min.js',
    'node_modules/react/dist/react.js',
    'node_modules/ngreact/ngReact.min.js',
    'node_modules/mathjs/dist/math.min.js'
];

gulp.task('scripts-library', function() {
    return gulp.src(js_files_library)
        .pipe(concat('library.js'))
        //.pipe(uglify())
        .pipe(gulp.dest('siteroot/static_build'));
});

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

    webpackConfigDev.output.publicPath = 'http://localhost:3000/siteroot/static_build/';

    new WebpackDevServer(webpack(webpackConfigDev), {
        hot: true,
        inline: true,
        publicPath: webpackConfigDev.output.publicPath,
        contentBase: 'http://' + djangoHost
    }).listen(webpackPort, "localhost", function(err) {
        if (err) throw new gutil.PluginError("webpack-dev-server", err);
        gutil.log("[webpack-dev-server]", "Go to http://" + webpackHost + "/webpack-dev-server/index.html !");
    });
});

gulp.task('build', ['webpack:build', 'scripts-library']);
gulp.task('build-dev', ['webpack:build-dev', 'scripts-library']);
gulp.task('default', ['webpack-dev-server', 'scripts-library']);
