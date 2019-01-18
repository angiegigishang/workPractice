import Vue from 'vue'
import { monitorUrl, monitorResetUrl } from './const'

const $get = Vue.prototype.$get
const $post = Vue.prototype.$post

export default {
  getPiplineData (param, cbk, failCbk) {
    $get(`/api/monitor/all/${param}`, cbk, failCbk)
    // $get(`/api/monitor/all/${param}`, cbk, failCbk, { baseURL: monitorUrl })
  },
  changePlan (piplineCode, processCode, cbk) {
    $get(`/api/monitor/change_plan/${piplineCode}/${processCode}`, cbk, null)
    // $get(`/api/monitor/change_plan/${piplineCode}/${processCode}`, cbk, null, { baseURL: monitorUrl })
  },
  reset (piplineCode, cbk) { // reset 工序状态
    $get(`api/simulator/set/${piplineCode}`, cbk, null)
    // $get(`api/simulator/set/${piplineCode}`, cbk, null, { baseURL: monitorResetUrl })
  },
  changeStatus (param, succ, fail) { // 工序状态修改
    $post('api/simulator/change_status', param, succ, fail)
    // $post('api/simulator/change_status', param, succ, fail, { baseURL: monitorResetUrl })
  },
  processCount (param, succ, cbk) { // 开始工序计数
    $post('api/simulator/count', param, cbk, null)
    // $post('api/simulator/count', param, cbk, null, { baseURL: monitorResetUrl })
  }
}
