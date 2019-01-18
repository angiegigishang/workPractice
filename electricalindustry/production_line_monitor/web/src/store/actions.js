export const updateAllData = ({commit, state}, data) => {
  commit('updatePiplineName', data.piplineName)
  commit('updateOnlineVersion', data.online_version)
  commit('updateCheckinInfo', data.check_in.checkinInfo)
  commit('updateEquipmentStatus', data.equipment_status)
  commit('updatePlan', data.plan)
  commit('updateCurrentPlan', data.current_plan)
  commit('updateProcessList', data.process_list)
  commit('updateDataCollection', data.data_collection)
  commit('updateWarning', data.warning)
}
