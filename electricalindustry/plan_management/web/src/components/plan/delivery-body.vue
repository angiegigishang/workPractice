<template>
  <div class="q-ma-md">
    <q-select :value="data.product_line_code"
              @input="piplineHandler"
              class="q-mt-md"
              :float-label="$t('label.selectPipeline')"
              :options="pipelines" />

    <date-picker :disabled="!data.product_line_code"
                 class="q-my-md"
                 :value="data.plan_start_date"
                 @input="inputHandler"
                 placeholder="计划开工日期"
                 :format="format"></date-picker>

    <plan-sort :plans="sortedPlans" :plan-order="planInOrder"></plan-sort>
  </div>
</template>

<script>
import { date } from 'quasar'
import { mapState } from 'vuex'
import PlanSort from './plan-sort'
import http from 'http/plan'
export default {
  components: {
    PlanSort
  },
  props: {
    data: {
      type: Object,
      default: () => {}
    },
    plans: { // 待下发的计划
      required: false,
      type: Array
    },
    planInOrder: { // 计划code排序
      required: false,
      type: Array
    },
    workshop: { // 下发车间
      type: String,
      default: ''
    }
  },
  data () {
    return {
      sortedPlans: this.plans,
      format: 'YYYY-MM-DD'
    }
  },
  watch: {
    plans (newValue) { // 下发界面没下发退出后重新进入下发界面出发, 用于清空之前的计划
      this.sortedPlans = newValue
    }
  },
  computed: {
    ...mapState(['workshops']),
    pipelines () {
      if (!this.workshops[this.workshop]) {
        return []
      }
      const list = this.workshops[this.workshop]['pipelines'] || []
      return list.map(item => ({ label: item.product_line_name, value: item.product_line_code }))
    }
  },
  methods: {
    inputHandler (value) {
      this.data.plan_start_date = date.formatDate(value, this.format)
      this.getPlans()
    },
    piplineHandler (value) {
      this.data.product_line_code = value
      this.getPlans()
    },
    getPlans () {
      http.getSpecifiedPlan(this.data.product_line_code, this.data.plan_start_date, function (res) {
        if (this.responseValidate(res)) {
          this.sortedPlans = (res.data || []).concat(this.plans)
        }
      }.bind(this))
    }
  }
}
</script>
