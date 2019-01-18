<template>
  <v-touch class="full-width column full-height">
    <div class="header-view row justify-between">
      <!-- 标题 -->
      <div class="q-display-2 text-bold">{{ $t('title.mainTitle') }}</div>
      <!-- 时钟 -->
      <time-clock style="margin-top: 0"></time-clock>
    </div>
    <div class="full-width content-view row">
      <div class="content">
        <div class="q-pl-md q-pr-md">
          <data-table :data="data" :headers="headers"></data-table>
        </div>
      </div>
  </div>
  </v-touch>
</template>

<script>
import DataTable from 'components/common/data-table'
import TimeClock from '../common/time-clock'
import http from 'http/history'
export default {
  components: {
    DataTable,
    TimeClock
  },
  data () {
    return {
      data: [],
      headers: []
    }
  },
  created () {
    this.getTableData()
  },
  methods: {
    // 获取表格数据
    getTableData () {
      let url = 'getReportHistory'
      http[url](res => {
        if (this.responseValidate(res)) {
          let { names, datas } = this.parserTableData(res.data)
          this.data = datas
          this.headers = names
        }
      })
    },
    parserTableData (data) {
      let dates = Object.keys(data.group_data)
      dates.sort((a, b) => {
        return a.localeCompare(b) > 0
      })
      let datas = dates.map(val => ({
        data: data.group_data[val],
        date: val
      }))
      return {
        datas,
        dates,
        names: data.group_names
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
  .header-view
    padding 40px 20px 4px
  .content-view
    height 87vh
  .tab-item
    display flex
    align-items center
    justify-content center
    background-color rgba(102, 112, 140, .2)
  .content
    width 100vw
    margin 0 auto
</style>
