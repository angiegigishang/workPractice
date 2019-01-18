import Vue from 'vue'
import { checkinUrl } from './const'

const $get = Vue.prototype.$get
const $post = Vue.prototype.$post

export default {
  // 考勤查询接口
  getAttendances (param, cbk) {
    $get(`api/attendance_manage/pipeline/${param}/attendance_info`, cbk, null)
    // $get(`api/attendance_manage/pipeline/${param}/attendance_info`, cbk, null, { baseURL: checkinUrl })
  },
  // 人员签到
  sighSubmit (param, succ, fail) {
    $post('api/attendance_manage/checkin_info', param, succ, fail)
    // $post('api/attendance_manage/checkin_info', param, succ, fail, { baseURL: checkinUrl })
  }
}
