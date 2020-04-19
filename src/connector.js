import Vue from 'vue'
import reqwest from './reqwest.js'

const serverUrl = 'http://localhost:9092'

const ACCESS_TOKEN_KEY = 'ACCESS_TOKEN'
const REFRESH_TOKEN_KEY = 'REFRESH_TOKEN'

const clientId = '0gvr1GFNpCy9fSpxsKHPdUPUu7ZSCQS76zc8kAgl'
const clientSecret = 'dazoA4IhCGrWrkh2rA02FE1qm3AVWdAz9qKqSZDLAD22xWiVYsEeMtq2BmqVY748U8Qw9jecBo9BHYYG3nZDgOUUwaEFjjDir1VX25ejnCvEcwdzV3Wt2Rxcnt45lxaN'

// Fix this issue:
//   Do not access Object.prototype method ‘hasOwnProperty’ from target object no-prototype-builtins
const hasOwnProperty = function (obj, name) {
    return obj && Object.prototype.hasOwnProperty.call(obj, name)
}

// For debug
const crossOrigin = true

let cachedData = {}

const get_key = function (key) {
    if (hasOwnProperty(cachedData, key) && cachedData[key])
        return cachedData[key]
    cachedData[key] = window.localStorage.getItem(key)
    return cachedData[key]
}

const set_key = function (key, value) {
    cachedData[key] = value

    if (value === null) {
        window.localStorage.removeItem(key)
        return
    }

    try {
        window.localStorage.setItem(key, value)
    }
    catch (e) {
        Vue.prototype.$message( {
            type: 'warning',
            message: '当前浏览器无法保存登陆信息，关闭页面之后登陆信息会丢失',
            showClose: true,
            duration: 0
        } )
    }
}

const is_authenticated = function () {
    return get_key(ACCESS_TOKEN_KEY)
}

const error_callback = function (req, msg, err) {
    let response = req.response
    if (typeof req.response === 'string' &&
        req.response[0] === '{' && req.response.slice(-1) === '}')
        response = JSON.parse(req.response)
    this( false, {
        status: req.status,
        statusText: req.statusText,
        message: msg ? msg :
            req.status === 0 ? '无法发送请求到服务器' :
            hasOwnProperty(response, 'error') ?  response.error :
            hasOwnProperty(response, 'detail') ? response.detail :
            hasOwnProperty(err, 'message') ? err.message :
            '发送请求到服务器发生了未知错误'
    } )
}

const request_token = function (url, data, callback) {
    reqwest( {
        url: url,
        method: 'post',
        type: 'json',
        contentType: 'application/x-www-form-urlencoded',
        headers: {
            Authorization: 'Basic ' + btoa(clientId + ':' + clientSecret)
        },
        data: data,
        crossOrigin: crossOrigin,
        success: function (result) {
            set_key(ACCESS_TOKEN_KEY, data['access_token'])
            set_key(REFRESH_TOKEN_KEY, data['refresh_token'])
            callback(true, result)
        },
        error: error_callback.bind(callback)
    } )
}

const get_token = function (username, password, callback) {
    const url = serverUrl + '/o/token/'
    const data = {
        grant_type: 'password',
        username: username,
        password: password
    }
    request_token(url, data, callback)
}

 const refresh_token = function (callback) {
    const url = serverUrl + '/o/token/'
    const data = {
        grant_type: 'refresh_token',
        refresh_token: get_key(REFRESH_TOKEN_KEY),
        client_id: clientId,
        client_secret: clientSecret
    }
    request_token(url, data, callback)
}

const revoke_token = function (callback) {
    const url = serverUrl + '/o/revoke_token/'
    const data = {
        token: get_key(ACCESS_TOKEN_KEY),
        client_id: clientId,
        client_secret: clientSecret
    }
    reqwest( {
        url: url,
        method: 'post',
        type: 'json',
        contentType: 'application/x-www-form-urlencoded',
        data: data,
        crossOrigin: crossOrigin,
        success: function (result) {
            set_key(ACCESS_TOKEN_KEY, null)
            set_key(REFRESH_TOKEN_KEY, null)
            callback(true, result)
        },
        error: error_callback.bind(callback)
    } )
}

const request_api = function (api, method, paras, callback, complete) {
    const url = serverUrl + api.slice(-1) === '/' ? api : (api + '/')
    reqwest( {
        url: url,
        method: method,
        type: hasOwnProperty(paras, 'responseType') ? paras.responseType : 'json',
        contentType: paras.contentType,
        headers: {
            Authorization: 'Bearer ' + get_key(ACCESS_TOKEN_KEY)
        },
        data: paras.data,
        crossOrigin: crossOrigin,
        success: function (result) {
            callback(true, result)
        },
        error: error_callback.bind(callback),
        complete: complete
    } )
}

