<template>
  <div class="full-width q-pa-lg">
    <div class="row justify-end q-mb-md">
      <q-btn icon="refresh"
             outline round
             color="secondary"
             @click="getData(true)" />
      <q-btn icon="add"
             class="q-ml-md"
             outline round
             color="secondary"
             @click="openAdd" />
      <q-btn label="批量下发"
             class="q-ml-md"
             outline dense
             color="secondary"
             @click="openDelivery(null)" />
    </div>

    <plan-table :data="data"
                ref="plan_table"
                :columns="displayCols"
                :select-change="selectChange"
                @delete="del"
                @rollback="back"
                @dispatch="openDelivery"></plan-table>
    <mg-modal v-bind="this[modalName + 'Bind']"
              :open.sync="show"
              @confirm="confirm">
      <template slot="body">
        <add-body v-if="modalName === addName"
                  :data="addObj"
                  :cols="addColumns"></add-body>
        <delivery-body v-else-if="modalName === deliveryName"
                       :plans="selectList"
                       :plan-in-order="planInOrder"
                       :workshop="selectWorkshop"
                       :data="deliveryObj"></delivery-body>
      </template>
    </mg-modal>

    <q-page-sticky position="bottom-left" :offset="[50, 50]">
      <q-btn round color="secondary" icon="low_priority" class="animate-pop" @click="$router.push('historyManage')">
        <q-tooltip style="font-size: 12px" anchor="top middle" self="bottom middle" :offset="[0, 6]">
          {{ $t('label.getHistory') }}
        </q-tooltip>
      </q-btn>
    </q-page-sticky>
  </div>
</template>

