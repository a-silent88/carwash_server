// Assuming you already have NodeJS, npm and gulp installed
// and followed instructions at:
// https://www.browsersync.io/docs/gulp/
//
// save this file at <<DJANGO PROJECT ROOT>>
// on your terminal:
// $ cd <<DJANGO PROJECT ROOT>>
// $ gulp

// this will open a browser window with your project
// and reload it whenever a file with the extensions scss,css,html,py,js
// is changed

var gulp = require('gulp');
var autoprefixer = require('gulp-autoprefixer');
var cleanCSS = require('gulp-clean-css');
var browserSync = require('browser-sync').create();
var sourcemaps = require('gulp-sourcemaps');
var gcmq = require('gulp-group-css-media-queries');
var preproc = require('gulp-less');
var gutil = require( 'gulp-util' );
var ftp = require( 'vinyl-ftp' );
var plumber = require('gulp-plumber');
var tinypng = require('gulp-tinypng-extended');

var config = {
    src: '.',
    css: {
        watch: 'static/css/*.css',
        src: 'src/less/main.less',
        dest: 'static/css/'
    },
    py: {
        src: './**/**/**/*.py'
    },
    html: {
        src: './**/templates/*.html'
    },
	js: {
		src: 'static/js/*.js'
    },
    img: {
        src: '/static/img/'
    },
    ftp: {
        user: '',
        password: '',
        host: '',
        parallel: '',
        log: '',
        dirnew: '',
        dirold: '',
        css: '',
        js: ''

    }
};

gulp.task('build', function (start) {
    gulp.src(config.css.src)
    // .pipe(sourcemaps.init())
    .pipe(preproc())
    .pipe(gcmq())
    .pipe(autoprefixer({
        overrideBrowserslist: ['> 0.1%'],
        cascade: false,
        grid: true
    }))
    // .pipe(cleanCSS({
    //     level: 2
    // }))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(config.css.dest));
    start();
});

gulp.task('tinypng', function () {
    gulp.src(config.img.src + '*.{png,jpg,jpeg}')
        .pipe(plumber())
        .pipe(tinypng({
            key: '9FL9K9jlfDiX9ot6wSUFRi5ib5JWkbtZ',
            sigFile: 'img/.tinypng-sigs',
            log: true
        }))
        .pipe(gulp.dest(config.img.src));
});

gulp.task('watch', function() {
    browserSync.init({
        notify: false,
        proxy: "localhost:8000",
    });
    gulp.watch(config.css.src).on('change', gulp.series('build'));
    gulp.watch(config.css.watch).on('change', browserSync.reload);
    gulp.watch(config.py.src).on('change', browserSync.reload);
    gulp.watch(config.js.src).on('change', browserSync.reload);
    gulp.watch(config.html.src).on('change', browserSync.reload);
});

gulp.task( 'deploy', function () {

	var conn = ftp.create( {
		host:     config.ftp.host,
		user:     config.ftp.user,
		password: config.ftp.password,
		parallel: config.ftp.parallel,
		log:      config.ftp.log
	} );

	var globs = [
		config.ftp.css,
		config.ftp.js
	];

	// using base = '.' will transfer everything to /public_html correctly
	// turn off buffering in gulp.src for best performance

	return gulp.src( globs, { base: '.', buffer: false } )
		.pipe( conn.newer( config.ftp.dirold) ) // only upload newer files
		.pipe( conn.dest( config.ftp.dirnew ) );

} );