helpers =
  arrayToHash: (array)->
    i = 0
    hash = {}
    while i < array.length
      hash[ array[i] ] = array[i+1]
      i+=2
    hash


module.exports = (grunt) ->
  grunt.initConfig
    pkg: grunt.file.readJSON("package.json")


    banners:
        credits: "/**\n * <%= pkg.name %>-<%= pkg.version %> <%= grunt.template.today('dd/mm/yyyy') %>\n * @author: <%= pkg.authors %>\n **/\n"


    # compile sass
    sass:
      dist:
        options:
          noCache: true
        files:
          '../beepaste/static/css/style.css': 'sass/default.scss'

    # concat vendors file
    concat:
      vendors:
        files: helpers.arrayToHash [
          # output path
          "../beepaste/static/js/beepaste.js",[
            # vendor files
            "vendor/openpgp/dist/openpgp.min.js"
            "js/beepaste.js"
	] ]

    # minify css
    cssmin:
      add_banner:
        options:
          banner: "<%= banners.credits %>"
        files: [
          "../beepaste/static/css/style.min.css": "../beepaste/static/css/style.css"]

    # uglify javascript
    uglify:
      options:
        banner: "<%= banners.credits %>"
        mangle: true
      my_target:
        files: [
            '../beepaste/static/js/beepaste.min.js': ['../beepaste/static/js/beepaste.js']
        ]


    # copy files
    copy:
      templates:
        expand: true
        cwd: './templates/'
        src: '**'
        dest: '../beepaste/templates/'
        flatten: false
        filter: 'isFile'

      fa:
        expand: true
        cwd: './vendor/font-awesome/css/'
        src: 'font-awesome.css'
        dest: '../beepaste/static/css/'
        flatten: false
        filter: 'isFile'

      materializeJS:
        expand: true
        cwd: './vendor/materialize/bin/'
        src: 'materialize.js'
        dest: '../beepaste/static/js/'
        flatten: false
        filter: 'isFile'

      jqueryJS:
        expand: true
        cwd: './vendor/jquery-dist/'
        src: 'jquery.min.js'
        dest: '../beepaste/static/js/'
        flatten: false
        filter: 'isFile'

      openpgpJS:
        expand: true
        cwd: './vendor/openpgp/dist/'
        src: 'openpgp.worker.js'
        dest: '../beepaste/static/js/'
        flatten: false
        filter: 'isFile'

      images:
        expand: true
        cwd: './images/'
        src: '**'
        dest: '../beepaste/static/img/'
        flatten: false
        filter: 'isFile'

      fonts:
        expand: true
        cwd: 'vendor/font-awesome/fonts/'
        src: '**'
        dest: '../beepaste/static/fonts/'
        flatten: false
        filter: 'isFile'

      fonts2:
        expand: true
        cwd: './fonts'
        src: '**'
        dest: '../beepaste/static/fonts/'
        flatten: false
        filter: 'isFile'

    # clean files
    clean:
      static:
        options:
          force: true
        src: ["../beepaste/static"]
      templates:
        options:
          force: true
        src: ["../beepaste/templates"]



    #watch for changes in files
    watch:
      files: [
        'gruntfile.coffee'
        'templates/*.jinja2'
        'templates/**/*.jinja2'
        'js/*.js'
        'sass/*.scss'
       ]
      tasks: ['devtasks']


  grunt.loadNpmTasks 'grunt-contrib-watch'
  grunt.loadNpmTasks 'grunt-contrib-sass'
  grunt.loadNpmTasks 'grunt-contrib-concat'
  grunt.loadNpmTasks 'grunt-contrib-uglify'
  grunt.loadNpmTasks 'grunt-contrib-cssmin'
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-contrib-copy'
  grunt.loadNpmTasks 'grunt-bower-task'
  grunt.loadNpmTasks 'grunt-contrib-clean'
  grunt.loadNpmTasks 'grunt-newer'
  grunt.loadNpmTasks 'grunt-este-watch'



# develop the site
  grunt.registerTask 'default', =>
    grunt.task.run 'devtasks'

# Tasks
  grunt.registerTask 'devtasks' , [ 'clean',
                                    'sass',
                                    'concat:vendors',
                                    'copy',
                                    'uglify',
                                    'cssmin',
                                    'watch'
                                  ]
