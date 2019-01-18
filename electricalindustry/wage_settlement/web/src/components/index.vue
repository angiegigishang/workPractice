<template>
  <q-layout view="HHH lpr fff">
    <q-layout-header>
      <mg-toolbar
        :title="navTitle"
        @left-click="$router.push('/')">
      </mg-toolbar>
    </q-layout-header>

    <q-page-container>
      <router-view></router-view>
    </q-page-container>
  </q-layout>
</template>

<script>
import { mapState } from 'vuex'
export default {
  computed: mapState(['navTitle'])
}
</script>
