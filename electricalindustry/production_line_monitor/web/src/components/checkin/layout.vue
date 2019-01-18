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
    <div class="main">
      <!-- 标题 -->
      <div class="q-display-2 text-bold title-left height-fit">{{ piplineName }}</div>
      <!-- 时钟 -->
      <time-clock class="title-right height-fit"></time-clock>

      <checkin-gather :process-list="processList"
                      :checkin-group="checkinInfo"
                      @submit="signSubmit"></checkin-gather>
    </div>
  </v-touch>
</template>

<script>
import { mapState } from 'vuex'
import CheckinGather from './checkin-gather'
import TimeClock from '../common/time-clock'
import http from 'http/checkin'
import { piplineCode } from 'assets/constant'
export default {
  components: {
    CheckinGather,
    TimeClock
  },
  data () {
    return {
      processList: [],
      checkinInfo: []
    }
  },
  computed: {
    ...mapState(['piplineName'])
  },
  created () {
    http.getAttendances(piplineCode, function (res) {
      if (res.code === 'success') {
        const data = res.data
        this.processList = data.processList
        this.checkinInfo = data.checkinInfo
      }
    }.bind(this))
  },
  methods: {
    getsureHandler () { // 手势跳转
      this.$router.push({ path: '/' })
    },
    signSubmit (memberList) {
      // 防止误操作
      if (!Array.isArray(memberList) || !memberList.length) {
        return
      }

      // 提交到后台
      const param = {
        checkin_info: memberList,
        pipeline_code: piplineCode
      }
      http.sighSubmit(param, function (res) {
        if (this.responseValidate(res)) {
          this.checkinInfo = res.data
        }
      }.bind(this))
    }
  }
}
</script>

<style lang="stylus" scoped>
  .main
    width 90%
    margin 0 auto
  .height-fit
    height fit-content
  .title-left
    position absolute
    top 40px
    left 20px
  .title-right
    position absolute
    top 40px
    right 20px
</style>
