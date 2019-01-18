function load (component) {
  // 'components' is aliased to src/components
  return () => import(`components/${component}.vue`)
}

export default
[
  {
    path: '/',
    component: load('index'),
    children: [
      { path: '', name: 'plan', component: load('plan/layout') },
      { path: 'historyManage', name: 'historyManage', component: load('historyManage/layout') }
    ]
  },

  // Always leave this last one
  { path: '*', component: load('Error404') } // Not found
]
