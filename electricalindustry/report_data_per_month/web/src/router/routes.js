function load (component, name) {
  // 'components' is aliased to src/components
  return () => import(/* webpackChunkName: "name" */ `components/${component}.vue`)
}

export default
[
  { path: '/',
    component: load('index', 'index'),
    children: [
      {
        path: '',
        component: load('history/layout', 'history')
      }
    ]
  },

  // Always leave this last one
  { path: '*', component: load('components/Error404', '404') } // Not found
]
