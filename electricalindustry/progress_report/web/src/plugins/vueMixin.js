import { Notify } from 'quasar'

export default ({ Vue }) => {
  Vue.mixin({
  //  add whatever you need in VUE: methods | components | directives | created | mounted .....
  //  !NOTE: not add lifecycle methods (created) if unneccessary as they would register into every component you defined
    methods: {
      isValid (obj, propName) {
        if (obj === null || obj === undefined) {
          return false
        }

        // Object or Array
        if (obj instanceof Object) {
          return propName ? (propName in obj) : true
        } else if (obj instanceof Array) {
          return !!obj.length
        } else { // beyond that, return true( for example: obj === 0 )
          return true
        }
      },
      showNotify (config) {
        !('timeout' in config) && (config['timeout'] = 1000)
        !('position' in config) && (config['position'] = 'bottom')
        !('color' in config) && (config['color'] = 'grey')
        Notify.create(config)
      },
      responseValidate (response) { // validate rest api
        if (response.code === 'fail') {
          if ('showNotify' in this) {
            this.showNotify({
              message: 'request failed: ' + response.info,
              position: 'center',
              color: 'red'
            })
          }
          return false
        }

        return true
      },
      download (response) {
        if (!response) {
          return
        }

        let fileName = 'test.txt'
        if ('headers' in response &&
          'content-disposition' in response['headers'] &&
          response['headers']['content-disposition'].indexOf('filename') > -1) {
          const header = response['headers']['content-disposition'].split(';')
          for (let i = 0; i < header.length; i++) {
            if (header[i].trim().startsWith('filename')) {
              const arr = header[i].split('=')
              fileName = arr[arr.length - 1].trim()
              break
            }
          }
        }
        let url = window.URL.createObjectURL(new Blob([response.data]))
        let link = document.createElement('a')
        link.style.display = 'none'
        link.href = url
        link.setAttribute('download', decodeURI(fileName))
        link.click()
      }
    }
  })
}

/*
* call all above redirectly without importing anything just like they are defined in you own component
*
* examples:
*   this.testFunc()
*
* */
