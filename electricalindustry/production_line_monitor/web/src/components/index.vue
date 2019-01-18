<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import http from 'http/monitor'
import { piplineCode } from 'assets/constant'
export default {
  watch: {
    '$route': {
      immediate: true,
      handler (to) {
        if (to.name === 'monitor') {
          this.getData()
        }
      }
    }
  },
  methods: {
    ...mapActions(['updateAllData']),
    getData () { // 查询监控页面数据
      this.$q.loading.show()
      http.getPiplineData(piplineCode, function (res) {
        if (res.code === 'success') {
          this.$q.loading.hide()
          this.updateAllData(res.data)
        }
      }.bind(this), function () {
        this.$q.loading.hide()
      }.bind(this))
    }
  }
}
</script>
