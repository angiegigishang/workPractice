import MgToolbar from './src/components/navigator/mg-toolbar'
import MgTabs from './src/components/navigator/mg-tabs'
import MgModal from './src/components/popups/mg-modal'
import MgDialog from './src/components/popups/mg-dialog'
import MgTable from './src/components/group/mg-table'
import MgDatetime from './src/components/tools/mgDatetime'

const components = [
  MgToolbar,
  MgTabs,
  MgModal,
  MgDialog,
  MgTable,
  MgDatetime
]

const install = function (Vue) {
  components.forEach(function (component) {
    Vue.component(component.name, component)
  })
}

export {
  MgToolbar,
  MgTabs,
  MgModal,
  MgDialog,
  MgTable,
  MgDatetime,
  install as default
}
