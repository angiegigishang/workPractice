<template>
  <div class="row justify-between relative-position">
    <div class="col-auto q-mx-lg q-mt-md" v-for="group in data">
      <div v-for="member in group.members"
                class="inline-block q-ma-md q-caption member text-center">
        {{member.name}}
      </div>
    </div>
    <m-mask v-show="show !== 'all' && show !== 'people'"></m-mask>
  </div>
</template>

<script>
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
    MMask
  }
}
</script>

<style lang="stylus" scoped>
@import '~variables'
$default-color = #e2dbdb
$member-color = #61a0a8
$member-size = 3rem
$member-size-height = 2.25rem
// 人员
.member
  width $member-size
  height $member-size-height
  line-height $member-size-height
  border-radius 0.83rem
  border-width 2px
  border-style solid
  border-color $member-color
  color $member-color
</style>
