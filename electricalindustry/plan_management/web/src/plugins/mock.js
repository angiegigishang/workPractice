import Mock from 'mockjs'

/*
 * 模板key为：去掉前缀（即协议、ip、端口）的接口名，且必须以'/'开头
 * for example：
 *  {
 *    '/api/config/allapps': []
 *  }
 */
const template = require('src/mock-data/data.json')

// get template data
function getMockData (options) {
  const url = new URL(options.url)
  return Mock.mock(template[url.pathname])
}

export default () => {
  /*
   * url匹配示例：
   *   http://localhost
   *   http://localhost:8080
   *   http://192.168.20.126
   *   http://192.168.20.126/test/test
   *   http://192.168.20.126:8080/test
   */
  const reg = /((http|https):\/\/)((([0-9]{1,3}\.){3}[0-9]{1,3})|localhost)(:[0-9]{1,4})?(\/[a-zA-Z0-9_]*)?/
  Mock.mock(reg, 'get', getMockData)
    .mock(reg, 'post', getMockData)
    .mock(reg, 'put', getMockData)
    .mock(reg, 'delete', getMockData)
}
