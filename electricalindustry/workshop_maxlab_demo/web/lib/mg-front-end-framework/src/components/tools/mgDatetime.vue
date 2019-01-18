<template>
  <div :class="['time-box', disable ? 'disabled' : '']">
    <datetime :format="currentFormat.compFormat"
              :phrases="timePhrases"
              :value="parseTime"
              value-zone="local"
              @input="timeChange"
              :type="mode"
              :placeholder="placeholder"
              class="them-secondary"
              input-class="datetime-input full-width"
              :min-datetime="minT"
              :max-datetime="maxT"></datetime>
    <div class="clear-btn" v-show="showClearIcon" @click="timeChange('')">x</div>
    <div v-show="disable" class="disabled-layer"></div>
  </div>
</template>

<script>
import { date } from 'quasar'
import { Datetime } from 'vue-datetime'
import { Settings } from 'luxon'
import 'vue-datetime/dist/vue-datetime.css'

Settings.defaultLocale = 'zh'
export default {
  name: 'mg-datetime',
  components: {
    Datetime
  },
  data () {
    return {
      minT: '',
      maxT: '',
      parseTime: '',
      realFormat: 'YYYY-MM-DDTHH:mm:ss',
      dateFormat: {
        compFormat: 'yyyy-MM-dd',
        dataFormat: 'YYYY-MM-DD',
        config: { hours: 0, minutes: 0, seconds: 0 }
      },
      datetimeFormat: {
        compFormat: 'yyyy-MM-dd HH:mm:ss',
        dataFormat: 'YYYY-MM-DD HH:mm:ss',
        config: { seconds: 0 }
      },
      timePhrases: {ok: '确认', cancel: '取消'}
    }
  },
  computed: {
    currentFormat () {
      return this.mode === 'date' ? this.dateFormat : this.datetimeFormat
    },
    showClearIcon () {
      return this.clear && this.parseTime
    }
  },
  props: {
    clear: {
      type: Boolean,
      default: false
    },
    mode: {
      type: String,
      default: 'datetime'
    },
    time: {
      type: String,
      default: ''
    },
    max: {
      type: String,
      default: ''
    },
    min: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: '时间'
    },
    disable: {
      type: Boolean,
      default: false
    }
  },
  created () {
    this.parseTime = this.getFormatTime(this.time)
  },
  watch: {
    time (value) {
      this.parseTime = this.getFormatTime(value)
    },
    min: {
      immediate: true,
      handler (value) {
        this.setSpecialTime(value, 'minT')
      }
    },
    max: {
      immediate: true,
      handler (value) {
        this.setSpecialTime(value, 'maxT')
      }
    }
  },
  methods: {
    setSpecialTime (time, tag) {
      this[tag] = time ? this.getFormatTime(time) : time
    },
    getFormatTime (t) {
      return date.formatDate(t, this.realFormat)
    },
    timeChange (time) {
      this.parseTime = time
      let realTime = time && this.timeFormat(time, this.currentFormat.config)
      this.$emit('update:time', realTime)
    },
    timeFormat (t, options) {
      return date.formatDate(date.adjustDate(t, options), this.currentFormat.dataFormat)
    }
  }
}
</script>

<style lang="stylus">
  @import "~variables"

  .time-box
    position relative
    height 42px
    width 180px
    .clear-btn
      cursor pointer
      position absolute
      top 0
      right 4px
      text-align center
      line-height 20px
      height 20px
      border-radius 50%
      width 20px
      margin-top 11px
      color darkgrey
    .clear-btn:hover
      background #e6e5e5
      color #000

  .datetime-input
    height 36px
    margin 3px
    border 1px solid #BDBDBD
    padding 3px

  .them-secondary .vdatetime-popup__header,
  .them-secondary .vdatetime-calendar__month__day--selected > span > span,
  .them-secondary .vdatetime-calendar__month__day--selected:hover > span > span
    background: $secondary

  .them-secondary .vdatetime-year-picker__item--selected,
  .them-secondary .vdatetime-time-picker__item--selected,
  .them-secondary .vdatetime-popup__actions__button
    color $secondary

  .disabled
    opacity 0.6 !important
    cursor not-allowed
    .disabled-layer
      position absolute
      width 100%
      height 100%
      top 0
      z-index 100

</style>
