<template>
  <div class="full-width q-mt-md">
    <div class="wage-page">
      <div class="text-bold q-title q-mb-sm">{{ time }}</div>
      <mg-table
      class="common-table wage-table"
      :columns="columns"
      :data="tableData"
      :search="true"
      :rows-option="[0]"
      row-key="person_code"
      :hide-bottom="true"
      v-on:filter-method="filterMethod">
      <template slot="body-cell-person_name" slot-scope="props">
        <div  v-if="props.row.wage_code === 'time'" class="cursor-pointer" style="text-decoration: underline;" @click="goToNext(props.row)">
          {{ props.row.person_name }}
        </div>
        <template v-else>
          {{ props.row.person_name }}
        </template>
      </template>
      <template slot="body-cell-amount" slot-scope="props">
        {{ props.row.wage_code === 'time' ? props.row.total_time : props.row.piece_amount }}
      </template>
      <!--<template slot="body-cell-operate" slot-scope="props">-->
        <!--<q-btn v-if="props.row.wage_code === 'time'" color="secondary" :label="$t('label.adjust')" @click="goToNext(props.row)"></q-btn>-->
      <!--</template>-->
    </mg-table>
    </div>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'
import { date } from 'quasar'
import http from 'http/serverRequests'
export default {
  data () {
    return {
      columns: [
        { name: 'person_name', label: this.$t('table.wage.person_name'), field: 'person_name', align: 'center' },
        { name: 'wage', label: this.$t('table.wage.wage'), field: 'wage', align: 'center' },
        { name: 'wage_type', label: this.$t('table.wage.wage_type'), field: 'wage_type', align: 'center' },
        { name: 'amount', label: this.$t('table.wage.amount'), field: 'amount', align: 'center' },
        { name: 'workshop', label: this.$t('table.wage.workshop'), field: 'workshop', align: 'center' },
        { name: 'pipeline', label: this.$t('table.wage.pipeline'), field: 'pipeline', align: 'center' }
        // { name: 'piece_amount', label: this.$t('table.wage.piece_amount'), field: 'piece_amount', align: 'center' },
        // { name: 'total_time', label: this.$t('table.wage.total_time'), field: 'total_time', align: 'center' },
        // { name: 'operate', label: this.$t('table.wage.operate'), field: 'operate', align: 'center' }
      ],
      tableData: [],
      time: null
    }
  },
  created () {
    this.updateNavTitle(this.$t('title.wage'))
    this.setTime()
    this.getWage()
  },
  methods: {
    ...mapMutations(['updateNavTitle']),
    // 设置时间
    setTime () {
      this.time = date.formatDate(new Date(), 'YYYY年MM月')
    },
    // 获取工资列表
    getWage () {
      http.getWageList(res => {
        if (this.responseValidate(res)) {
          if (this.responseValidate(res)) {
            this.tableData = res.data || []
          }
        }
      })
    },
    // 跳转
    goToNext (row) {
      let { wage_code: wageCode, person_code: personCode } = row
      let url = wageCode === 'time' ? '/time' : '/piece'
      this.$router.push(`${url}?person_code=${personCode}`)
    },
    filterMethod (rows, terms, cols, cellValue) {
      const lowerTerms = terms ? terms.toLowerCase() : ''
      return rows.filter(
        row => cols.some(col => (cellValue(col, row) + '').toLowerCase().indexOf(lowerTerms) !== -1)
      )
    }
  }
}
</script>

<style lang="stylus" scoped>
  .wage-page
    width 80%
    margin 0 auto
  .q-table
    tbody
      td
        padding 0
        height 42px
</style>
