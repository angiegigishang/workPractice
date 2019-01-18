export const updateHttpBody = (state, data) => {
  if (data) {
    state.httpBody = data
  }
}

// 更新物料集合
export const updateMaterials = (state, data) => {
  if (!Array.isArray(data)) {
    return
  }
  let result = {}
  data.forEach(item => {
    result[item.name] = {
      code: item.code,
      unit: item.dimension
    }
  })
  state.materials = result
}

// 更新计划定制字段
export const updateExtralFields = (state, data) => {
  if (Array.isArray(data)) {
    state.extralFields = data.map(item => ({
      label: item.field_name,
      sortable: true,
      field: item.field_code,
      name: item.field_code,
      align: 'center'
    }))
  }
}

// 更新车间产线关系
export const updateWorkshops = (state, data) => {
  if (!Array.isArray(data)) {
    return
  }
  let result = {}
  data.forEach(item => {
    result[item.workshop_code] = {
      name: item.workshop_name,
      pipelines: item.pl_list || []
    }
  })
  state.workshops = result
}
