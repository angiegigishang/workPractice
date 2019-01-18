<template>
  <div class="full-width full-height">
    <div class="layout-wrap row items-center">
      <div v-for="item in list" class="row justify-center col-4">
        <div class="card text-center shadow-1" @click="$router.push(item.url)">
          <q-icon :name="item.icon" color="grey-9"/>
          <p class="caption text-grey-10 q-mt-md">{{ item.name }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'
export default {
  data () {
    return {
      list: [
        { name: this.$t('title.wage'), url: '/wage', icon: 'attach_money' },
        { name: this.$t('title.piece'), url: '/piece', icon: 'group_work' },
        { name: this.$t('title.time'), url: '/time', icon: 'access_alarm' }
      ]
    }
  },
  created () {
    this.updateNavTitle(this.$t('title.all'))
  },
  methods: mapMutations(['updateNavTitle'])
}
</script>

<style lang="stylus" scoped>
  .layout-wrap
    height calc(100vh - 100px)
    .card
      cursor pointer
      position relative
      width 200px
      padding 16px
      border-radius 6px
      .q-icon
        font-size 56px
      &:hover
        transform: scale(1.4)
</style>
