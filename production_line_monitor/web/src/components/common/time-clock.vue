<template>
  <div :class="cssCollect">
    <div style="display: inline-block;width: 186px">{{ time }}</div>
    <v-touch @tap="fullscreenHandler" style="display: inline">
      <q-icon :name="$q.fullscreen.isActive ? fullscreenexitIcon : fullscreenIcon"
              size="40px" color="$default-color" class="cursor-pointer"></q-icon>
    </v-touch>
  </div>
</template>

<script>
import { date } from 'quasar'
export default {
  props: {
    extralCss: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    cssCollect () {
      return ['title-2', 'font-led', ...this.extralCss]
    }
  },
  data () {
    return {
      timeFormat: 'YYYY-MM-DD HH:mm:ss', // 时间格式
      refresh: 1000, // 时间刷新间隔
      time: '', // 当前时间
      fullscreenIcon: 'fullscreen', // 全屏icon
      fullscreenexitIcon: 'fullscreen_exit' // 退出全屏icon
    }
  },
  created () {
    this.timeInterval()
  },
  methods: {
    fullscreenHandler () { // 触发全屏
      if (this.$q.fullscreen.isCapable) {
        this.$q.fullscreen.toggle()
      }
    },
    timeInterval () {
      this.time = date.formatDate(new Date(), this.timeFormat)
      setInterval(function () {
        this.time = date.formatDate(new Date(), this.timeFormat)
      }.bind(this), this.refresh)
    }
  }
}
</script>
