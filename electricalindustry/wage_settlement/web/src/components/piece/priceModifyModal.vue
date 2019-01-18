<template>
  <q-modal
    class="attr-modal"
    no-esc-dismiss
    no-backdrop-dismiss
    v-model="show">
    <div>
      <div class="bg-secondary text-white text-center modal-header q-title">
        <p>{{ this.form.process }}</p>
      </div>
      <div class="q-pa-md">
        <template v-for="val in mapper">
          <q-field
            :label="val.name"
            :label-width="4"
            class="q-mt-md">
            <q-input v-model.trim="form[val.code]" />
          </q-field>
        </template>
      </div>
      <div class="text-center q-mt-sm q-mb-sm">
        <q-btn label="取消" color="secondary" @click="cancel" />
        <q-btn label="保存" color="secondary" @click="confirm" />
      </div>
    </div>
  </q-modal>
</template>

<script>
export default {
  props: {
    dialogShow: {
      type: Boolean,
      default: false
    },
    dialogData: {
      type: Object,
      default: () => {}
    },
    // 分组
    mapper: {
      type: Array,
      default: []
    }
  },
  data () {
    return {
      show: false,
      num: 1,
      form: {}
    }
  },
  watch: {
    dialogShow (show) {
      this.show = show
      if (show) {
        this.getForm()
      }
    }
  },
  created () {
    this.show = this.dialogShow
    this.getForm()
  },
  methods: {
    getForm () {
      this.form = { ...this.dialogData }
      delete this.form.__index
    },
    confirm () {
      this.$emit('update-table', this.form)
    },
    cancel () {
      this.$emit('update:dialogShow', false)
    }
  }
}
</script>
