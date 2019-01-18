<template>
  <div class="report-list row justify-around">
    <template v-for="plan in reportPlan">
      <div
        :class="['plan-item q-pa-sm cursor-pointer', reportPlan.length > 3 ? 'col-4' : 'col']"
        :style="{
         'border-color': planCode === plan.plan_number ? 'rgb(2, 123, 227)' : '#ccc',
         'background': planCode === plan.plan_number ? 'rgba(2, 123, 227, .3)' : 'transparent'
        }"
        @click="changePlan(plan.plan_number)">
        <q-list class="col-auto" dark dense no-border>
          <q-list-header :class="['detail-material text-bold', {'text-primary': planCode === plan.plan_number}]">{{plan.material_name}}</q-list-header>
          <q-item class="q-title">
            <q-item-side>
              <q-item-tile>计划号：</q-item-tile>
            </q-item-side>
            <q-item-main class="text-right">
              <q-item-tile>{{plan.plan_number}}</q-item-tile>
            </q-item-main>
          </q-item>
          <q-item class="q-title">
            <q-item-side>
              <q-item-tile>计划数：</q-item-tile>
            </q-item-side>
            <q-item-main class="text-right">
              <q-item-tile>{{plan.plan_count}}</q-item-tile>
            </q-item-main>
          </q-item>
          <q-item class="q-title">
            <q-item-side>
              <q-item-tile>合&nbsp;&nbsp;&nbsp;格：</q-item-tile>
            </q-item-side>
            <q-item-main class="text-right">
              <q-item-tile>{{plan.qualified_count}}</q-item-tile>
            </q-item-main>
          </q-item>
          <q-item class="q-title">
            <q-item-side>
              <q-item-tile>不合格：</q-item-tile>
            </q-item-side>
            <q-item-main class="text-right">
              <q-item-tile>{{plan.unqualified_count}}</q-item-tile>
            </q-item-main>
          </q-item>
          <q-item class="q-title">
            <q-item-side>
              <q-item-tile>进&nbsp;&nbsp; 度：</q-item-tile>
            </q-item-side>
            <q-item-main class="text-right">
              <q-item-tile>{{plan.plan_progress}}</q-item-tile>
            </q-item-main>
          </q-item>
        </q-list>
        <!--<template v-for="col in cols">-->
          <!--<template v-if="col.field === 'material_name'">-->
            <!--<div class="q-list-header q-headline">{{plan[col.field]}}</div>-->
          <!--</template>-->
          <!--<div v-else class="row no-wrap justify-between plan-row">-->
            <!--<span>{{ col.name }}:</span>-->
            <!--<span>{{ plan[col.field] }}</span>-->
          <!--</div>-->
        <!--</template>-->
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
        { name: '物料名称', field: 'material_name' },
        { name: '计划号', field: 'plan_number' },
        { name: '计划数', field: 'plan_count' },
        { name: '合格', field: 'qualified_count' },
        { name: '不合格', field: 'unqualified_count' },
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
  .report-list
    flex-wrap nowrap
    overflow auto
  .plan-item
    border-width 2px
    border-style solid
    border-radius 4px
    margin-right 8px
    .detail-material
      font-size 20px
      padding 0 0 8px 0
      min-height 0
    &:last-child
      margin-right 0
</style>
