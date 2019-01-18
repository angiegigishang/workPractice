<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  data () {
    return {

    }
  }
}
</script>

<style lang="stylus" scoped>
  @import '~variables'

  .content
    margin-top 100px
    font-size 24px
    color $tertiary
</style>
