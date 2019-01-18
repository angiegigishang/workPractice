<template>
  <v-touch class="full-width full-height relative-position overflow-hidden"
           @swipe2="getsureHandler">
    <!-- 左右跳转 -->
    <v-touch @tap="getsureHandler" class="location-left">
      <q-btn round icon="chevron_left" size="md"></q-btn>
    </v-touch>
    <v-touch @tap="getsureHandler" class="location-right">
      <q-btn round icon="chevron_right" size="md"></q-btn>
    </v-touch>
    <div class="main full-width full-height">
      <!-- 演示功能 -->
      <div v-if="!onlineVersion" style="color: #403E42; ">
        <div class="fixed" style="left: 250px; top: 45px;">
          <q-btn v-ripple dense outline round icon="cached" @click="resetProcess"></q-btn>
        </div>
        <div class="fixed" style="left: 20px; bottom: 10px;">
          <q-btn class="q-ml-sm" label="全部显示" v-ripple dense outline round icon="select_all" @click="switchDisplay('all')"></q-btn>
          <q-btn class="q-ml-sm" label="计划" v-ripple dense outline round icon="format_list_numbered" @click="switchDisplay('plan')"></q-btn>
          <q-btn class="q-ml-sm" label="质量" v-ripple dense outline round icon="high_quality" @click="switchDisplay('quality')"></q-btn>
          <q-btn class="q-ml-sm" label="设备" v-ripple dense outline round icon="settings_input_hdmi" @click="switchDisplay('equipment')"></q-btn>
          <q-btn class="q-ml-sm" label="人员" v-ripple dense outline round icon="people" @click="switchDisplay('people')"></q-btn>
          <q-btn class="q-ml-sm" label="异常" v-ripple dense outline round icon="warning" @click="switchDisplay('warning')"></q-btn>
        </div>
        <!--<div class="fixed" style="right: 20px; top: 85px;">-->
          <!--<q-btn v-ripple dense outline round icon="new_releases" @click="randomWarning"></q-btn>-->
        <!--</div>-->
      </div>
      <!-- 标题 -->
      <div class="q-display-2 text-bold absolute" style="left: 20px; top: 40px;">{{ piplineName }}</div>
      <!-- 时钟 -->
      <time-clock class="absolute" style="right: 20px; top: 40px;"></time-clock>
      <!-- 异常提示文字 -->
      <warning-message
          v-if="warningArr.length > 0"
          :data="warningArr"
          :options="classOption"
          :show="show"
          class="absolute"
          style="width: 25%;right: 60px; top: 85px"
      >
      </warning-message>
      <!-- 累计生产 -->
      <total-num v-if="processList.length > 0" :data="total" :show="show"></total-num>
      <div class="q-px-md">
        <!--生产计划仪表盘-->
        <plan-list :data="plans" :show="show"></plan-list>
        <!-- 产线信息 -->
        <pipline-detail :processList="processList" :currentPlan="currentPlan" :show="show"></pipline-detail>
        <!-- 在上班人员信息 -->
        <member-on-work :data="checkinInfo" :show="show"></member-on-work>
        <!-- 按钮组 -->
        <q-btn-group class="fixed" style="bottom: 10px; right: 20px">
          <q-btn size="0.5rem" class="q-ml-md report-btn" label="考勤" @click="switchHandler('/checkin')"></q-btn>
          <q-btn size="0.5rem" class="q-ml-md report-btn" label="报工" @click="switchHandler('/report')"></q-btn>
        </q-btn-group>
      </div>
    </div>
  </v-touch>
</template>

<script>
import { mapState } from 'vuex'
import { piplineCode, planChartColors } from 'assets/constant'
import TimeClock from '../common/time-clock'
import TotalNum from './total-num'
import PlanList from './plan-list'
import PiplineDetail from './pipline-detail'
import MemberOnWork from './member-on-work'
import http from 'http/monitor'
import WarningMessage from './warning-message'
import { devWarnings } from 'assets/dev-warning'

