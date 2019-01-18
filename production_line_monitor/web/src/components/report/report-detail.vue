<template>
  <div class="report-wrap q-pt-md">
    <div class="report-item row justify-between">
      <div class="col row q-ma-sm">
        <span class="col text-left">总数/可报(合格数&nbsp;&nbsp;  ):</span>
        <span class="col text-bold text-center text-primary font-40">
          {{ reportDetail.current_detected_count && reportDetail.current_detected_count.qualified_count }} / {{ reportDetail.remain_submit_count && reportDetail.remain_submit_count.qualified_count  }}
        </span>
      </div>
      <div class="col row q-ma-sm">
        <div class="report-left-title text-left">报工合格数&nbsp;&nbsp;  :</div>
        <div class="report-right-input text-left row justify-between">
          <div>
            <div class="input-wrap">
              <input v-model="form.qualified_count" class="block full-width input-style text-center text-primary text-bold font-40" autocomplete="off" min="0" type="number" />
            </div>
            <q-icon
              class="cursor-pointer q-mt-sm"
              size="2rem"
              :color="qualified_auto_fill ? 'primary' : 'faded'"
              :name="qualified_auto_fill ? 'sync' : 'sync_disabled'"
              @click.native="changeQualified(!qualified_auto_fill)"></q-icon>
          </div>
          <span v-show="qualifiedError" class="text-red">已超出剩余</span>
        </div>
      </div>
    </div>
    <div class="report-item row justify-between">
      <div class="col row q-ma-sm">
        <span class="col text-left">总数/可报(不合格数):</span>
        <span class="col text-bold text-red text-center font-40">
          {{ reportDetail.current_detected_count && reportDetail.current_detected_count.unqualified_count }} / {{ reportDetail.remain_submit_count && reportDetail.remain_submit_count.unqualified_count }}
        </span>
      </div>
      <div class="col row q-ma-sm">
        <span class="report-left-title text-left">报工不合格数:</span>
        <div class="report-right-input text-left row justify-between">
          <div>
            <div class="input-wrap">
              <input v-model="form.unqualified_count" class="block full-width input-style text-center text-red text-bold font-40" autocomplete="off" min="0" type="number" />
            </div>
            <q-icon
              class="cursor-pointer q-mt-sm"
              size="2rem"
              :color="unqualified_auto_fill ? 'primary' : 'faded'"
              :name="unqualified_auto_fill ? 'sync' : 'sync_disabled'"
              @click.native="changeUnqualified(!unqualified_auto_fill)"></q-icon>
          </div>
          <span v-show="unqualifiedError" class="text-red">已超出剩余</span>
         </div>
      </div>
    </div>
    <div class="text-right">
      <q-btn size="1.5rem" :disabled="qualifiedError || this.unqualifiedError" @click="confirm" class="q-ml-md report-btn" label="报工"></q-btn>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    reportDetail: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      amount: '',
      qualified_auto_fill: false,
      unqualified_auto_fill: false,
      form: {
        qualified_count: 0,
        unqualified_count: 0
      }
    }
  },
  watch: {
    reportDetail: {
      deep: true,
      immediate: true,
      handler () {
        this.init()
      }
    }
  },
  computed: {
    // 合格数上报异常
    qualifiedError () {
      if (this.reportDetail.current_detected_count) {
        return this.form.qualified_count > this.reportDetail.remain_submit_count.qualified_count
      } else {
        return false
      }
    },
    unqualifiedError () {
      // 不合格数上报异常
      if (this.reportDetail.current_detected_count) {
        return this.form.unqualified_count > this.reportDetail.remain_submit_count.unqualified_count
      } else {
        return false
      }
    }
  },
  created () {
    // 设置数据
    this.init()
  },
  methods: {
    init () {
      if (this.reportDetail.current_submitted_count) {
        this.form = {
          ...this.reportDetail.current_submitted_count
        }
      } else {
        this.form = {
          qualified_count: 0,
          unqualified_count: 0
        }
      }
      this.qualified_auto_fill = false
      this.unqualified_auto_fill = false
    },
    // 填充合格数
    changeQualified (value) {
      this.qualified_auto_fill = value
      if (value) {
        this.form.qualified_count = this.reportDetail.remain_submit_count.qualified_count
      } else {
        this.form.qualified_count = this.reportDetail.current_submitted_count.qualified_count
      }
    },
    // 填充不合格数
    changeUnqualified (value) {
      this.unqualified_auto_fill = value
      if (value) {
        this.form.unqualified_count = this.reportDetail.remain_submit_count.unqualified_count
      } else {
        this.form.unqualified_count = this.reportDetail.current_submitted_count.unqualified_count
      }
    },
    confirm () {
      // 检测数据
      let { unqualified_count: unCount, qualified_count: count } = this.form
      let nUnCount = Number(unCount)
      let nCount = Number(count)
      let message = ''
      if (isNaN(nUnCount) || isNaN(nCount)) {
        message = '数据格式错误,请输入数字!!!'
      } else if (nUnCount < 0 || nCount < 0) {
        message = '请检查数据,不能为负值!!!'
      }

      if (message) {
        this.showNotify({
          message
        })
      } else {
        this.$emit('report-callback', this.form)
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
  .report-item
    line-height 2rem
    .report-left-title
      text-align left
      width 150px
      display inline-block
    .report-right-input
      display inline-block
      width: calc(100% - 150px)
    .font-40
      font-size 40px
    .input-wrap
      display inline-block
      width: calc(100% - 50px)
    .input-style
      border none
      outline none
      border-bottom 1px solid #ccc
      background-color transparent
      &::-webkit-outer-spin-button,
      &::-webkit-inner-spin-button
        -webkit-appearance none
  .report-btn
    background rgba(2, 123, 227, .3)
</style>
