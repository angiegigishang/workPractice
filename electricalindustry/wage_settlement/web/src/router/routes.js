function load (path) {
  return () => import(`components/${path}.vue`)
}
export default
[
  {
    path: '/',
    component: load('index'),
    children: [
      { path: '', component: load('layout') },
      { path: 'wage', component: load('wage/layout') },
      { path: 'piece', component: load('piece/layout') },
      { path: 'time', component: load('time/layout') }
    ]
  },

  // Always leave this last one
  { path: '*', component: load('Error404') } // Not found
]
