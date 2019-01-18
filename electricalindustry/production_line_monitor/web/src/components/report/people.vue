<template>
  <v-touch class="group-item full-width row no-wrap cursor-pointer"
    @tap="toggleCheck(person.group_code)">
    <template v-for="item in person.member_list">
      <div class="col text-center q-ma-sm">
        <div class="person-item" :style="peopleStyle">
          <div style="font-size: 1rem;">{{ item.name }}</div>
        </div>
      </div>
    </template>
  </v-touch>
</template>

<script>
import { bgColorList } from 'assets/constant'
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
    isCheckGroup () {
      return this.group === this.person.group_code
    },
    borderColor () {
      return bgColorList[this.person.group_code]
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
      width 3.8rem
      height 3rem
      line-height 3rem
      border-radius 1rem
      border-width 4px
      border-style solid
</style>
