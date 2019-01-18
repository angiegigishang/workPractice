<template>
  <v-touch class="full-width full-height"
           @swipe2="getsureHandler">
    <!-- 左右跳转 -->
    <v-touch @tap="getsureHandler" class="location-left">
      <q-btn round icon="chevron_left" size="md"></q-btn>
    </v-touch>
    <v-touch @tap="getsureHandler" class="location-right">
      <q-btn round icon="chevron_right" size="md"></q-btn>
    </v-touch>
    <div class="report-page full-width full-height">
      <div class="full-height column">
        <div class="header-view row justify-between">
          <!-- 标题 -->
          <div class="q-display-2 text-bold">{{ piplineName }}</div>
          <!-- 时钟 -->
          <time-clock style="margin-top: 0"></time-clock>
        </div>
        <div class="content-view row justify-around">
          <div class="col-2 left-view column justify-around">
            <template v-for="person in groupList ">
              <people-component :group.sync="group" :person="person"></people-component>
            </template>
          </div>
          <div class="col-9 right-view">
            <process-list class="items-center" :group="group" :process-data="processData"></process-list>
            <report-list style="margin-top: 40px" :plan-code.sync="planCode" :report-plan="reportPlan"></report-list>
            <!--<div class="title-1 text-primary text-left plan-material">{{ currentPlan.material_name }}</div>-->
            <report-detail :report-detail="reportDetail" @report-callback="reportCallback"></report-detail>
          </div>
        </div>
      </div>
    </div>
  </v-touch>
</template>

<script>
import { mapState } from 'vuex'
import http from 'http/report'
import TimeClock from '../common/time-clock'
import peopleComponent from './people'
import processList from './process-list'
import reportList from './report-list'
import reportDetail from './report-detail'
import { piplineCode } from 'assets/constant'
export default {
  components: {
    peopleComponent,
    processList,
    reportList,
    reportDetail,
    TimeClock
  },
  computed: {
    ...mapState(['piplineName']),
    processData () {
      let oFind = this.processListData.find(o => o.group_code === this.group)
      return oFind ? oFind.process_list : []
    },
    processCode () {
      let oFind = this.processData.find(o => o.is_report_point === 1)
      return oFind ? oFind.code : ''
    },
    currentPlan () {
      if (this.planCode) {
        return this.reportPlan.find(o => o.plan_number === this.planCode)
      } else {
        return {}
      }
    },
    // 报工详情
    reportDetail () {
      if (this.planCode) {
        return this.currentPlan.report_data
      } else {
        return {}
      }
    }
  },
  data () {
    return {
      group: '',
      groupList: [],
      processListData: [],
      planCode: '',
      reportPlan: []
    }
  },
  watch: {
    // 人员组change => 更新计划
    group () {
      // 获取计划信息
      this.getGroupPlan()
    }
  },
  created () {
    this.$q.loading.show()
    this.init()
  },
  methods: {
    // 页面手势
    getsureHandler () {
      this.$router.push({ path: '/' })
    },
    // promise
    getPromise (path) {
      return new Promise((resolve, reject) => {
        http[path](piplineCode, res => {
          if (res.code === 'fail') {
            reject(res.info)
          } else {
            resolve(res.data)
          }
        })
      })
    },
    // 初始化处理
    init () {
      // 人员
      let pPerson = this.getPromise('getProductLinePerson')
      // 工序
      let pProcess = this.getPromise('getProductLineProcess')
      Promise.all([pPerson, pProcess]).then(result => {
        this.groupList = result[0] || []
        this.processListData = result[1] || []
        if (this.groupList.length) {
          this.group = this.groupList[0].group_code
        }
        // this.getGroupPlan()
      }).catch(error => {
        console.log(error)
      })
    },
    // 获取计划列表
    getGroupPlan () {
      http.getProductLinePlan(piplineCode, this.group, this.processCode, res => {
        this.$q.loading.hide()
        if (this.responseValidate(res)) {
          this.reportPlan = res.data || []
          if (this.reportPlan.length) {
            this.planCode = this.reportPlan[0].plan_number
          }
        }
      }, () => {
        this.$q.loading.hide()
      })
    },
    // 确认报工
    reportCallback (form) {
      // 报工处理
      let plan = this.reportPlan.find(o => o.plan_number === this.planCode)
      let data = {
        'group_code': this.group,
        'plan_number': this.planCode,
        'process_code': this.processCode,
        'material_name': plan.material_name,
        'material_code': plan.material_code,
        'unqualified_count': Number(form.unqualified_count),
        'qualified_count': Number(form.qualified_count)
      }
      http.saveReport(data, res => {
        if (this.responseValidate(res)) {
          this.showNotify({
            message: '报工成功！',
            color: 'positive'
          })
        } else {
          this.showNotify({
            message: '报工失败！',
            color: 'negative'
          })
        }
      })
    }
  }
}
</script>

<style lang="stylus" scoped>
  .header-view
    padding 40px 20px 8px
  .content-view
    height 87vh
    .plan-material
      margin-top 20px
  .back-btn
    background rgba(2, 123, 227, .3)
</style>
