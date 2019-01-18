<template>
  <div class="relative-position" :class="{'high-level': show === 'plan'}">
    <div v-if="data.length > 0" class="row justify-center q-my-sm">
      <div class="col q-px-sm plan-wrapper" v-for="plan in data" :key="plan.planId" :class="{'active': plan.isWorking}">
        <div class="row justify-between items-center plan-content relative-position">
          <q-list class="col-auto" dark dense no-border>
            <q-list-header class="text-bold">{{plan.planProduct}}</q-list-header>
            <q-item class="q-body-2">
              <q-item-side>
                <q-item-tile>计划号：</q-item-tile>
              </q-item-side>
              <q-item-main>
                <q-item-tile>{{plan.planId}}</q-item-tile>
              </q-item-main>
            </q-item>
            <q-item class="q-body-2">
              <q-item-side>
                <q-item-tile>计划数：</q-item-tile>
              </q-item-side>
              <q-item-main>
                <q-item-tile>{{plan.planNum}}</q-item-tile>
              </q-item-main>
            </q-item>
            <q-item class="q-body-2">
              <q-item-side>
                <q-item-tile>合&nbsp;&nbsp;&nbsp;&nbsp;格：</q-item-tile>
              </q-item-side>
              <q-item-main>
                <q-item-tile>{{plan.positive_num}}</q-item-tile>
              </q-item-main>
            </q-item>
            <q-item class="q-body-2">
              <q-item-side>
                <q-item-tile>不合格：</q-item-tile>
              </q-item-side>
              <q-item-main>
                <q-item-tile>{{plan.negative_num}}</q-item-tile>
              </q-item-main>
            </q-item>
          </q-list>
          <div class="col-auto absolute-right">
            <plan-chart :planNum="plan.planNum" :positive="plan.positive_num" :progressColor="plan.progress_color"></plan-chart>
          </div>
        </div>
    </div>
    </div>
    <!--<div v-if="data.length === 0" class="text-center q-py-lg">暂无计划</div>-->
    <m-mask v-show="show !== 'all' && show !== 'plan'"></m-mask>
  </div>
</template>

<script>
import PlanChart from './plan-chart'
import MMask from './m-mask'
export default {
  props: {
    data: {
      type: Array,
      default: () => []
    },
    show: {
      type: String,
      default: 'all'
    }
  },
  components: {
    PlanChart,
    MMask
  }
}
</script>

<style lang="stylus" scoped>
@import '~variables'
.high-level
  z-index 9
.plan-wrapper
  height 179px
  box-sizing border-box
  border-radius 8px
.plan-content
  box-sizing border-box
  border-width 1px
  border-style solid
  border-color #555
  border-radius 8px
.active
  .plan-content
    border-width 2px
    border-color rgb(2, 123, 227)
    background rgba(2, 123, 227, .3)
</style>
