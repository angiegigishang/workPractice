import Vue from 'vue'

const $get = Vue.prototype.$get
// const $delete = Vue.prototype.$delete
const $post = Vue.prototype.$post
// const $put = Vue.prototype.$put

export default {
  planList (cbk) { // 查询未下发和已下发计划
    $get('api/plan_management/manage/plan/list', cbk)
  },
  planAdd (param, cbk) { // 添加计划
    $post('api/plan_management/manage/plan/add', param, cbk)
  },
  planDispatch (param, succ, fail) { // 下发计划
    $post('api/plan_management/manage/plan/dispatch', param, succ, fail)
  },
  planDelete (param, cbk) { // 删除计划
    $post('api/plan_management/manage/plan/delete', param, cbk)
  },
  planRollback (param, cbk) { // 回退计划
    $post('api/plan_management/manage/plan/rollback', param, cbk)
  },
  planConfigs (cbk) { // 查询计划相关的配置数据
    $get('api/plan_management/manage/plan/config', cbk)
  },
  getSpecifiedPlan (piplineCode, st, cbk) { // 根据产线和开工日期查询计划
    $get(`api/plan_management/manage/${piplineCode}/${st}/dispatched_plan/list`, cbk)
  },
  validPlanStatus (param, succ) { // 检查准备下发的计划状态
    $post('api/plan_management/manage/plan/dispatch_check', param, succ)
  }
}
