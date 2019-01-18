import Vue from 'vue'
import { checkinUrl, reportUrl } from './const'

const $get = Vue.prototype.$get

export default {
  // 获取考勤历史
  getCheckInHistory (month, cbk) {
    // $get('api/attendance_manage/statistics/' + month, cbk, null)
    $get('api/attendance_manage/statistics/' + month, cbk, null, { baseURL: checkinUrl })
  },

  // 获取报工历史
  getReportHistory (cbk) {
    $get('api/progress_report/report/data_per_month', cbk, null)
    // $get('api/progress_report/report/data_per_month', cbk, null, { baseURL: reportUrl })
  }
}
