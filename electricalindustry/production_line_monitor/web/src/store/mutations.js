export const updateHttpBody = (state, data) => {
  if (data) {
    state.httpBody = data
  }
}
// 更新监控数据
export const updatePiplineName = (state, data) => {
  data && (state.piplineName = data)
}
export const updateOnlineVersion = (state, data) => {
  data && (state.onlineVersion = data)
}
export const updateCheckinInfo = (state, data) => {
  data && (state.monitorCheckinInfo = data)
}
export const updateEquipmentStatus = (state, data) => {
  data && (state.monitorEquipmentStatus = data)
}
export const updatePlan = (state, data) => {
  data && (state.monitorPlan = data)
}
export const updateCurrentPlan = (state, data) => {
  data && (state.monitorCurrentPlan = data)
}
export const updateProcessList = (state, data) => {
  data && (state.monitorProcessList = data)
}
export const updateDataCollection = (state, data) => {
  data && (state.monitorDataCollection = data)
}
export const updateWarning = (state, data) => {
  data && (state.monitorWarning = data)
}
