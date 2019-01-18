<template>
  <div style="padding: 15px 0">
    <div class="row" style="margin-bottom: 15px;padding: 0 16px">
      <div class=“col” style="margin-right: 20px">
        <date-picker :value="start_date"
                     @input="inputStart"
                     placeholder="开始日期"
                     format="YYYY-MM-DD"></date-picker>
      </div>
      <div class=“col” style="margin-right: 20px">
         <date-picker :value="end_date"
                      @input="inputEnd"
                      placeholder="截止日期"
                      format="YYYY-MM-DD"></date-picker>
      </div>
      <div class=“col”>
        <q-btn color="secondary" size="m" label="查询" @click="query"/>
      </div>
    </div>
    <div class="col-11">
      <div class="q-pl-md q-pr-md">
        <q-table
          :data="data"
          :columns="cols"
          :filter="filter"
          :no-data-label ="$t('message.noData')"
          :no-results-label ="$t('message.noMatchedData')"
          row-key="task_no"
          class="mg-table"
        >
         <template slot="top-left" slot-scope="props">
        <q-search
          hide-underline
          color="secondary"
          v-model="filter"
          class="col-6"
        />
        </template>
        <q-td slot="body-cell-plan_status" slot-scope="{ row, col }" :class="`text-${col.align}`">
          {{ planStatusList[String(row.plan_status)] }}
        </q-td>
        <q-td slot="body-cell-plan_type" slot-scope="{ row, col }" :class="`text-${col.align}`">
          {{ planTypeList[String(row.plan_type)] }}
        </q-td>
        </q-table>
      </div>
    </div>
  </div>
</template>

<script>
import http from 'http/historyManage'
import { date } from 'quasar'
import { planStatusList, planTypeList } from 'assets/constant'
export default {

  data () {
    return {
      filter: '',
      start_date: '',
      end_date: '',
      planStatusList,
      planTypeList,
      cols: [
        { label: '任务单号', field: 'task_no', name: 'task_no', sortable: true, align: 'center' },
        { label: '物料名称', field: 'material_name', name: 'material_name', sortable: true, align: 'center' },
        { label: '计划生产数', field: 'plan_count', name: 'plan_count', sortable: true, align: 'center' },
        { label: '计划开工日期', field: 'plan_start_date', name: 'plan_start_date', sortable: true, align: 'center' },
        { label: '车间名', field: 'workshop_name', name: 'workshop_name', sortable: true, align: 'center' },
        { label: '产线信息', field: 'product_line_code', name: 'product_line_code', sortable: true, align: 'center' },
        { label: '录入人员名', field: 'operator', name: 'operator', sortable: true, align: 'center' },
        { label: '录入时间', field: 'create_time', name: 'create_time', sortable: true, align: 'center' },
        { label: '修改时间', field: 'modified_time', name: 'modified_time', sortable: true, align: 'center' },
        { label: '计划状态', field: 'plan_status', name: 'plan_status', sortable: true, align: 'center' },
        { label: '计划类型', field: 'plan_type', name: 'plan_type', sortable: true, align: 'center' },
        { label: '实际完工日期', field: ' real_end_date', name: ' real_end_date', sortable: true, align: 'center' }
      ],
      data: []
    }
  },
  mounted () {
    this.start_date = date.formatDate(date.addToDate(Date.now(), { days: -7 }), 'YYYY-MM-DD').slice(0, 10)
    this.end_date = date.formatDate(Date.now(), 'YYYY-MM-DD').slice(0, 10)
    this.query()
  },
  methods: {
    // 获取表格数据
    query () {
      http.getHistoryManage(this.start_date, this.end_date, res => {
        this.data = res.data
      })
    },
    inputStart (value) {
      this.start_date = date.formatDate(value, 'YYYY-MM-DD')
    },
    inputEnd (value) {
      this.end_date = date.formatDate(value, 'YYYY-MM-DD')
    }
  }
}
</script>
