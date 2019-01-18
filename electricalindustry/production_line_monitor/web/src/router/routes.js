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
      { path: '', name: 'monitor', component: load('monitor/layout') }, // 监控
      { path: 'checkin', component: load('checkin/layout') }, // 考勤
      { path: 'report', component: load('report/layout') } // 报工
    ]
  },

  {
    path: '/history',
    component: load('history/layout')
  },

  // Always leave this last one
  { path: '*', name: '404', component: load('Error404') } // Not found
]
