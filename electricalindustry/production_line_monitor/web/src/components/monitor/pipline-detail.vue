<template>
  <div>
    <!-- 工序状态示意 -->
    <div v-if="processList.length > 0" class="row justify-center items-center relative-position">
      <q-list class="col-4 text-center" no-border>
        <template v-for="item in processBar">
          <v-touch class="inline-block" @tap="isOnlineVersion('changeProcessStatus',item.status)">
            <q-item v-ripple="showRipple">
             <div class="cursor-pointer">
                <q-icon name="radio_button_checked" :color="item.color"></q-icon>
                <span class="q-body-2">{{ item.name }}</span>
              </div>
            </q-item>
          </v-touch>
        </template>
      </q-list>
      <!--<marquee-text class="col-6 marquee-text">{{content}}</marquee-text>-->
      <m-mask v-show="show !== 'all' && show !== 'equipment'"></m-mask>
    </div>
    <!-- 当前计划 -->
    <div v-if="calcCurrentPlan && calcCurrentPlan.length"
         class="current-plan-wrapper row justify-between q-mx-md relative-position"
         :class="{'high-level': show === 'plan'}"
    >
      <v-touch v-for="item in calcCurrentPlan"
               :key="item.id"
               @tap="isOnlineVersion('processCount', item)"
               class="current-plan q-subheading text-center"
               :style="{'width': item.width}"
      >
        <div v-if="item.plan_id" v-ripple="showRipple" class="relative-position ellipsis">{{item.plan_product}}（{{item.plan_id}}）</div>
      </v-touch>
      <m-mask v-show="show !== 'all' && show !== 'plan'"></m-mask>
    </div>
    <!-- 工序流程 -->
    <div class="row no-wrap justify-between q-mx-md relative-position" style="margin-top: 56px;">
      <!-- 分割线 -->
      <div v-if="processList.length > 0" class="absolute full-width split">
        <div class="relative-position split-look"></div>
        <m-mask v-show="show !== 'all' && show !== 'equipment'"></m-mask>
      </div>
      <!-- 工序 -->
      <template>
        <template v-for="item in processList">
          <div :id="item.code" class="relative-position" style="z-index: 2">
            <!-- 工序物料状态 -->
            <div class="procedure-number text-center row justify-center items-center text-bold text-italic absolute full-width"
                 v-if="!item.is_manul"
                 :class="{'high-level': show === 'quality'}"
            >
              <div class="q-mb-md full-width text-center">
                <span class="color-positive q-headline">{{item.positive_num}}</span><sub v-if="item.negative_num !== null">/<span class="color-negative">{{item.negative_num}}</span></sub>
              </div>
              <m-mask v-show="show !== 'all' && show !== 'quality'"></m-mask>
            </div>
            <!-- 工序icon -->
            <v-touch @tap="isOnlineVersion('processFocus', item.code)" class="relative-position">
              <div class="procedure icon-width icon-height cursor-pointer"
                 :style="{'border-color': processStatusColor2[item.equipment_status], 'box-shadow': focusProcessList.indexOf(item.code) === -1 ? 'none' : '0 0 3px 3px #59648c'}"
                >
                <div class="procedure-circle">
                  <q-icon size="24px" :name="item.is_manul ? manualIcon : deviceIcon" :color="processStatusColor[item.equipment_status]"></q-icon>
                </div>
              </div>
              <bubble-tip v-if="item.hasError" :show="show"></bubble-tip>
              <m-mask v-show="show !== 'all' && show !== 'equipment'"></m-mask>
            </v-touch>
            <!-- 工序名 -->
            <v-touch @tap="isOnlineVersion('changePlan', item)">
              <div class="q-py-sm procedure-title" :class="{'animate-blink': item.code === selectedCode}">
                <div class="title-3 text-center" :class="{ positive: onlineVersion ? false : item.if_change }">{{ item.name }}</div>
              </div>
              <m-mask v-show="show !== 'all' && show !== 'equipment'"></m-mask>
            </v-touch>
          </div>
        </template>
      </template>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { processBar, piplineCode } from 'assets/constant'
import http from 'http/monitor'
import BubbleTip from './bubble-tip'
import MMask from './m-mask'

