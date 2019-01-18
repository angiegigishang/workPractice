<template>
  <div class="full-height text-center text-bold table">
    <div class="table-header row items-center bg-primary">
      <div class="col">姓名</div>
      <template v-for="col in cols">
        <div class="col">{{ col.name }}</div>
      </template>
    </div>
    <div class="table-body">
      <template v-for="row in data">
        <div class="row no-wrap items-center row-height">
          <div class="col">{{row['name']}}</div>
          <template v-for="colitem in cols">
            <div :class="[{col:true}, {colred: colitem.field == 'absent' && row['absent'] >= 3}]" >
              {{ row[colitem.field] === null ? '/' : row[colitem.field] }}
              <!--<slot :name="field" v-bind="{col, row}"></slot>-->
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
    cols: {
      type: Array,
      default: () => []
    },
    hname: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      isabcent: false
    }
  }
}
</script>

<style lang="stylus" scoped>
  .table
    font-size 20px
    .table-header
      min-height 36px
      /*line-height 36px*/
      border-radius 2px
      .col
        word-break break-all
        padding 10px
    .row-height
      min-height 38px
      /*line-height 38px*/
      border-bottom 1px solid #505778
      background-color rgba(102, 112, 140, .3)
      border-style solid
      border-color #9B9CBC
      border-width 0 1px 1px
      border-radius 4px
  .colred
     color: red;
</style>
