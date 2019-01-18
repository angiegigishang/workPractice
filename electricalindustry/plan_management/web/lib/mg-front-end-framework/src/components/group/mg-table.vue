<template>
  <q-table
    :data="data"
    :columns="columns"
    :row-key="rowKey"
    :filter="filter"
    :pagination.sync="pagination"
    :hide-bottom="hide"
    :selection="selection"
    :selected.sync="selectedRows"
    :rows-per-page-options="rowsOption"
    :no-data-label="$t('message.noData')"
    :rows-per-page-label="$t('message.pageLable')"
    :filter-method="filterFunc">

    <div :slot="search ? 'top-left' : 'toppp'" slot-scope="props">
      <q-search
        :debounce="600"
        hide-underline
        color="secondary"
        v-model="filter"
        class="col-6"
        :placeholder="searchLable"/>
    </div>

    <template :slot="topRight ? 'top-right' : 'toppp'" slot-scope="props">
      <slot name="top-right"/>
    </template>

    <template :slot="`body-cell-${col.name}`" v-for="col in columns" slot-scope="props">
      <q-td :class="`text-${col.align}`">
        <slot :name="`body-cell-${col.name}`" :row="props.row" :col="props.col" :pagination="pagination">
          {{props.row[col.name]}}
        </slot>
      </q-td>
    </template>

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
</template>

<script>
import {QTable, QSearch, QBtn, QTd} from 'quasar'

export default {
  name: 'MgTable',
  components: {
    QTable, QSearch, QBtn, QTd
  },
  props: {
    search: {
      type: Boolean,
      default: false
    },
    topRight: {
      type: Boolean,
      default: false
    },
    searchLable: {
      type: String,
      default: 'Search'
    },
    hideBottom: {
      type: Boolean,
      default: false
    },
    rowsOption: {
      type: Array,
      default: function () {
        return [5, 10, 15, 20, 30, 50, 0]
      }
    },
    data: {
      type: Array,
      default: () => []
    },
    columns: {
      type: Array,
      default: () => []
    },
    rowKey: {
      type: String,
      default: ''
    },
    selection: {
      type: String,
      default: 'none'
    },
    initSelected: {
      type: [Array, Object],
      default: () => []
    }
  },
  computed: {
    hide () {
      return this.hideBottom && !!this.data.length
    }
  },
  watch: {
    initSelected (newV) {
      const type = typeof newV
      if (!newV || type !== 'object') {
        return
      }

      this.selectedRows = this.getRowData(newV)
    },
    selectedRows (newV) {
      this.$emit('select-change', newV)
    }
  },
  mounted () {
    this.selectedRows = this.getRowData(this.initSelected)
  },
  data () {
    return {
      select: 5,
      filter: '',
      selectedRows: [],
      loading: false,
      pagination: {
        page: 1, // 当前显示的页号
        rowsPerPage: this.rowsOption[0] // 当前页显示的行数
      }
    }
  },
  methods: {
    getRowData (obj) {
      if (obj instanceof Array) {
        const arr = []
        for (let i = 0; i < obj.length; i++) {
          const temp = this.getFromTableData(obj[i])
          temp && arr.push(temp)
        }
        return arr
      } else {
        const temp = this.getFromTableData(obj)
        return temp ? [].concat(temp) : []
      }
    },
    getFromTableData (obj) {
      let resultObj
      const keys = Object.keys(obj)
      const arr = this.data
      const len = arr.length
      for (let i = 0; i < len; i++) {
        const o = arr[i]
        let flag = true
        keys.forEach(function (key) {
          flag = flag && obj[key] === o[key]
        })
        if (flag) {
          resultObj = o
          break
        }
      }
      return resultObj
    },
    filterFunc (rows, terms, cols, cellValue) {
      if ('filter-method' in this.$listeners) {
        return this.$listeners['filter-method'](rows, terms, cols, cellValue)
      } else {
        return rows
      }
    }
  }
}
</script>
