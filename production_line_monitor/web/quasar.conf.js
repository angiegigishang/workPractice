// Configuration for your app
const path = require('path')

module.exports = function (ctx) {
  const devTool = ctx.dev ? '#eval-source-map' : false

  // const requestHost = '192.168.20.128:8989' // equal to 'localhost:80'
  const requestHost = '192.168.20.114:8989' // equal to 'localhost:80'
  const env = ctx.dev
    ? { // so on dev we'll have
      http_base_url: JSON.stringify(`http://${requestHost}`),
      websocket_base_url: JSON.stringify(`ws://${requestHost}/websocket_url`)
    }
    : { // and on build (production):
      http_base_url: '"http://" + location.host',
      websocket_base_url: '"ws://" + location.host + location.pathname + "websocket_url"'
    }
  let plugins = [
    'websocketJs', // comment this line if websocket is not needed
    'vueMixin', // comment if neccessary
    'vueUse',
    'httpJs'
  ]
   ctx.dev && plugins.push('mock') // uncomment if needed

  return {
    // app plugins (/src/plugins)
    plugins: plugins,
    css: [
      'app.styl'
    ],
    extras: [
      'material-icons'
      // 'ionicons',
      // 'mdi',
      // 'fontawesome'
    ],
    supportIE: false,
    vendor: {
      add: [],
      remove: []
    },
    build: {
      distDir: 'dist/monitor', // output dir
      // htmlFilename: 'index.html',
      devtool: devTool,
      env: env, // add to process.env

      scopeHoisting: true,
      vueRouterMode: 'hash',
      // gzip: true,
      // analyze: true,
      // extractCSS: false,
      // useNotifier: false,
      extendWebpack (cfg) {
        // cfg.module.rules.push({
        //   enforce: 'pre',
        //   test: /\.(js|vue)$/,
        //   loader: 'eslint-loader',
        //   exclude: /(node_modules|quasar)/
        // })

        cfg.resolve.alias = {
          ...cfg.resolve.alias, // This adds the existing alias

          // Add your own alias like this
          http: path.resolve(__dirname, './src/api/http')
        }
      }
    },
    devServer: {
      // https: true,
      host: 'localhost', // web ip
      port: 8080, // web port
      open: false // opens browser window automatically
    },
    // framework: 'all' --- includes everything; for dev only!
    framework: {
      components: [
        'QBtn',
        'QIcon',
        'QRadio',
        'QInput',
        'QList',
        'QListHeader',
        'QItem',
        'QItemMain',
        'QItemSeparator',
        'QItemSide',
        'QItemTile',
        'QBtn',
        'QBtnGroup'
      ],
      directives: [
        'Ripple'
      ],
      // Quasar plugins
      plugins: [
        'Notify', 'Cookies', 'AppFullscreen', 'Loading'
      ]
    },
    // animations: 'all' --- includes all animations
    animations: [
    ],

    // leave this here for Quasar CLI
    starterKit: '1.0.2'
  }
}
