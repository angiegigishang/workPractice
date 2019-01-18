import WebsocketLifecycle from '../api/websocket/websocketLifecycle'

let ws
const websocketUrl = process.env.websocket_base_url
const timeout = 5000

function createWs () {
  // websocket instantiated
  ws = new WebSocket(websocketUrl)
  initEventHandler()
}

function initEventHandler () {
  // ws.onopen = WebsocketLifecycle.onopen

  ws.onmessage = WebsocketLifecycle.onmessage

  ws.onclose = function () {
    WebsocketLifecycle.onclose()
    setTimeout(function () {
      createWs()
    }, timeout)
  }
}

function sendWsDataToApp (data) {
  data && ws.send(data)
}

export default ({ Vue }) => {
  // 定义websocket向后端发送数据的方法, 在组件中使用: this.$ws_send('123'); 在js文件中使用: Vue.prototype.$ws_send('123')
  Vue.prototype.$ws_send = sendWsDataToApp

  createWs()
}
