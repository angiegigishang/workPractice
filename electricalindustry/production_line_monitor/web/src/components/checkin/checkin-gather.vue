<template>
  <div class="full-width" style="margin-top: 180px">
    <!-- 工序列表 -->
    <div class="row no-wrap justify-between relative-position">
      <!-- 分割线 -->
      <div class="absolute full-width split">
        <div class="relative-position split-look"></div>
      </div>

       <!--工序 -->
      <template :id="item[0]" v-for="item in processList">
        <div class="relative-position" style="z-index: 2">
          <!-- 工序icon -->
          <div class="procedure icon-width icon-height cursor-pointer"
               :style="{'border-color': groupByLoc[process2GroupMap[item[0]]].color}">
            <div class="procedure-circle">
              <q-icon :name="item[2] ? manualIcon : deviceIcon"
                      :style="{color: item[3] <= groupByLoc[process2GroupMap[item[0]]].workNum ? groupByLoc[process2GroupMap[item[0]]].color : offColor}"
                      size="24px"></q-icon>
            </div>
          </div>
          <!-- 工序名 -->
          <div class="q-py-sm icon-width"><!-- 文字旋转45度：rotate-45 -->
            <div class="title-3" style="text-align: center">{{ item[1] }}</div>
          </div>
        </div>
      </template>
    </div>

     <!--人员展示 -->
    <div class="row justify-between full-width q-mt-xl">
      <div v-for="group in groupByLoc"
           class="q-pa-md q-ma-md member-box row">
        <template v-for="mem in group.members">
          <v-touch class="q-ma-md member text-center text-bold"
                   :style="{'border-color': mem.on_work ? group.color : offColor, color: mem.on_work ? group.color : offColor}"
                   @tap="signHandler(mem)">
            <span :style="{'background-image': `url(${mem.avatar ? mem.avatar : defaultAvatar})`, opacity: mem.on_work ? 1 :0.3}">
            </span>
            <span>{{mem.name}}</span>
          </v-touch>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { colorList } from 'assets/constant'
export default {
  props: {
    processList: {
      type: Array,
      default: () => []
    },
    checkinGroup: {
      type: Array,
      default: () => []
    }
  },
  data () {
    return {
      on_work: false,
      offColor: '#403E42', // 未点亮颜色
      process2GroupMap: {}, // 工序id: 组index
      manualIcon: 'directions_walk', // 人工
      deviceIcon: 'settings_input_hdmi', // 设备
      defaultAvatar: "statics/defaultAvatar.png"
    }
  },
  computed: {
    groupByLoc () {
      const result = []
      const list = this.checkinGroup
      if (!Array.isArray(list) || !list.length) {
        return result
      }

      // 分组信息整理
      list.forEach(function (item, index) {
        const group = {
          groupCode: item.groupCode,
          members: this.copyMembers(item.members),
          on_work: this.getMemberState(item.members),
          color: this.randColor(index),
          workNum: this.getWorkNum(item.members) // 当前在线人数
        }
        result.push(group)
        this.setProcess2Group(item.processCodes, index)
      }.bind(this))

      return result
    }
  },
  methods: {
    copyMembers (members) {
      const result = []
      if (!Array.isArray(members) || !members.length) {
        return result
      }

      members.forEach(mem => {
        result.push(Object.assign({}, mem))
      })
      return result
    },
    getWorkNum (members) {
      if (!Array.isArray(members) || !members.length) {
        return 0
      }

      return members.filter(mem => mem.on_work).length
    },
    setProcess2Group (processCodes, index) {
      if (!Array.isArray(processCodes) || !processCodes.length) {
        return
      }

      processCodes.forEach(function (code) {
        this.process2GroupMap[code] = index
      }.bind(this))
    },
    getMemberState (members) {
      if (!Array.isArray(members) || !members.length) {
        return false
      }

      return !!members.filter(item => item.on_work).length
    },
    signHandler (member) { // 记录签到数据
      member.on_work = !member.on_work
      this.$emit('submit', [{
        code: member.code,
        on_work: member.on_work
      }])
    },
    randColor (index) {
      return colorList[index]
    }
  }
}
</script>

<style lang="stylus" scoped>
  @import "~variables"

  $size = 56px
  $member-size = 4rem
  $member-size-height = 4.3rem
  $avatar-size = 2rem

  .icon-width
    width $size
  .icon-height
    height $size
    line-height $size - 8
  .split
    height $size
    .split-look
      top 50%
      height 4px
      width 100%
      background-color $default-color
  .procedure
    color #fff
    text-align center
    font-weight bold
    border-radius $size
    border-width 4px
    border-style solid
    text-align center
    margin-bottom 10px
    .procedure-circle
      background-color #071C30
      width 100%
      border-radius 100%
      height 100%

  .member-box
    border 0px solid grey
    .member
      width $member-size
      height $member-size-height
      border-radius 1.1rem
      border-width 4px
      border-style solid
      display flex
      flex-direction column
      justify-content space-around
      align-items center
      font-size 16px
      span
        &:first-child
          width $avatar-size
          height $avatar-size
          border-radius 50%
          background-repeat no-repeat
          background-size 100% 100%
        &:last-child
          position relative
          top -2px

</style>
