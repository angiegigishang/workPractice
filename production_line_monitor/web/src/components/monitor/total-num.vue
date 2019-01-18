<template>
  <div class="row justify-center">
    <div class="col-auto relative-position">
      <span class="q-title">今日累计合格 / 不合格：</span>
      <div class="q-display-4 text-bold inline-block">
        <!--<div class="flip"></div>-->
        <span>{{ data.positive }}</span>
      </div>
      <span class="q-title"> / </span>
      <sub class="q-display-3 color-negative">{{ data.negative }}</sub>
      <m-mask v-if="show !== 'all' && show !== 'quality'"></m-mask>
    </div>
  </div>
</template>

<script>
import MMask from './m-mask'
import { Flip } from 'number-flip'
// const $ = s => document.querySelector(s)
export default {
  props: {
    data: {
      type: Object,
      default: () => {}
    },
    show: {
      type: String,
      default: 'all'
    }
  },
  data () {
    return {
      sepa: null
    }
  },
  // mounted () {
  //   if (!this.sepa) {
  //     this.sepa = new Flip({
  //       node: $('.flip'),
  //       from: this.data.positive,
  //       to: this.data.positive
  //     })
  //   }
  // },
  // destroyed () {
  //   this.sepa = null
  // },
  // watch: {
  //   data (newVal) {
  //     this.sepa.flipTo({
  //       to: newVal.positive
  //     })
  //   }
  // },
  components: {
    MMask
  }
}
</script>

<style lang="stylus" scoped>
@import '~variables'
.color-negative
  color $negative
.flip
  height 105px !important
</style>
