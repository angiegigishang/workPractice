<template>
  <div class="full-height column text-center text-bold table">
    <div class="table-header row items-center bg-primary">
      <template v-for="col in cols">
        <div class="col">{{ col.name }}</div>
      </template>
    </div>
    <div class="table-body">
      <template v-for="row in data">
        <div class="row no-wrap items-center row-height">
          <template v-for="col in cols">
            <div class="col">
              {{ row[col.field] === null ? '/' : row[col.field] }}
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
    }
  }
}
</script>

<style lang="stylus" scoped>
  .table
    font-size 12px
    .table-header
      height 36px
      line-height 36px
      color #fff
    .row-height
      height 38px
      border-bottom 1px solid #505778
      border-style solid
      border-color #9B9CBC
      border-width 0 1px 1px
      color: #999

</style>
