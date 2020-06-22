const gulp = require('gulp') 
const cleanCSS = require('gulp-clean-css');
const terser = require('gulp-terser');
const del = require('del')

const OUTPUT_FOLDER = 'collected_static_libs'

const js_files = [
    'node_modules/bootstrap/dist/js/bootstrap.bundle.js',
    'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js',
    'node_modules/jquery/dist/jquery.js',
    'node_modules/jquery/dist/jquery.min.js',
];

const css_files = [
    'node_modules/bootstrap/dist/css/bootstrap.css',
    'node_modules/bootstrap/dist/css/bootstrap.min.css',
];
  
gulp.task('distribute_js', function() {
    return gulp.src(js_files)
        .pipe(terser())
        .pipe(gulp.dest(`./${OUTPUT_FOLDER}`));
})

gulp.task('distribute_css', function() {
    return gulp.src(css_files)
        .pipe(cleanCSS({level: {1: {specialComments: false}}}))
        .pipe(gulp.dest(`./${OUTPUT_FOLDER}`));
})

gulp.task('build', gulp.parallel('distribute_js', 'distribute_css'))

gulp.task('clean', function(){
    return del(`./${OUTPUT_FOLDER}`, {force:true});
})