<script>
import PlanTable from './plan-table'
import AddBody from './add-body'
import DeliveryBody from './delivery-body'
import { mapState } from 'vuex'
import { tableColumns } from 'assets/constant'
// tableColumns字段说明: focus, 添加时必填字段; type, 添加时用于识别字段类型, 不指定则默认input; disable, 添加时为禁用状态; hide, 添加时隐藏该字段; nodisplay, table中是否不显示, 不指定则默认显示
import http from 'http/plan'
import { date } from 'quasar'
export default {
  components: {
    PlanTable,
    AddBody,
    DeliveryBody
  },
  computed: {
    ...mapState(['extralFields', 'workshops']),
    field2name () { // 字段名: 显示名
      let result = Object.create(null)
      tableColumns.forEach(col => { result[col['field']] = col['label'] })
      return result
    }
  },
  watch: {
    selectList (obj) {
      this.planInOrder = obj.map(item => item.task_no)
    },
    extralFields: {
      immediate: true,
      handler (newValue) {
        if (!Array.isArray(newValue)) {
          return
        }

        newValue.forEach(function (item) {
          this.addObj[item['field']] = ''
        }.bind(this))

        this.addColumns = tableColumns.filter(col => !col.hide).concat(this.extralFields)
        this.displayCols = tableColumns.filter(col => !col.nodisplay).concat(this.extralFields)
          .concat({ label: '操作', field: 'operate', name: 'operate', align: 'center', hide: true })
      }
    }
  },
  data () {
    return {
      data: [],
      displayCols: [], // table显示字段
      addColumns: [], // 添加时的字段
      show: false, // 是否打开弹框
      addName: 'add', // 添加计划弹框标识
      deliveryName: 'delivery', // 下发计划弹框标识
      modalName: 'add', // 当前弹框组件
      addBind: {
        width: '900px',
        height: '540px',
        title: '添加计划'
      },
      deliveryBind: {
        width: '500px',
        height: '480px',
        title: '下发计划'
      },
      selectWorkshop: '', // 当前要下发的车间code
      selectList: [], // 选中的计划
      planInOrder: [], // 计划下发排序
      addObj: {
        'task_no': '', // 必填
        'material_code': '', // 必填，选择
        'material_name': '', // 必填，选择
        'plan_count': 0, // 必填
        'plan_start_date': '',
        'comment': '',
        'workshop_name': '', // 必填，选择
        'workshop_code': ''
      },
      tomorow: date.formatDate(date.addToDate(Date.now(), { days: 1 }), 'YYYY-MM-DD'),
      deliveryObj: {
        product_line_code: '',
        plan_start_date: ''
      } // 下发
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData (show = false) { // 获取table数据
      http.planList(function (res) {
        if (this.responseValidate(res)) {
          this.data = res.data
          show && this.showNotify({ message: this.$t('message.refreshSuccessful') })
        }
      }.bind(this))
    },
    confirm () { // 点击弹框确认按钮时调用
      this[this.modalName]()
    },
    del (row) { // 确认删除
      this.showDialog({ message: this.$t('message.confirmDeletePlan') }, function () {
        this.deletePlan(row)
      }.bind(this))
    },
    deletePlan (row) { // 删除计划
      http.planDelete({ task_no: row['task_no'] }, function (res) {
        if (!this.responseValidate(res)) {
          return
        }
        const index = this.getPlanByCode(row['task_no'])
        index > -1 && this.data.splice(index, 1)
        this.showNotify({ message: this.$t('message.deleteSuccessful') })
      }.bind(this))
    },
    openAdd () { // 打开添加计划的界面
      this.clearObj(this.addObj)
      this.modalName = this.addName
      this.show = true
    },
    add () { // 添加计划
      if (!this.planValidate(this.addObj)) {
        return
      }
      http.planAdd(this.addObj, function (res) {
        if (!this.responseValidate(res)) {
          return
        }
        this.data.unshift(res.data)
        this.showNotify({ message: this.$t('message.addSuccessful') })
      }.bind(this))
    },
    planValidate (obj) { // 验证计划必填字段
      const fieldMap = this.field2name
      const fields = ['task_no', 'plan_count', 'material_name', 'material_code', 'material_unit', 'workshop_name']
      let msg = '' // 未赋值的必填字段
      fields.forEach(field => {
        !String(obj[field]).length && (msg += fieldMap[field] + ',')
      })
      if (msg) {
        msg = msg.substr(0, msg.length - 1)
        this.showNotify({ message: msg + this.$t('message.fieldsNotNull'), timeout: 2000 })
      }
      return !msg
    },
    selectChange (list) {
      if (Array.isArray(list)) {
        this.selectList = list
      }
    },
    validPlan () {
      http.validPlanStatus(this.selectList, function (res) {
        if (res.code === 'fail') {
          this.showNotify({ message: res.info })
          this.clearSelectList()
          this.getData(true)
        } else if (res.code === 'success') {
          this.startDispatch()
        }
      }.bind(this))
    },
    clearSelectList () { // 清空table选中项
      this.$refs['plan_table'].clearSelectList()
      this.selectChange([])
    },
    openDelivery () {
      this.validPlan()
    },
    startDispatch () { // 打开下发计划界面
      const list = this.selectList
      if (!list.length) {
        this.showNotify({ message: this.$t('message.noSelectPlan') })
        return
      }
      // 选中计划的车间信息 验证
      if (!this.validateWorkshop(list)) {
        return
      }

      // 初始化
      this.deliveryObj['product_line_code'] = ''
      this.deliveryObj['plan_start_date'] = this.tomorow
      this.selectWorkshop = list[0]['workshop_code']
      this.modalName = this.deliveryName
      this.show = true
    },
    validateWorkshop (selectList) { // 验证要下发的车间信息
      let workshopCodes = []
      selectList.forEach(item => {
        !workshopCodes.includes(item['workshop_code']) && workshopCodes.push(item['workshop_code'])
      })
      let errMsg
      if (workshopCodes.length > 1) {
        errMsg = this.$t('message.multipleWorkshopDispatch')
      } else if (workshopCodes.length === 0) {
        errMsg = this.$t('message.noWorkshopDispatch')
      } else if (!this.workshops[workshopCodes[0]]) {
        errMsg = this.$t('message.invalidWorkshop')
      }
      errMsg && this.showNotify({ message: errMsg })

      return !errMsg
    },
    delivery () { // 下发计划
      const param = Object.assign({
        'task_no_list': this.selectList.map(item => item['task_no']),
        'task_seq_list': this.planInOrder
      }, this.deliveryObj)
      http.planDispatch(param, function (res) {
        if (!this.responseValidate(res)) {
          return
        }
        this.clearSelectList()
        this.updatePlan(res.data)
        this.showNotify({ message: this.$t('message.dispatchSuccessful') })
      }.bind(this), function () {
        this.clearSelectList()
      }.bind(this))
    },
    back (row) { // 确认回退计划
      this.showDialog({ message: this.$t('message.confirmRollbackPlan') }, function () {
        this.rollbackPlan(row)
      }.bind(this))
    },
    rollbackPlan (row) { // 回退计划
      http.planRollback({ task_no: row['task_no'] }, function (res) {
        if (!this.responseValidate(res)) {
          return
        }
        this.updatePlan([res.data])
        this.showNotify({ message: this.$t('message.rollbackSuccessful') })
      }.bind(this))
    },
    updatePlan (planList = []) { // 批量更新计划
      if (!planList.length) {
        return
      }
      for (let i = 0; i < planList.length; i++) {
        const index = this.getPlanByCode(planList[i]['task_no'])
        index > -1 && this.data.splice(index, 1, planList[i])
      }
    },
    getPlanByCode (code) { // 根据code获取计划信息
      let index = -1
      if (!this.data.length) {
        return index
      }

      for (let i = 0; i < this.data.length; i++) {
        if (this.data[i]['task_no'] === code) {
          index = i
          break
        }
      }
      return index
    }
  }
}
</script>
