/*
* install all vue plugins here
* */

import VueI18n from 'vue-i18n'
import messages from 'src/i18n'
import MgComponents from 'mg-front-end-framework'
import DatePicker from 'vue-datepicker-local'

export default ({ app, Vue }) => {
  Vue.use(VueI18n)
  // Set i18n instance on app
  app.i18n = new VueI18n({
    locale: 'zh',
    fallbackLocale: 'zh',
    messages
  })

  Vue.use(MgComponents)

  Vue.component('date-picker', DatePicker)
}
