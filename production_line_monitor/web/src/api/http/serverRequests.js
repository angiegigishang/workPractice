import Vue from 'vue'

const $get = Vue.prototype.$get
// const $delete = Vue.prototype.$delete
// const $post = Vue.prototype.$post
// const $put = Vue.prototype.$put

export default {
  // declare some methods to communicate with server by using $get | $delete | $post | $put.
  // if you want to access different domain, specify it as the last parameter
  allapps (cbk) {
    $get('api/config/allapps', cbk, null, { baseURL: 'http://192.168.20.186:80' })
  }
  // cbk is a customed callback function when the server has response
}
