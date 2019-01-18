import Vue from 'vue'

const $get = Vue.prototype.$get
// const $delete = Vue.prototype.$delete
const $post = Vue.prototype.$post
// const $put = Vue.prototype.$put

export default {
  // 获取某产线所有人员信息
  getProductLinePerson (productLineCode, cbk) {
    $get(`api/progress_report/${productLineCode}/employee/list`, cbk)
  },

  // 获取产线的所有工序
  getProductLineProcess (productLineCode, cbk) {
    $get(`api/progress_report/${productLineCode}/process/list`, cbk)
  },

  // 获取报工点工序相关计划列表
  getProductLinePlan (productLineCode, groupCode, processCode, cbk) {
    $get(`api/progress_report/${productLineCode}/${groupCode}/${processCode}/production_plan/list`, cbk)
  },

  // 保存报工数据
  saveReport (param, cbk) {
    $post('api/progress_report/report/save', param, cbk)
  }
  // cbk is a customed callback function when the server has response
}
