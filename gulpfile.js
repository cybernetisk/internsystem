var gulp = require('gulp'),
    sass = require('gulp-sass'),
    sourcemaps = require('gulp-sourcemaps'),
    uglify = require('gulp-uglify'),
    concat = require('gulp-concat'),
    ngAnnotate = require('gulp-ng-annotate'),
    gulpif = require('gulp-if'),
    args = require('yargs').argv,
    templates = require('gulp-angular-templatecache'),
    minifyHTML = require('gulp-minify-html'),
    rename = require('gulp-rename'),
    rev = require('gulp-rev'),
    buffer = require('gulp-buffer'),
    extend = require('gulp-extend'),
    runSequence = require('run-sequence'),
    minifyCSS = require('gulp-minify-css'),
    react = require('gulp-react');

// run with --production to do more compressing etc
var isProd = !!args.production;

var js_files_library = [
    'bower_components/jquery/dist/jquery.js',
    'bower_components/bootstrap-sass-official/assets/javascripts/bootstrap.js',
    'bower_components/angular/angular.js',
    'bower_components/angular-ui-router/release/angular-ui-router.min.js',
    'bower_components/angular-animate/angular-animate.js',
    'bower_components/angular-resource/angular-resource.js',
    'bower_components/react/react.js',
    'bower_components/ngReact/ngReact.js',
    'bower_components/mathjs/dist/math.js'
];

var js_files = [
    'varer/frontend/app.js',
    'varer/frontend/**/module.js',
    'varer/frontend/**/*.js',
    'z/frontend/app.js',
    'z/frontend/**/module.js',
    'z/frontend/**/*.js',
    'samlauth/frontend/app.js',
    'samlauth/frontend/**/module.js',
    'samlauth/frontend/**/*.js',
    'siteroot/frontend/app.js',
    'siteroot/frontend/**/module.js',
    'siteroot/frontend/**/*.js'
];

var jsx_files = [
    'varer/frontend/**/*.jsx'
];

var css_files = [
    'siteroot/frontend/app.scss'
];

var processScripts = function (files, name, isJsx) {
    return gulp.src(files)
        .pipe(sourcemaps.init())
        .pipe(concat(name + '.js'))
        .pipe(gulpif(isJsx, react()))
        .pipe(gulpif(isProd, ngAnnotate()))
        .pipe(gulpif(isProd, uglify()))
        .pipe(buffer())
        .pipe(rev())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('siteroot/static_build'))
        .pipe(rev.manifest({path: 'rev-manifest-scripts-' + name + '.json'}))
        .pipe(gulp.dest('siteroot/static_build'));
};

gulp.task('styles', function() {
    return gulp.src(css_files)
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(concat('frontend.css'))
        .pipe(gulpif(isProd, minifyCSS()))
        .pipe(buffer())
        .pipe(rev())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('siteroot/static_build'))
        .pipe(rev.manifest({path: 'rev-manifest-styles.json'}))
        .pipe(gulp.dest('siteroot/static_build'));
});

gulp.task('scripts-library', function () {
    return processScripts(js_files_library, 'library');
});

gulp.task('scripts', function() {
    return processScripts(js_files, 'frontend');
});

gulp.task('scripts-jsx', function () {
    return processScripts(jsx_files, 'frontend-jsx', true);
});

gulp.task('templates', ['templates-normal'], function() {
    return gulp.src('*/frontend/**/*.html')
        .pipe(gulp.dest('siteroot/static_build/views'));
});

gulp.task('templates', function() {
    return gulp.src(['*/frontend/**/*.html'])
        .pipe(rename(function(path) {
            path.dirname = "views/" + path.dirname.replace('frontend/', '');
        }))
        .pipe(minifyHTML({
            quotes: true,
            empty: true
        }))
        .pipe(templates('templates.js', {module: 'cyb.oko'}))
        .pipe(buffer())
        .pipe(rev())
        .pipe(gulp.dest('siteroot/static_build'))
        .pipe(rev.manifest({path: 'rev-manifest-templates.json'}))
        .pipe(gulp.dest('siteroot/static_build'));
});

gulp.task('fonts', function() {
    return gulp.src('./bower_components/bootstrap-sass-official/assets/fonts/**')
        .pipe(gulp.dest('siteroot/static_build/fonts'));
});

gulp.task('rev-concat', function() {
    return gulp.src('siteroot/static_build/rev-manifest-*.json')
        .pipe(extend('rev-manifest.json'))
        .pipe(gulp.dest('siteroot/static_build'));
});

gulp.task('watch', function() {
    gulp.watch('*/frontend/**/*.scss').on('change', function () { runSequence('styles', 'rev-concat'); });
    gulp.watch(js_files).on('change', function () { runSequence('scripts', 'rev-concat'); });
    gulp.watch(jsx_files).on('change', function () { runSequence('scripts-jsx', 'rev-concat'); });
    gulp.watch('*/frontend/**/*.html').on('change', function () { runSequence('templates', 'rev-concat'); });
});

gulp.task('production', function(cb) {
    isProd = true;
    runSequence(
        ['styles', 'scripts-library', 'scripts', 'scripts-jsx', 'fonts', 'templates'],
        'rev-concat',
        cb);
});

gulp.task('default', function(cb) {
    runSequence(
        ['styles', 'scripts-library', 'scripts', 'scripts-jsx', 'templates'],
        'rev-concat',
        cb);
});
