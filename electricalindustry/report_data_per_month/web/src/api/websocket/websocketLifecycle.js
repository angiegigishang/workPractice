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

    let type = message.data_type
    if (type === 'draw') {
      store.commit('insertQueue', message.data[0])
    }
  },
  onclose (event) {
    // this method will be involved when readyState === 'CLOSED'
    console.log('websocket connect is closed...')
  }
}
