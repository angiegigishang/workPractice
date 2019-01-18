<template>
  <div class="full-height text-center text-bold table">
    <div class="table-header row items-center bg-primary topFix" v-show="fixed">
      <div class="col"></div>
      <template v-for="head in headers">
        <div class="col">{{ head }}</div>
      </template>
    </div>
    <div class="table-header row items-center bg-primary">
      <div class="col"></div>
      <template v-for="head in headers">
        <div class="col">{{ head }}</div>
      </template>
    </div>
    <div class="table-body">
      <template v-for="item in data.length > 0 ? [...data,...data, '累计'] : data">
        <div class="row no-wrap items-center row-height">
          <div class="col">{{item.date ? item.date : '累计'}}</div>
          <template v-for="(head,idx) in headers">
            <div class="col">
              {{ item.data === undefined || item.data[head] === undefined ?
              (item === '累计' ? totals[idx] :'/' ) : `${
                item.data[head].qualified_count !== undefined ?
                item.data[head].qualified_count : ''}/${
                item.data[head].unqualified_count !== undefined ?
                item.data[head].unqualified_count : ''}
              ` }}
            </div>
          </template>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    data: {
      type: Array,
      default: () => []
    },
    headers: {
      type: Array,
      default: () => []
    }
  },
  data () {
    return {
      fixed: false
    }
  },
  created () {
    document.getElementById('q-app').addEventListener('scroll', this.scrollTop)
  },
  beforeDestroy () {
    document.getElementById(('q-app')).removeEventListener('scroll', this.scrollTop)
  },
  methods: {
    scrollTop () {
      if (document.getElementById('q-app').scrollTop >= 92) {
        this.fixed = true
      } else if (document.getElementById('q-app').scrollTop < 92) {
        this.fixed = false
      }
    }
  },
  computed: {
    totals () {
      return this.$props.headers.map((val, idx) => {
        let qualifiedTotal = 0
        let unqualifiedTotal = 0
        let qflag = false
        let uqflag = false
        for (let i = 0, len = this.$props.data.length; i < len; i++) {
          if (this.$props.data[i].data[val]) {
            if (this.$props.data[i].data[val].unqualified_count !== undefined) {
              uqflag = true
              unqualifiedTotal += this.$props.data[i].data[val].unqualified_count
            }
            if (this.$props.data[i].data[val].qualified_count !== undefined) {
              qflag = true
              qualifiedTotal += this.$props.data[i].data[val].qualified_count
            }
          }
        }
        let qualify = '', unqualify = ''
        if (qflag) {
          qualify = qualifiedTotal
        }
        if (uqflag) {
          unqualify = unqualifiedTotal
        }
        return `${qualify}/${unqualify}`
      })
    }
  }
}
</script>

<style lang="stylus" scoped>
  .table
    font-size 20px
    .table-header
      /*height 36px*/
      /*line-height 36px*/
    .row-height
      /*height 38px*/
      /*line-height 38px*/
      border-bottom 1px solid #505778
      background-color rgba(102, 112, 140, .3)
      border-style solid
      border-color #9B9CBC
      border-width 0 1px 1px
      &:last-child
        margin-bottom 40px
    .col
      word-break break-all
      height  auto
      padding 10px
    .topFix
      position  fixed
      top 0
      left 50%
      transform translateX(-50%)
      width calc(100% - 32px)
      z-index 999
</style>
