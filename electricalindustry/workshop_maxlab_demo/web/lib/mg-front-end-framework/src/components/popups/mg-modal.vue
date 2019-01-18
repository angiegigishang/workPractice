<template>
  <q-modal v-model="isOpen" :content-css="{minWidth: width, minHeight: height}">
    <q-modal-layout
      header-class="bg-secondary no-shadow"
      footer-class="bg-white no-shadow"
    >
      <q-toolbar :class="align[titleAlign]" slot="header" color="secondary">
        <q-toolbar-title>
          {{title}}
        </q-toolbar-title>
      </q-toolbar>
      <slot name="body">
        add something here....
      </slot>
      <div slot="footer" class="modal-footer q-mb-md q-mt-md">
        <slot name="footer">
          <div class="inner text-center">
            <q-btn color="secondary" v-close-overlay
                   size="md"
                   :label="confirmTitle"
                   class="q-mr-xl"
                   @click="confirm"/>
            <q-btn color="brown-5" v-close-overlay
                   size="md"
                   :label="cancelTitle"
                   @click="cancel"
            />
          </div>
        </slot>
      </div>
    </q-modal-layout>
  </q-modal>
</template>

<script>
import { QModal, QModalLayout, QToolbar, QToolbarTitle, QBtn, CloseOverlay } from 'quasar'
export default {
  name: 'MgModal',
  components: {
    QModal, QModalLayout, QToolbar, QToolbarTitle, QBtn
  },
  directives: {
    CloseOverlay
  },
  data () {
    return {
      confirmTitle: this.getBtnLabel('button.confirm', '确认'),
      cancelTitle: this.getBtnLabel('button.cancel', '取消'),
      align: {
        left: 'text-left',
        center: 'text-center',
        right: 'text-right'
      }
    }
  },
  props: {
    open: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'modal title'
    },
    titleAlign: {
      type: String,
      default: 'center'
    },
    height: {
      type: String,
      default: '400px'
    },
    width: {
      type: String,
      default: '400px'
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
  methods: {
    changeOpen (flag) {
      this.$emit('update:open', flag)
    },
    confirm () {
      this.$emit('confirm')
    },
    cancel () {
      this.$emit('cancel')
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
