<template>
  <div class="relative-position">
    <q-table :data="data"
             :filter="filter"
             row-key="task_no"
             class="mg-table"
             :columns="columns"
             :selection="selectionMode"
             :selected.sync="selectList"
             :pagination.sync="pagination"
             :rows-per-page-options="rowsOption"
             :no-data-label="$t('message.noData')"
             :no-results-label="$t('message.noMatchedData')"
             :selected-rows-label="getSelectedLabel"
             :rows-per-page-label="$t('message.pageLable')">
      <template slot="top-left" slot-scope="props">
        <q-search
          hide-underline
          color="secondary"
          v-model="filter"
          class="col-6" />
      </template>
      <q-td slot="body-cell-plan_status" slot-scope="{ row, col }" :class="`text-${col.align}`">
        {{ planStatusList[String(row.plan_status)] }}
      </q-td>
      <q-td slot="body-cell-plan_type" slot-scope="{ row, col }" :class="`text-${col.align}`">
        {{ planTypeList[String(row.plan_type)] }}
      </q-td>
      <q-td slot="body-cell-operate" slot-scope="{ row, col }" class="operate-width">
        <div style="height: 24px" class="operate-width"></div>
      </q-td>
      <template slot="pagination" slot-scope="props" class="row flex-center q-py-sm">
        <q-btn
          round dense size="sm" icon="keyboard_arrow_left" color="secondary" class="q-mr-sm"
          :disable="props.isFirstPage"
          @click="props.prevPage"
        />
        <div class="q-mr-sm"> {{ props.pagination.page }} / {{ props.pagesNumber }}</div>
        <q-btn
          round dense size="sm" icon="keyboard_arrow_right" color="secondary"
          :disable="props.isLastPage"
          @click="props.nextPage"
        />
      </template>
    </q-table>
    <div v-if="pagePlans.length"
         class="operate-width absolute-right"
         style="top: 65px;bottom: 48px;">
      <div style="background-color: #fff;" class="column">
        <div style="height: 56px;line-height: 56px;color: #757575;"
             class="full-width text-center font-12 col-bottom">操作</div>
        <div v-for="row in pagePlans" style="height: 48px;border-left: 1px solid #D7D7D7"
             class="full-width text-center row justify-center items-center operate-fix col-bottom">
          <q-btn :label="$t('label.delivery')"
                 :color="(row.plan_status === 0 || row.plan_status === 3) ? 'secondary' : 'grey'"
                 :disable="(row.plan_status !== 0 && row.plan_status !== 3)"
                 class="no-shadow"
                 dense outline
                 @click="confirm('dispatch', row)" />
          <q-btn :label="$t('label.delete')"
                 :color="(row.plan_status === 1 || row.plan_status === 3) ? 'grey' : 'secondary'"
                 :disable="(row.plan_status === 1 || row.plan_status === 3)"
                 dense outline
                 class="no-shadow q-mx-sm"
                 @click="confirm('delete', row)" />
          <q-btn :label="$t('label.back')"
                 :color="row.plan_status === 1 ? 'secondary' : 'grey'"
                 :disable="row.plan_status !== 1"
                 dense outline
                 class="no-shadow"
                 @click="confirm('rollback', row)" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { planStatusList, planTypeList } from 'assets/constant'
export default {
  props: {
    data: {
      type: Array,
      default: () => []
    },
    columns: {
      type: Array,
      default: () => []
    },
    selectChange: {
      type: Function,
      require: true
    }
  },
  data () {
    return {
      planStatusList,
      planTypeList,
      selectList: [], // 选中行
      filter: '', // 搜索字段
      rowsOption: [10, 20, 30],
      pagination: {
        page: 1, // 当前显示的页号
        rowsPerPage: 10 // 当前页显示的行数
      },
      pagePlans: [] // 当前页计划
    }
  },
  watch: {
    selectList (newValue) {
      this.selectChange(newValue)
    },
    data: {
      immediate: true,
      handler (newList) {
        this.setPagePlans(newList)
      }
    },
    'pagination.page' () {
      this.setPagePlans()
    }
  },
  computed: {
    selectionMode () {
      return this.data.length ? 'multiple' : 'none'
    }
  },
  methods: {
    setPagePlans (list) {
      list = list || this.data
      if (!Array.isArray(list)) {
        return
      }
      const start = (this.pagination.page - 1) * this.pagination.rowsPerPage
      this.pagePlans = Array.prototype.slice.call(list, start, start + this.pagination.rowsPerPage)
    },
    confirm (funcName, row) { // funcName： dispatch, delete, rollback
      if (funcName === 'dispatch') {
        this.selectList = [row]
      }
      this.$emit(funcName, row)
    },
    getSelectedLabel (num) {
      return `已选中${num}行`
    },
    clearSelectList () {
      this.selectList.splice(0, this.selectList.length)
    }
  }
}
</script>

<style lang="stylus" scoped>
.operate-width
  width 150px
.col-bottom
  border-bottom 1px solid #D7D7D7
  box-sizing border-box
.operate-fix:nth-child(even)
  background-color #f5f5f5
</style>
<style lang="stylus">
.mg-table
  .q-table .q-input input
    text-align center
    width 80px
  .q-table th, .q-table td
    padding 7px 7px
  .q-table tbody tr:nth-child(odd)
    background-color #f5f5f5
</style>
