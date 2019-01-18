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
      { path: 'monitor', component: load('monitor/layout') }, // 监控
      { path: 'checkin', component: load('checkin/layout') }, // 考勤
      { path: 'report', component: load('report/layout') } // 报工
    ]
  },

  // Always leave this last one
  { path: '*', component: load('components/Error404') } // Not found
]
