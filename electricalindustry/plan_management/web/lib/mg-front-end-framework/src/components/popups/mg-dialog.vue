<template>
  <q-dialog
    v-model="isOpen"
    no-esc-dismiss
    @ok="onOk"
    @cancel="onCancel"
    @show="onShow"
    @hide="onHide"
    color="secondary">
    <span slot="title">{{ title }}</span>
    <slot name="body" slot="body" />
    <template slot="buttons" slot-scope="props">
      <slot name="footer"
            :ok="props.ok"
            :cancel="props.cancel"
            :show="props.show"
            :hide="props.hide">
        <q-btn color="primary" :label="confirmTitle" @click="props.ok" />
        <q-btn color="primary" :label="cancelTitle" @click="props.cancel" />
      </slot>
    </template>
  </q-dialog>
</template>

<script>
import { QDialog, QBtn } from 'quasar'
export default {
  name: 'MgDialog',
  components: {
    QDialog, QBtn
  },
  props: {
    open: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ''
    }
  },
  computed: {
    isOpen: {
      set (newValue) {
        this.changeOpen(newValue)
      },
      get () {
        return this.open
      }
    }
  },
  data () {
    return {
      confirmTitle: this.getBtnLabel('button.confirm', '确认'),
      cancelTitle: this.getBtnLabel('button.cancel', '取消')
    }
  },
  methods: {
    onOk () {
      this.$emit('ok')
    },
    onCancel () {
      this.$emit('cancel')
    },
    onShow () {
      this.$emit('show')
    },
    onHide () {
      this.$emit('hide')
    },
    changeOpen (flag) {
      this.$emit('update:open', flag)
    },
    getBtnLabel (path, replace) {
      const arr = path.split('.')
      const len = arr.length
      if (len === 0) {
        return replace
      } else if (len === 1) {
        return this.$t(path)
      }
      const parentPath = this.$t(arr.slice(0, len - 1).join('.'))
      const key = arr[len - 1]
      if (typeof parentPath === 'object' && key in parentPath) {
        return parentPath[key]
      }

      return replace
    }
  }
}
</script>
