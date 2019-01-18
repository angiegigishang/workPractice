import Vue from 'vue'

const $get = Vue.prototype.$get

export default {
  getHistoryManage (startDate, endDate, cbk) {
    $get(`api/plan_management/manage/plan/history/${startDate}/${endDate}`, cbk)
  }
}