export default {
  props: {
    processList: {
      type: Array,
      default: () => []
    },
    currentPlan: {
      type: Array,
      default: () => []
    },
    show: {
      type: String,
      default: 'all'
    }
  },
  data () {
    return {
      focusProcessList: [], // 当前需要切换状态的工序code
      manualIcon: 'directions_walk', // 人工
      deviceIcon: 'settings_input_hdmi', // 设备
      processBar,
      processStatusColor: ['neutral', 'warning', 'negative', 'positive'], // 工序状态颜色, 0:关机，1：开机，2：故障，3：加工
      processStatusColor2: ['#E0E1E2', '#F2C037', '#DB2828', '#21BA45'], // 工序状态颜色, 0:关机，1：开机，2：故障，3：加工
      selectedCode: '', // 切换计划选中的工序
      calcCurrentPlan: [],
      content: '进料到位推缸异常!  拨叉前后缸异常!  拨叉左右缸异常! ',
      speed: 30,
      screenWidth: Number
    }
  },
  computed: {
    ...mapState(['onlineVersion']),
    showRipple () {
      return !this.onlineVersion
    }
  },
  methods: {
    changeProcessStatus (status) {
      if (!this.focusProcessList.length) {
        this.showNotify({
          message: '未选中工序'
        })
        return
      }
      const param = {
        process_code_list: this.focusProcessList,
        product_line: piplineCode,
        status: status
      }
      http.changeStatus(param, function (res) {
        this.clearFocusProcessList()
        this.responseValidate(res)
      }.bind(this), this.clearFocusProcessList)
    },
    clearFocusProcessList () { // 清空选中工序
      this.focusProcessList = []
    },
    processFocus (code) { // 记录选中的工序code: 若当前为选中状态，则取消选中
      const index = this.focusProcessList.indexOf(code)
      if (index === -1) {
        this.focusProcessList.push(code)
      } else {
        this.focusProcessList.splice(index, 1)
      }
    },
    processCount (list) { // 工序计数
      const param = {
        process_code_list: list.group,
        product_line: piplineCode
      }
      http.processCount(param, function (res) {
      })
    },
    changePlan (item) {
      if (!item.if_change) {
        return
      }
      this.selectedCode = item.code
      http.changePlan(piplineCode, item.code)
      setTimeout(() => {
        this.selectedCode = ''
      }, 60000)
    },
    isOnlineVersion (funcName, param) {
      if (this.onlineVersion) {
        return
      }
      this[funcName](param)
    },
    _calc (data) {

      console.log('processList',this.processList.length)
     
      let totalLen = this.processList.length
      this.$nextTick(() => {
        this.calcCurrentPlan = data.map((item) => {
          let len = item.group.length
          console.log('totalLen', totalLen)
          console.log('len', len)
          console.log('screenWidth', this.screenWidth)
          //console.log('screenWidth', screenWidth)
          //let x1 = document.getElementById(item.group[0]).offsetLeft
          //let x2 = document.getElementById(item.group[len - 1]).offsetLeft
          //item.width = `${x2 - x1 + 56}px`
          item.width = `${(this.screenWidth/totalLen) * len - 50}px`
          return item
        })
      })
    },
    
  },
  created () {
    this.screenWidth = document.body.clientWidth
  },
  mounted () {
     window.onresize = () => {
        this.screenWidth = document.body.clientWidth
        console.log('onresizescrennwidth', this.screenWidth)
       }    
  },
  components: {
    BubbleTip,
    MMask
  },
  watch: {
    currentPlan (newVal) {
      this._calc(newVal)
    },
    screenWidth (val, newVal) {
      this._calc(this.currentPlan)
      console.log('watch', val, newVal)
    }
  }
}
</script>

<style lang="stylus" scoped>
@import '~variables'
$size = 56px
$size-lg = 32px
$size-sm = 18px
$default-color = #e2dbdb
.marquee-text
  color $negative
.current-plan-wrapper
  height $size-lg
  .current-plan
    line-height $size-lg
    border-bottom 2px solid $tertiary
.high-level
  z-index 9
// 分割线
.split
  height $size
  .split-look
    top 50%
    height 4px
    width 100%
    background-color $default-color
    opacity 0.6
// 工序样式
.procedure-number
  height $size - 8
  top -48px
  left 0
  .color-positive
    color $default-color
  .color-negative
    color $negative
.procedure
  color #fff
  text-align center
  font-weight bold
  border-radius $size
  border-width 4px
  border-style solid
  text-align center
  margin-bottom 10px
  .procedure-circle
    background-color #071C30
    width 100%
    border-radius 100%
    height 100%
.procedure-title
  .positive
    text-decoration underline
.icon-height
    height $size
    line-height $size - 8
.icon-width
    width $size
.title-3
  font-size 14px
  font-weight bold
</style>
