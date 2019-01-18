<template>
  <q-tabs inverted :align="tabAlign"
          :text-color="color"
          v-model="activeTab"
          :no-pane-border="!paneBorder">
    <template v-for="tab in tabList">
      <q-tab :default="tab.default"
             :icon="tab.icon"
             @click="eventHandler($event)"
             slot="title"
             :name="tab.name"
             :label="tab.label"/>
      <q-tab-pane :name="tab.name">
        <slot :name="tab.name" :param="tab">{{tab.label}}</slot>
      </q-tab-pane>
    </template>
  </q-tabs>
</template>

<script>
import {QTabs, QTab, QTabPane} from 'quasar'

export default {
  name: 'MgTabs',
  components: {
    QTabs, QTab, QTabPane
  },
  props: {
    active: {
      type: String,
      default: ''
    },
    tabAlign: { // left center right justify
      type: String,
      default: 'left'
    },
    color: {
      type: String,
      default: 'primary'
    },
    paneBorder: {
      type: Boolean,
      default: true
    },
    tabList: {
      type: Array,
      default: function () {
        return []
      },
      validator: function (data) {
        let flag = data instanceof Array
        if (flag && data.length > 0) {
          let hasDefault = false
          for (let i = 0; i < data.length; i++) {
            const obj = data[i]
            if (!('name' in obj && 'label' in obj)) {
              flag = false
              break
            }
            hasDefault = hasDefault || obj['default']
          }
          if (flag && !hasDefault) {
            data[0]['default'] = true
          }
        }
        return flag
      }
    }
  },
  data () {
    return {
      activeTab: ''
    }
  },
  created () {
    this.activeTab = this.active || this.tabList[0]['name']
  },
  watch: {
    active (newValue) {
      this.activeTab = newValue
    }
  },
  methods: {
    eventHandler (tabName) {
      this.$emit('select', tabName)
    }
  }
}
</script>
