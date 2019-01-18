export const updateHttpBody = (state, data) => {
  if (data) {
    state.httpBody = data
  }
}

// 更新导航表头
export const updateNavTitle = (state, data) => {
  state.navTitle = data
}
