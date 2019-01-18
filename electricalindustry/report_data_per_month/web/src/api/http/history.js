import Vue from 'vue'

const $get = Vue.prototype.$get
// const $delete = Vue.prototype.$delete
// const $post = Vue.prototype.$post
// const $put = Vue.prototype.$put

export default {
  // 获取报工历史
  getReportHistory (suc) {
    $get('/api/progress_report/report/data_per_month', suc, null)
  }
}
