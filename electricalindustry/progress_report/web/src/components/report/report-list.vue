<template>
  <div class="row justify-around">
    <template v-for="plan in reportPlan">
      <div
        class="col plan-item q-pa-sm cursor-pointer"
        :style="{
         'border-color': planCode === plan.plan_number ? 'rgb(2, 123, 227)' : '#ccc',
         'color': planCode === plan.plan_number ? 'white' : '#e2dbdb',
         'background': planCode === plan.plan_number ? 'rgba(2, 123, 227, .3)' : 'transparent'
        }"
        @click="changePlan(plan.plan_number)">
        <template v-for="col in cols">
          <div class="row no-wrap justify-between plan-row">
            <span>{{ col.name }}</span>
            <span>{{ plan[col.field] }}</span>
          </div>
        </template>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  props: {
    reportPlan: {
      type: Array,
      default: () => []
    },
    planCode: {
      type: String
    }
  },
  data () {
    return {
      cols: [
        { name: '计划号', field: 'plan_number' },
        { name: '物料名称', field: 'material_name' },
        { name: '计划生产数量', field: 'plan_count' },
        { name: '合格数', field: 'qualified_count' },
        { name: '不合格数', field: 'unqualified_count' },
        { name: '进度', field: 'plan_progress' }
      ]
    }
  },
  methods: {
    changePlan (plan) {
      this.$emit('update:planCode', plan)
    }
  }
}
</script>

<style lang="stylus" scoped>
  .plan-item
    border-width 2px
    border-style solid
    border-radius 4px
    margin-right 8px
    &:last-child
      margin-right 0
</style>
