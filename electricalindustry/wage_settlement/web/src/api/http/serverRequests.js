import Vue from 'vue'

const $get = Vue.prototype.$get
// const $delete = Vue.prototype.$delete
const $post = Vue.prototype.$post
// const $put = Vue.prototype.$put

export default {
  // declare some methods to communicate with server by using $get | $delete | $post | $put.
  // if you want to access different domain, specify it as the last parameter
  // 获取工序-物料单价
  getPriceMapper (perconCode, cbk) {
    let param = perconCode ? `?person_code=${perconCode}` : ''
    $get(`api/wage_settlement/process_materiel_price_mapper${param}`, cbk, null)
  },
  updatePriceMapper (param, cbk) {
    $post('api/wage_settlement/process_materiel_price_mapper', param, cbk, null)
  },
  // 计时单价
  getTimelyWage (perconCode, cbk) {
    let param = perconCode ? `?person_code=${perconCode}` : ''
    $get(`api/wage_settlement/timely_wage_mapper${param}`, cbk)
  },
  updateTimelyWage (param, cbk) {
    $post('api/wage_settlement/timely_wage_mapper', param, cbk)
  },
  // 获取工资列表
  getWageList (cbk) {
    $get('api/wage_settlement/wage_detail', cbk)
  }
  // cbk is a customed callback function when the server has response
}
