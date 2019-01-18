<template>
  <div class="row plan-box">
    <div class="column q-mr-sm">
      <div class="q-pa-sm plan" v-for="number in plans.length">{{ number }}</div>
    </div>
    <div class="column col">
      <!-- 不可排序的计划 -->
      <div class="column">
        <div class="q-pa-sm cursor-pointer plan" v-for="item in dispatchedPlans" :data-no="item.task_no">
          {{ `${item.task_no}(${item.material_name})` }}
          <div class="inline-block q-ml-md plan-no-drag">{{ planStatusList[String(item.plan_status)] }}</div>
        </div>
      </div>
      <!-- 排序计划 -->
      <div class="column plan-container">
        <div class="q-pa-sm cursor-pointer plan" v-for="item in undispathedPlans" :data-no="item.task_no">
          {{ `${item.task_no}(${item.material_name})` }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Dragula from 'dragula/dragula'
import 'dragula/dist/dragula.css'
import { planStatusList } from 'assets/constant'
export default {
  props: {
    plans: {
      type: Array,
      default: () => []
    },
    planOrder: {
      type: Array,
      default: () => []
    }
  },
  watch: {
    plans: {
      immediate: true,
      handler (newValue) {
        this.dispatchedPlans = []
        this.undispathedPlans = []
        if (!Array.isArray(newValue)) {
          return []
        }
        this.plans.forEach(function (item) {
          const status = String(item['plan_status'])
          if (status === '2' || status === '4') { // 不可排序
            this.dispatchedPlans.push(item)
          } else {
            this.undispathedPlans.push(item)
          }
        }.bind(this))
      }
    }
  },
  data () {
    return {
      dispatchedPlans: [], // 不可排序的计划：进行中、已完工
      undispathedPlans: [], // 可排序的计划
      dragula: null,
      planStatusList
    }
  },
  destroyed () {
    this.dragula && this.dragula.destroy()
  },
  mounted () {
    this.dragListener()
  },
  methods: {
    dragListener () {
      this.dragula = Dragula([this.$el.querySelector('.plan-container')])
        .on('dragend', function (el) {
          const siblings = el.parentNode.childNodes
          let list = Array.prototype.map.call(siblings, function (item) { return item.dataset.no })
          list = this.dispatchedPlans.map(item => item['task_no']).concat(...list)
          this.planOrder.splice(0, this.planOrder.length, ...list)
        }.bind(this))
    }
  }
}
</script>

<style lang="stylus" scoped>
@import "~variables"
.plan-box
  border 1px solid #e1e1e1
  .plan
    border-width 1px
    border-color #e1e1e1
    border-style solid
    user-select none
    margin 2px 0
    height 40px
    box-sizing border-box
  .plan-disable
    border-color #f00
  .plan-no-drag
    color $info
</style>
