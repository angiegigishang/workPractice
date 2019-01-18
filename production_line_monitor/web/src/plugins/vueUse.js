/*
* install all vue plugins here
* */

import VueI18n from 'vue-i18n'
import messages from 'src/i18n'
import VueTouch from 'vue-touch'
// 1指水平滑动
VueTouch.registerCustomEvent('swipe2', {
  type: 'swipe',
  pointers: 1,
  direction: 'horizontal'
})
// 3指水平滑动
// VueTouch.registerCustomEvent('swipe3', {
//   type: 'swipe',
//   pointers: 3,
//   direction: 'horizontal'
// })

export default ({ app, Vue }) => {
  Vue.use(VueI18n)
  // Set i18n instance on app
  app.i18n = new VueI18n({
    locale: 'zh',
    fallbackLocale: 'zh',
    messages
  })

  Vue.use(VueTouch)
}
