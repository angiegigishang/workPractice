<template>
  <div>
    <vue-seamless-scroll :data="data" :class-option="options" class="seamless-wrap">
      <q-list class="seamless-item q-pa-none" no-border dense>
        <q-item v-for="(item, index) in data" :key="index" class="items-start">
          <q-item-side class="title-3">
            <q-item-tile>
              {{item.process_name}}:
            </q-item-tile>
          </q-item-side>
          <q-item-main class="title-3">
            <q-item-tile text-color="negative">
              {{item.message}}
            </q-item-tile>
          </q-item-main>
        </q-item>
      </q-list>
    </vue-seamless-scroll>
    <m-mask v-show="show !== 'all' && show !== 'warning'"></m-mask>
  </div>
</template>

<script>
import vueSeamlessScroll from 'vue-seamless-scroll'
import MMask from './m-mask'
export default {
  props: {
    data: {
      type: Array,
      default: () => []
    },
    options: {
      type: Object,
      default: () => {}
    },
    show: {
      type: String,
      default: 'all'
    }
  },
  components: {
    vueSeamlessScroll,
    MMask
  }
}
</script>

<style lang="stylus" scoped>
.seamless-wrap
  height 40px
  overflow hidden
  .seamless-item
    list-style none
</style>
