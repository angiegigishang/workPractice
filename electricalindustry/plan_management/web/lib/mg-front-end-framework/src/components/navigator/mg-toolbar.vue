<template>
  <q-toolbar class="bg-toolbar">
    <slot name="left">
      <q-btn flat class="absolute" @click="clickHandler">
        <img src="../../img/realtechLogo.png"/>
      </q-btn>
    </slot>
    <q-toolbar-title>
      <div class="text-center text-bold mg-title">
        {{ title }}
      </div>
    </q-toolbar-title>
    <div class="absolute right-14">
      <slot name="right" />
      <q-btn v-show="showAccount">
        <q-icon name="account_circle"/>
        <q-popover>
          <q-list link>
            <q-item>
              <q-item-main :label="userName"/>
            </q-item>
            <q-item @click.native="logout">
              <q-item-main label="退出"/>
            </q-item>
          </q-list>
        </q-popover>
      </q-btn>
    </div>
  </q-toolbar>
</template>

<script>
import { QToolbar, QBtn, QToolbarTitle, QIcon, QPopover, QList, QItem, QItemMain, Cookies } from 'quasar'
export default {
  name: 'MgToolbar',
  components: {
    QToolbar, QBtn, QToolbarTitle, QIcon, QPopover, QList, QItem, QItemMain
  },
  props: {
    title: {
      type: String,
      default: ''
    },
    showAccount: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    userName () {
      return Cookies.has(this.loginName) === true ? Cookies.get(this.loginName) : ''
    }
  },
  data () {
    return {
      loginName: 'login_name',
      loginUuid: 'login_uuid'
    }
  },
  methods: {
    clickHandler () {
      this.$emit('left-click')
    },
    logout () {
      if (Cookies.has(this.loginName)) {
        Cookies.remove(this.loginName)
      }
      if (Cookies.has(this.loginUuid)) {
        Cookies.remove(this.loginUuid)
      }
      // 应用场景：后端没有提供退出接口时，主动刷新当前页以触发后端的登录拦截功能
      this.$router.go(0)

      this.$emit('logout')
    }
  }
}
</script>

<style lang="stylus" scoped>
  .bg-toolbar
    background-color: #1D273A!important
    height 50px
    .mg-title
      font-size 30px
    .right-14
      right 14px
</style>
