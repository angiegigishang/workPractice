// use this file when starting with http request
import router from '../router'
import axios from 'axios'
import store from 'src/store'
const http = axios.create({
  timeout: 5000,
  baseURL: process.env.http_base_url,
  headers: {'content-type': 'application/x-www-form-urlencoded'}
  // withCredentials: true
})

// http interceptor for response
http.interceptors.response.use(response => {
  if (response.status !== 200) {
    return Promise.reject(new Error('request failed'))
  }

  const result = response.data
  // cookie过期则跳转至登录页面
  if (result.code === 'login') {
    if (result.data) {
      if (result.data.login_url) {
        let href = router.resolve({
          path: '/login',
          query: { path: window.location.href, appId: result.data.app_id }
        })
        window.location.href = result.data.login_url + href.href
      } else {
        router.push('/404')
      }
    } else {
      router.push('/404')
    }

    return Promise.reject(result.info)
  }

  let res = {}
  let httpBody = {}
  const dataKeys = ['data', 'code', 'info', 'headers']
  const allKeys = Object.keys(result)

  dataKeys.forEach(function (key) {
    if (allKeys.indexOf(key) > -1) {
      res[key] = result[key]
    } else if (key in response) {
      res[key] = response[key]
    }
  })

  allKeys.forEach(key => {
    if (dataKeys.indexOf(key) === -1) {
      httpBody[key] = result[key]
    }
  })

  Object.keys(httpBody).length > 0 && store.commit('updateHttpBody', httpBody)

  return res
}, error => {
  return Promise.reject(error)
})

function _get (url, succ, fail, config = {}) {
  http.get(url, config)
    .then(function (response) {
      typeof succ === 'function' && succ(response)
    })
    .catch(function (error) {
      console.error(url + ' failed, error messsage: ' + error)
      typeof fail === 'function' && fail()
    })
}

function _delete (url, succ, fail, config = {}) {
  http.delete(url, config)
    .then(function (response) {
      typeof succ === 'function' && succ(response)
    })
    .catch(function (error) {
      console.error(url + ' failed, error messsage: ' + error)
      typeof fail === 'function' && fail()
    })
}

function _post (url, param, succ, fail, config = {}) {
  http.post(url, param, config)
    .then(function (response) {
      typeof succ === 'function' && succ(response)
    })
    .catch(function (error) {
      console.error(url + ' failed, error messsage: ' + error)
      typeof fail === 'function' && fail()
    })
}

function _put (url, param, succ, fail, config = {}) {
  http.put(url, param, config)
    .then(function (response) {
      typeof succ === 'function' && succ(response)
    })
    .catch(function (error) {
      console.error(url + ' failed, error messsage: ' + error)
      typeof fail === 'function' && fail()
    })
}

export default ({ Vue }) => {
  Vue.prototype.$get = _get
  Vue.prototype.$delete = _delete
  Vue.prototype.$post = _post
  Vue.prototype.$put = _put
}
