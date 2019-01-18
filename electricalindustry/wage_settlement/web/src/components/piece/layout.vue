<template>
  <div class="row justify-center q-mt-md">
    <!--<mg-table-->
      <!--style="width: 80%"-->
      <!--:columns="columns"-->
      <!--:data="tableData"-->
      <!--:search="true"-->
      <!--:rows-option="[0]"-->
      <!--row-key="code"-->
      <!--v-on:filter-method="filterMethod"-->
      <!--:hide-bottom="true">-->
      <!--<template slot="body-cell-process" slot-scope="props">-->
        <!--<div class="cursor-pointer" style="text-decoration: underline;" @click="rowClick(props.row)">-->
            <!--{{ props.row.process }}-->
          <!--</div>-->
      <!--</template>-->
    <!--</mg-table>-->
    <q-table
      class="common-table"
      style="width: 80%"
      color="secondary"
      :columns="columns"
      :data="tableData"
      :filter="filter"
      :loading="loading"
      :no-data-label="$t('message.noData')"
      :pagination.sync="paginationControl"
      :hide-bottom="true"
      row-id="code">
        <template slot="top-left" slot-scope="props">
          <q-search color="secondary" v-model="filter"></q-search>
        </template>
      <tr slot="header" slot-scope="props">
        <template v-for="col in tableHead">
          <q-th :key="col.name" :props="props">
            {{col.label}}
            <!--<q-btn v-if="col.materialsList" label="物料列表">-->
              <q-icon class="cursor-pointer" v-if="col.materialsList" color="secondary" name="group_work">
                <q-popover
                  anchor="bottom left"
                  self="top left">
                  <template v-for="material in col.materialsList">
                    <div class="material-item">{{ material }}</div>
                  </template>
                </q-popover>
              </q-icon>
            <!--</q-btn>-->
          </q-th>
        </template>
      </tr>
        <q-td slot="body-cell-process"
              slot-scope="props"
              class="cursor-pointer text-center"
              style="text-decoration: underline;">
          <div @click="rowClick(props.row)">
            {{ props.row.process }}
          </div>
        </q-td>
      </q-table>
    <modal
      :mapper="mapper"
      :dialog-show.sync="showDialog"
      :dialog-data="currentModalData"
      @update-table="updateTable"></modal>
    <q-page-sticky v-if="personCode" position="top-right" :offset="[30, 18]">
      <q-btn round color="secondary" @click="$router.push('/wage')" icon="reply" />
    </q-page-sticky>
  </div>
</template>

<script>
import api from 'http/serverRequests'
import modal from './priceModifyModal'
import { mapMutations } from 'vuex'
export default {
  name: 'piece',
  components: {
    modal
  },
  computed: {
    // 人员code
    personCode () {
      return this.$route.query.person_code
    },
    // 表格头部详情col
    tableHead () {
      return this.columns.map(o => {
        let oMapper = this.mapper.find(m => m.code === o.field)
        return oMapper ? { ...o, materialsList: oMapper.materiel_names } : {...o}
      })
    }
  },
  data () {
    return {
      tableData: [],
      columns: [],
      mapper: [],
      filter: '',
      loading: false,
      paginationControl: {
        rowsPerPage: 0,
        page: 1
      },
      showDialog: false,
      currentModalIndex: -1,
      currentModalData: {},
      form: {}
    }
  },
  watch: {
    personCode () {
      this.getList()
    }
  },
  created () {
    // 更新导航标题
    this.updateNavTitle(this.$t('title.piece'))
    this.getList()
  },
  methods: {
    ...mapMutations(['updateNavTitle']),
    // 初始获取数据
    getList () {
      this.loading = true
      // 获取列表数据
      api.getPriceMapper(this.personCode, this.initTable)
    },
    initTable (data) {
      this.loading = false
      if (data.data) {
        this.mapper = data.data.mapper
        this.columns = data.data.columns.map(o => {
          return {
            ...o,
            align: 'center'
          }
        })
        this.tableData = data.data.rows
      }
    },
    rowClick (row) {
      this.showDialog = true
      this.currentModalData = row
    },
    updateTable (form) {
      console.log(form)
      api.updatePriceMapper(form, function (res) {
        if (this.responseValidate(res)) {
          // 更新数据
          let nIndex = this.currentModalData.__index
          this.tableData.splice(nIndex, 1, {
            ...this.tableData[nIndex],
            ...form
          })
          // 修改数据
          this.showDialog = false
          this.currentModalData = null
          this.showNotify({
            message: this.$t('message.success'),
            color: 'positive'
          })
        }
      }.bind(this))
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

<style lang="stylus">
  .q-table
    tbody
      td
        padding 0
        height 42px
  .material-item
    line-height 30px
    padding 4px 6px
    cursor pointer
    &:hover
     background-color #dedede
</style>