// const upload_file = function (api, data, callback) {
//     let file = new File( [filedata], filename, { type: 'text/plain' } )
//     paras.data = { source: file }
//     paras.contentType = 'multipart/form-data'
//     reqwest( paras );
// }

// const download_file = function (api, callback) {
//     paras.data = coursework
//     paras.responseType = 'blob'
// }

export default new Vue({
    data() {
        return {
            connected: false,
        }
    },
    methods: {
        showError(err) {
            Vue.prototype.$message( {
                type: 'error',
                message: err,
                showClose: true,
                duration: 15000
            } )
        },
        sendRequest(api, paras, event, options) {
            let opt = !options ? {} : options
            const loading = opt.loading
            const silent =  opt.silent
            const method = opt.method ? opt.method :
                  event.startswith('api-new') ? 'post' :
                  api.startswith('api-update') ? 'patch' :
                  api.startswith('api-remove') ? 'delete' : 'get'

            const retry_callback = function (success, result) {
                if (success)
                    this.sendRequest(api, paras, event, options)
                else {
                    if (!silent && result.message)
                        this.showError(result.message)
                    this.$emit(event, success, result)
                }
            }.bind(this)

            const callback = function (success, result) {
                if (success)
                    this.$emit(event, true, result)
                else if (result.status === 401 && is_authenticated()) {
                    refresh_token(retry_callback)
                }
                else {
                    if (!silent && result.message)
                        this.showError(result.message)
                    this.$emit(event, false, result)
                }
            }.bind(this)

            if (!loading) {
                request_api(api, method, paras, callback)
            }
            else {
                const vnode = this.$loading( {
                    lock: true,
                    text: loading,
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)'
                } )
                request_api(api, method, paras, callback, vnode.close)
            }
        },
        login: function (username, password, silent) {
            const callback = function (success, result) {
                if (!success && !silent && result.message)
                    this.showError(result.message)
                this.$emit('api-login', success, result)
            }.bind(this)
            get_token(username, password, callback)
        },
        logout: function (silent) {
            const callback = function (success, result) {
                if (!success && !silent && result.message)
                    this.showError(result.message)
                this.$emit('api-logout', success, result)
            }.bind(this)
            revoke_token(callback)
        },
        newCourse: function (course) {
            const api = '/api/courses/'
            this.sendRequest(api, { data: course }, 'api-new-course')
        },
        listCourses: function () {
            const api = '/api/courses/'
            this.sendRequest(api, {}, 'api-list-courses')
        },
        getCourse: function (course) {
            const api = '/api/courses/' + course.id
            this.sendRequest(api, {}, 'api-get-course')
        },
        updateCourse: function (course) {
            const api = '/api/courses/' + course.id
            this.sendRequest(api, { data: course }, 'api-update-course')
        },
        removeCourse: function (course) {
            const api = '/api/courses/' + course.id
            this.sendRequest(api, { data: course }, 'api-remove-course')
        },
        listCourseItems: function (course) {
            const api = '/api/courses/' + course.id + '/items/'
            this.sendRequest(api, {}, 'api-list-course-items')
        },
        newCoursework: function (coursework) {
            const api = '/api/courseworks/'
            this.sendRequest(api, { data: coursework }, 'api-new-coursework')
        },
        getCoursework: function (coursework) {
            const api = '/api/courseworks/' + coursework.id
            this.sendRequest(api, {}, 'api-get-coursework')
        },
        listCourseworks: function () {
            const api = '/api/courseworks/'
            this.sendRequest(api, {}, 'api-list-courseworks')
        },
        updateCoursework: function (coursework) {
            const api = '/api/courseworks/' + coursework.id
            this.sendRequest(api, { data: coursework }, 'api-update-coursework')
        },
        removeCoursework: function (coursework) {
            const api = '/api/courseworks/' + coursework.id
            this.sendRequest(api, { data: coursework }, 'api-remove-coursework')
        },
        getCourseworkContent: function (coursework) {
            const api = '/api/courseworks/' + coursework.id + '/content/'
            this.sendRequest(api, {}, 'api-get-coursework')
        },
        buildCoursework: function (coursework) {
            const api = '/api/courseworks/' + coursework.id + '/build/'
            this.sendRequest(api, { data: coursework }, 'api-build-coursework')
        },
        taskCoursework: function (coursework) {
            const api = '/api/courseworks/' + coursework.id + '/task/'
            this.sendRequest(api, { data: coursework }, 'api-task-coursework')
        },
    }
})