export default {
  data () {
    return {
      total: {}, // 累计数
      processList: [], // 工序列表
      checkinInfo: [], // 已上班员工
      plans: [], // 工序所有计划
      planChartColors,
      currentPlan: [],
      show: 'all',
      warningArr: [],
      devWarnings
    }
  },
  computed: {
    ...mapState(['piplineName', 'onlineVersion', 'monitorCheckinInfo', 'monitorEquipmentStatus', 'monitorPlan', 'monitorCurrentPlan', 'monitorProcessList', 'monitorDataCollection', 'monitorWarning']),
    classOption () {
      return {
        step: 0.5,
        limitMoveNum: 1
      }
    }
  },
  watch: {
    monitorCheckinInfo () {
      if (!this.monitorCheckinInfo) {
        return
      }
      this.checkinInfo = this.monitorCheckinInfo
    },
    monitorEquipmentStatus () {
      if (!this.monitorDataCollection || !this.monitorEquipmentStatus || !this.monitorProcessList) {
        return
      }
      this.processList = this._formatList(this.monitorProcessList, this.monitorEquipmentStatus, this.monitorDataCollection.process_quality, this.monitorWarning)
    },
    monitorPlan () {
      if (!this.monitorDataCollection || !this.monitorPlan || !this.monitorCurrentPlan) {
        return
      }
      this.plans = this._formatPlans(this.monitorPlan, this.monitorDataCollection.plan_quality, this.monitorCurrentPlan)
      this.currentPlan = this._formatCurrentPlan(this.monitorCurrentPlan, this.monitorPlan)
    },
    monitorCurrentPlan () {
      if (!this.monitorPlan || !this.monitorCurrentPlan || !this.monitorDataCollection) {
        return
      }
      this.currentPlan = this._formatCurrentPlan(this.monitorCurrentPlan, this.monitorPlan)
      this.plans = this._formatPlans(this.monitorPlan, this.monitorDataCollection.plan_quality, this.monitorCurrentPlan)
    },
    monitorProcessList () {
      if (!this.monitorDataCollection || !this.monitorEquipmentStatus || !this.monitorProcessList) {
        return
      }
      this.processList = this._formatList(this.monitorProcessList, this.monitorEquipmentStatus, this.monitorDataCollection.process_quality, this.monitorWarning)
    },
    monitorDataCollection () {
      if (!this.monitorDataCollection || !this.monitorEquipmentStatus || !this.monitorPlan || !this.monitorCurrentPlan || !this.monitorProcessList) {
        return
      }
      this.total = this.monitorDataCollection.total
      this.plans = this._formatPlans(this.monitorPlan, this.monitorDataCollection.plan_quality, this.monitorCurrentPlan)
      this.processList = this._formatList(this.monitorProcessList, this.monitorEquipmentStatus, this.monitorDataCollection.process_quality, this.monitorWarning)
    },
    monitorWarning () {
      if (!this.monitorDataCollection || !this.monitorEquipmentStatus || !this.monitorProcessList || !this.monitorWarning) {
        return
      }
      this.processList = this._formatList(this.monitorProcessList, this.monitorEquipmentStatus, this.monitorDataCollection.process_quality, this.monitorWarning)
    }
  },
  created () {
    console.log('store', this.$store)
    console.log('monitorWarning', this.monitorWarning)
    this._getPiplineData()
  },
  methods: {
    randomWarning () {
      let randomInt = Math.floor(Math.random() * 8)
      let params = {
        process_code: this.devWarnings[randomInt][0],
        process_warning: this.devWarnings[randomInt][1]
      }
      console.log(params)
    },
    getsureHandler () {
      this.$router.push({path: '/history'})
    },
    resetProcess () { // 工序reset
      http.reset(piplineCode)
    },
    _getPiplineData () {
      if (!this.monitorCheckinInfo || !this.monitorDataCollection || !this.monitorEquipmentStatus || !this.monitorPlan || !this.monitorCurrentPlan || !this.monitorProcessList) {
        return
      }
      this.total = this.monitorDataCollection.total
      this.plans = this._formatPlans(this.monitorPlan, this.monitorDataCollection.plan_quality, this.monitorCurrentPlan)
      this.checkinInfo = this.monitorCheckinInfo
      this.processList = this._formatList(this.monitorProcessList, this.monitorEquipmentStatus, this.monitorDataCollection.process_quality, this.monitorWarning)
      this.currentPlan = this._formatCurrentPlan(this.monitorCurrentPlan, this.monitorPlan)
    },
    _formatPlans (planData, numData, currentPlan) {
      if (planData.length === 0) {
        return
      }
      planData.forEach((plan) => {
        let current = currentPlan.find((item) => {
          return item.plan_id === plan.planId
        })
        if (current !== undefined) {
          plan.isWorking = true
        } else {
          plan.isWorking = false
        }
      })
      return planData.map((item) => {
        let id = item.planId
        let progressColor = this._calcPlanProgress(item)
        let newItem = Object.assign(item, {
          positive_num: numData[id].positive_num,
          negative_num: numData[id].negative_num,
          progress_color: progressColor
        })
        return newItem
      })
    },
    _calcPlanProgress (item) {
      let progressColor = []
      let progress
      if (item.positive_num) {
        progress = item.positive_num / item.planNum * 100
      } else {
        progress = 0
      }
      if (progress !== 100 && progress !== 0) {
        progress = progress.toFixed(1)
      }
      if (progress === 0) {
        progressColor = [this.planChartColors[0], this.planChartColors[0]]
      } else if (progress >= 100) {
        progressColor = [this.planChartColors[1], this.planChartColors[1]]
      } else if (progress > 0 && progress < 100) {
        progressColor = [this.planChartColors[2], this.planChartColors[0]]
      }
      return progressColor
    },
    _formatList (list, status, numData, warningData) {
      console.log('list',list)
      console.log('status', status)
      console.log('numData', numData)
      console.log('warningData', warningData)

      let warningArr = []
      let keys = Object.keys(warningData)
      if (keys.length > 0) {
        list.forEach((item) => {
          let errorProcessCode = keys.find((key) => {
            return key === item.code
          })
          if (errorProcessCode) {
            item.hasError = true

            warningData[errorProcessCode].forEach((errorItem) => {
              warningArr.push({
                process_name: item.name,
                message: errorItem.error_message
              })
            })
          }
        })
        this.warningArr = warningArr
      }
      return list.map((item) => {
        let code = item.code
        item.equipment_status = status[code]
        item.positive_num = numData[code].positive_num
        item.negative_num = numData[code].negative_num
        return item
      })
    },
    _formatCurrentPlan (currentPlan, planData) {
      if (planData.length === 0) {
        return
      }
      return currentPlan.map((item) => {
        if (item.plan_id === '') {
          item.plan_product = ''
        } else {
          let current = planData.find((plan) => {
            return item.plan_id === plan.planId
          })
          item.plan_product = current.planProduct
        }
        return item
      })
    },
    switchHandler (param) {
      this.$router.push(param)
    },
    switchDisplay (param) {
      this.show = param
    }
  },
  components: {
    TimeClock,
    TotalNum,
    PlanList,
    PiplineDetail,
    MemberOnWork,
    WarningMessage
  }
}
</script>

<style lang="stylus" scoped>
@import "~variables"
.main
  margin 0 auto
.report-btn
  background rgba(2, 123, 227, .3)
</style>
