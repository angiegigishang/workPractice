/**
 * websocket listeners
*/

// !NOTE: Uncomment the following line if you start to use vuex in websocket listeners
import store from 'src/store'

export default {
  /*
  onopen (event) {
    // this method will be involved when readyState === 'OPEN'
  },
  onerror (error) {
    // this method will be involved when error occurred
  },
  */
  onmessage (event) {
    // this method will be involved when message received
    let message = JSON.parse(event.data)
    if (!message) {
      return
    }

    let type = message.type
    if (type === 'all') {
      store.dispatch('updateAllData', message.data)
    } else if (type === 'data_collection') {
      store.commit('updateDataCollection', message.data.data_collection)
      store.commit('updateCurrentPlan', message.data.current_plan)
    } else if (type === 'plan') {
      store.commit('updatePlan', message.data.plan)
    } else if (type === 'equipment_status') {
      store.commit('updateEquipmentStatus', message.data)
    } else if (type === 'check_in') {
      store.commit('updateCheckinInfo', message.data.checkinInfo)
    }
  },
  onclose (event) {
    // this method will be involved when readyState === 'CLOSED'
    console.log('websocket connect is closed...')
  }
}
