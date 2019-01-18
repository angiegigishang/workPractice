import Vue from 'vue'
import { reportUrl } from './const'

const $get = Vue.prototype.$get
const $post = Vue.prototype.$post

export default {
  // 获取某产线所有人员信息
  getProductLinePerson (productLineCode, cbk) {
    $get(`api/progress_report/${productLineCode}/employee/list`, cbk, null)
    // $get(`api/progress_report/${productLineCode}/employee/list`, cbk, null, { baseURL: reportUrl })
  },

  // 获取产线的所有工序
  getProductLineProcess (productLineCode, cbk) {
    $get(`api/progress_report/${productLineCode}/process/list`, cbk, null)
    // $get(`api/progress_report/${productLineCode}/process/list`, cbk, null, { baseURL: reportUrl })
  },

  // 获取报工点工序相关计划列表
  getProductLinePlan (productLineCode, groupCode, processCode, cbk, failCbk) {
    $get(`api/progress_report/${productLineCode}/${groupCode}/${processCode}/production_plan/list`, cbk, failCbk)
    // $get(`api/progress_report/${productLineCode}/${groupCode}/${processCode}/production_plan/list`, cbk, null, { baseURL: reportUrl })
  },

  // 保存报工数据
  saveReport (param, cbk) {
    $post('api/progress_report/report/save', param, cbk, null)
    // $post('api/progress_report/report/save', param, cbk, null, { baseURL: reportUrl })
  }
  // cbk is a customed callback function when the server has response
}
