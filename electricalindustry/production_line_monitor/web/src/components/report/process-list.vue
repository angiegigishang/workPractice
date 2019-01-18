<template>
  <div>
    <div class="row items-center">
      <template v-for="(item, index) in processData">
        <div class="col" v-if="index === 0">
          <div class="split-line bg-white"></div>
        </div>
        <div>
            <div class="column items-center text-center relative-position">
              <div class="process-item" :style="getCircleStyle(item.is_report_point)">
                <q-icon :style="iconStyle" size="2rem" :name="item.type === 0 ? 'settings_input_hdmi' : 'directions_walk'"></q-icon>
              </div>
              <div class="absolute process-title title-3">{{ item.name }}</div>
            </div>
          </div>
        <div class="col">
          <div class="split-line bg-white"></div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import { bgColorList } from 'assets/constant'
export default {
  props: {
    // 组
    processData: {
      type: Array,
      default: () => []
    },
    group: {
      type: String,
      default: ''
    }
  },
  computed: {
    borderColor () {
      return bgColorList[this.group]
    },
    iconStyle () {
      return {
        color: this.borderColor
      }
    }
  },
  methods: {
    getCircleStyle (isReport) {
      return {
        'border-color': this.borderColor,
        'background-color': isReport === 1 ? this.borderColor + '80' : 'transparent'
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
  .process-item
    width 4rem
    height 4rem
    line-height 3.5rem
    border-radius 4rem
    border-width 4px
    border-style solid
    background-color transparent
  .process-title
    top 4rem
  .split-line
    top 2rem
    height 4px
</style>
