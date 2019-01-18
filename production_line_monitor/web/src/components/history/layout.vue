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
    <div class="full-height main-wrap">
      <div class="header-view row justify-between">
        <div class="row justify-between">
          <!-- 标题 -->
          <div class="q-display-2 text-bold">{{ piplineName }}</div>
          <!-- 搜索框 -->
         <!--  <div class="search">
            <input placeholder="输入搜索内容" v-model="keyword" @keyup="tabSearch">
          </div> -->
        </div>
        <!-- 时钟 -->
        <time-clock style="margin-top: 0"></time-clock>
      </div>
      <div class="full-width content-view row">
        <div class="col-1 column">
          <template v-for="tab in tabList">
            <div @click="changeTab(tab.field)" :class="['col tab-item cursor-pointer', {'bg-primary': active === tab.field}]">
              <div>{{ tab.name }}</div>
            </div>
          </template>
        </div>
        <div class="col-11">
          <div class="q-pl-md q-pr-md">
            <data-table :hname="hname" :cols="cols" :data="data" v-show="active === 'checkin'"></data-table>
            <data-table-report :data="data_report" :headers="headers" v-show="active !== 'checkin'"></data-table-report>
          </div>
        </div>

      </div>
    </div>
 <!--  <router-view></router-view> -->
  </v-touch>
</template>

<script>
import { mapState } from 'vuex'
import DataTable from './history-table-data'
import DataTableReport from './h-d-d'
import TimeClock from '../common/time-clock'
import http from 'http/history'
import { date } from 'quasar'


export default {
  components: {
    DataTable,
    TimeClock,
    DataTableReport
  },
  data () {
    return {
      tabList: [{
        name: '考勤统计',
        field: 'checkin'
      }, {
        name: '报工统计',
        field: 'report'
      }],
      active: '',
      cols: [],
      data: [],
      hname: '',
      data_report: [],
      headers: []
      // keyword: ''
    }
  },
  computed: {
    ...mapState(['piplineName'])
  },
  created () {
    // 默认展示考勤
    this.changeTab('checkin')
  },
  methods: {
    getReportData () {
      let url = 'getReportHistory'
      http[url](res => {
        if (this.responseValidate(res)) {
          let { names, datas } = this.parserReportData(res.data)
          this.data_report = datas
          this.headers = names
        }
      })
    },
    parserReportData (data) {
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
    },
    // 跳转到首页
    getsureHandler () {
      this.$router.push({ path: '/' })
    },
    // 更改显示tab
    changeTab (newTab) {
      if (newTab !== this.active) {
        // 清空数据
        this.cols = []
        this.data = []
        // 切换显示
        this.active = newTab
        this.getTableData()
      }
    },
    // 获取表格数据
    getTableData () {
      let url = this.active === 'checkin' ? 'getCheckInHistory' : 'getReportHistory'
      if (this.active !== 'checkin') {
        this.getReportData()
        return
      }
      // 获取当前月
      let month = date.formatDate(new Date(), 'YYYYMM')
      //console.log(month)

      http[url](month, res => {
        //console.log(res);

        if (this.responseValidate(res)) {
          let { cols, data } = this.parseTableData(res.data)
          //console.log(cols);
          //console.log(data);
          this.cols = cols
          this.data = data
        }
      })

    },
    //搜索功能
    // tabSearch () {
    //   console.log(this.keyword)

    //   if(this.keyword.trim() != '') {

    //   let url = "getSearchHistory"

    //   let month = date.formatDate(new Date(), 'YYYYMM')
    //   let name = this.keyword

    //   console.log(month, name)

    //   http[url](month, name, res => {

    //     let { cols, data } = this.parseTableData(res.data)

    //       this.cols = cols
    //       this.data = data


    //   })
    // } else {
    //   this.getTableData();
    // }

    // },
    // 数据转换
    parseTableData ({ header_list: headerList, data_list: dataList }) {
      //console.log(headerList);
      //console.log(dataList);
      let header = []
      let body = []

      // 表头处理
      header = headerList.map(o => {
        //console.log(o);
        let { code, name } = o
        return {
          name,
          field: code
        }
      })

      //console.log('1',header)

      let newheader = []
      //解析姓名列
      for(let item in header) {
        if(header[item].field != 'name') {
          newheader.push(header[item]);
        } else {
          this.hname = header[item].name;
        }
      }
      header = newheader;

      //console.log('2',header)
      //console.log(this.hname)

      // 内容体设置
      body = dataList.map(o => {
        //console.log(o);
        let oCurrent = {
          name: o.name,
          ...o.data
        }
        //console.log(oCurrent);
        let oRow = {}
        header.forEach(col => {
          //console.log('col', col)
         // console.log('oCurrent', oCurrent)
          oRow['name'] = oCurrent.name;
          if (col.field in oCurrent) {
            oRow[col.field] = oCurrent[col.field]
          } else {
            oRow[col.field] = null
          }
        })
        //console.log(oRow);
        return oRow
      })
      //console.log('header', header)
      //console.log('body', body)
      return {
        cols: header,
        data: body
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
  .main-wrap
    width 96%
    margin 0 auto
  .header-view
    padding 40px 20px 4px
    border-radius: 4px
  .content-view
    height 87vh
    border-radius: 4px
  .tab-item
    display flex
    align-items center
    justify-content center
    background-color rgba(102, 112, 140, .2)
    border-radius: 4px
  input
    opacity 0.6
    border-radius 6px
    padding 6px
    outline none
  .search
    margin-left: 10px
    margin-top: 5px

</style>

