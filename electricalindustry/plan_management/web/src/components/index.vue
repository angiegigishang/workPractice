<template>
  <q-layout view="HHH lpr fff">
    <q-layout-header>
      <mg-toolbar :title="$t('title.mainTitle')" @left-click="$router.push({ path: '/' })"></mg-toolbar>
    </q-layout-header>

    <q-page-container>
      <router-view></router-view>
    </q-page-container>
  </q-layout>
</template>

<script>
import http from 'http/plan'
import { mapMutations } from 'vuex'
export default {
  created () {
    // 获取计划相关的配置数据
    http.planConfigs(function (res) {
      if (res.code === 'success') {
        const data = res.data
        this.updateMaterials(data.material_config || [])
        this.updateExtralFields(data.custom_fields || [])
        this.updateWorkshops(data.workshop_config || [])
      }
    }.bind(this))
  },
  methods: mapMutations(['updateMaterials', 'updateExtralFields', 'updateWorkshops'])
}
</script>
