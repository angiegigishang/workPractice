<template>
  <div class="row justify-center q-mt-md">
    <mg-table
      class="common-table"
      style="width: 80%"
      :columns="columns"
      :data="tableData"
      :search="true"
      :rows-option="[0]"
      row-key="person_code"
      :hide-bottom="true"
      v-on:filter-method="filterMethod">
      <template slot="body-cell-price" slot-scope="props">
        <q-input v-model="props.row.price"></q-input>
      </template>
      <template slot="body-cell-operate" slot-scope="props">
        <q-btn color="secondary" :label="$t('button.confirm')" @click="updateChange(props.row)"></q-btn>
      </template>
    </mg-table>
    <q-page-sticky v-if="personCode" position="top-right" :offset="[30, 18]">
      <q-btn round color="secondary" @click="$router.push('/wage')" icon="reply" />
    </q-page-sticky>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'
import http from 'http/serverRequests'
export default {
  data () {
    return {
      columns: [
        { name: 'person_name', label: this.$t('table.time.person_name'), field: 'person_name', align: 'center' },
        { name: 'wage_name', label: this.$t('table.time.wage_name'), field: 'wage_name', align: 'center' },
        { name: 'price', label: this.$t('table.time.price'), field: 'price', align: 'center' },
        { name: 'operate', label: this.$t('table.time.operate'), field: 'price', align: 'center' }
      ],
      tableData: []
    }
  },
  computed: {
    personCode () {
      return this.$route.query.person_code
    }
  },
  watch: {
    personCode () {
      this.getList()
    }
  },
  created () {
    this.updateNavTitle(this.$t('title.time'))
    this.getList()
  },
  methods: {
    ...mapMutations(['updateNavTitle']),
    // 获取展示数据
    getList () {
      http.getTimelyWage(this.personCode, res => {
        if (this.responseValidate(res)) {
          this.tableData = res.data || []
        }
      })
    },
    // 更新数据
    updateChange (row) {
      http.updateTimelyWage({
        person_code: row.person_code,
        wage_code: row.wage_code,
        price: row.price
      }, res => {
        if (this.responseValidate(res)) {
          this.showNotify({
            message: this.$t('message.success'),
            color: 'positive'
          })
        }
      })
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
</style>
