<template>
  <div class="bubble-container absolute">
    <div v-for="item in num" class="wrapper">
      <div class="circle text-bold title-3" :class="`circle-${item}`">异常</div>
    </div>
    <m-mask v-if="show !== 'all' && show !== 'warning'"></m-mask>
  </div>
</template>

<script>
import MMask from './m-mask'
export default {
  props: {
    show: {
      type: String,
      default: 'all'
    }
  },
  data () {
    return {
      num: 1
    }
  },
  components: {
    MMask
  }
}
</script>

<style lang="stylus" scoped>
@import '~variables'
random(a,b)
  return math(math(0, 'random')*(b - a + 1) + a, 'floor')
$size = 56px
$size-circle = 56px
$height = 380px
$delay = 1.7s
$rise = 5s
@keyframes rise {
  0% {
    margin-top: 100%;
  }
  70% {
    opacity: 0.8;
    transform: scale(0.8);
  }
  95% {
    opacity: 0;
    transform: scale(0.6);
  }
  100% {
    margin-top: - $height;
    opacity: 0;
    transform: scale(0.55);
  }
}
.bubble-container
  height $height
  width $size
  overflow hidden
  bottom $size
  left 0
.wrapper
  position relative
.circle
  opacity 1
  position absolute
  border-radius 50%
  /*box-shadow -8px -8px 80px -8px $negative inset*/
  text-align center
  width $size-circle
  height $size-circle
  line-height $size-circle
  color $negative
  /*background -webkit-radial-gradient(30% 30%,#fff 5%,red 95%)*/
  /*background-color $negative*/
  background-image url("~assets/paopao1.png")
  background-size cover
  background-position center center
for $num in (1..10)
  .circle-{$num}
    animation rise $rise linear infinite
    animation-delay ($num - 1) * $delay
    top $height
</style>
