<template>
  <div class="group-item row no-wrap cursor-pointer" @click="toggleCheck(person.group_code)">
    <template v-for="item in person.member_list">
      <div class="text-center q-ma-sm">
        <div class="person-item" :style="peopleStyle">
          <div style="font-size: 1rem;">{{ item.name }}</div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  props: {
    person: {
      type: Object,
      default: () => {}
    },
    group: {
      type: String,
      default: ''
    }
  },
  computed: {
    ...mapState(['colorList']),
    isCheckGroup () {
      return this.group === this.person.group_code
    },
    borderColor () {
      return this.colorList[this.person.group_code]
    },
    peopleStyle () {
      return {
        'border-color': this.borderColor,
        'background-color': this.isCheckGroup ? this.borderColor + '80' : 'transparent',
        'color': this.borderColor,
        'display': 'inline-block'
      }
    }
  },
  methods: {
    toggleCheck (code) {
      this.$emit('update:group', code)
    }
  }
}
</script>

<style lang="stylus" scoped>
  .group-item
    .person-item
      width 4.5rem
      height 4.5rem
      line-height 4.5rem
      border-radius 100%
      border-width 4px
      border-style solid
</style>
