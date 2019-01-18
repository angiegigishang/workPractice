<template>
  <transition name="fade">
    <div class="mask"></div>
  </transition>
</template>

<script>
export default {}
</script>

<style lang="stylus" scoped>
.mask
  position absolute
  top 0
  right 0
  bottom 0
  left 0
  opacity .8
  background url("~assets/bg05.png")
.fade-enter-active, .fade-leave-active
  transition opacity 0.6s
.fade-enter, .fade-leave-active
  opacity 0
</style>
