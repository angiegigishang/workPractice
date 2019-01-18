<template>
  <div class="row">
    <template v-for="col in cols">
      <div class="col-6 q-my-sm font-14 col-box">
        <span class="col-label"><span class="required" v-if="col.focus">*</span>{{ col.label }}</span>
        <div class="inline-block col-width" v-if="col.type === 'date'">
          <date-picker :value="data[col.field]"
                       class="col-width"
                       @input="timeChange(col.field, $event)"
                       :format="dateFormat"></date-picker>
        </div>
        <div v-else-if="col.type === 'select'" class="inline-block col-width">
          <q-select v-if="col.field === 'material_name'"
                    v-model="data[col.field]"
                    :options="materialOptions"></q-select>
          <q-select v-else-if="col.field === 'workshop_name'"
                    v-model="data[col.field]"
                    :options="workshopOptions"></q-select>
        </div>
        <input v-else
               :type="col.type || 'text'"
               :disabled="!!col.disable"
               v-model="data[col.field]"
               class="col-input col-width">
      </div>
    </template>
  </div>
</template>

<script>
import { date } from 'quasar'
import { mapState } from 'vuex'
export default {
  props: {
    data: {
      type: Object,
      default: () => {}
    },
    cols: {
      type: Array,
      default: () => []
    }
  },
  data () {
    return {
      dateFormat: 'YYYY-MM-DD'
    }
  },
  computed: {
    ...mapState(['materials', 'workshops']),
    materialOptions () {
      if (!this.materials) {
        return []
      }
      const codes = Object.keys(this.materials)
      return codes.map(item => ({ label: item, value: item }))
    },
    workshop2code () {
      let result = {}
      const workshopObj = this.workshops
      if (!workshopObj) {
        return result
      }

      const codes = Object.keys(workshopObj)
      codes.forEach(code => (result[workshopObj[code].name] = code))
      return result
    },
    workshopOptions () {
      const names = Object.keys(this.workshop2code)
      return names.map(name => ({ label: name, value: name }))
    }
  },
  watch: {
    // 'data.material_name' (newValue) { // 物料名称变化时，同步修改物料编码和物料单位
    //   if (!newValue) {
    //     return
    //   }
    //   this.data['material_code'] = this.materials[newValue].code
    //   this.data['material_unit'] = this.materials[newValue].unit
    // },
    'data.workshop_name' (newValue) { // 车间名变化时，同步修改车间code
      if (!newValue) {
        return
      }
      this.data['workshop_code'] = this.workshop2code[newValue]
    }
  },
  methods: {
    timeChange (feildName, value) {
      this.data[feildName] = date.formatDate(value, this.dateFormat)
    }
  }
}
</script>

<style lang="stylus" scoped>
.col-label
  display inline-block
  width 130px
  text-align right
.col-input
  color #374853
  height 30px
  line-height 36px
  position relative
  border 1px solid #b1b1b1
  border-radius 5px
  background #fff
  padding-left 10px
  transition border .1s ease
  box-sizing border-box
.col-input:hover, .col-input:focus
  border-color #4cb8f7
  outline none
.col-width
  width 240px
</style>
<style lang="stylus">
.col-width .q-if-inverted .q-input-target
  color #000
</style>
