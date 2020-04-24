import { COMPILED, FAILURE, TIMEOUT, BUILDING } from './definition.js'

import Vue from 'vue'
import reqwest from './plugins/reqwest.js'


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
            set_key(ACCESS_TOKEN_KEY, result['access_token'])
            set_key(REFRESH_TOKEN_KEY, result['refresh_token'])
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
    const url = serverUrl + api + (api.slice(-1) === '/' ? '' : '/')
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
            callback(true, (result && Boolean(result.responseText)) ? result.responseText : result)
        },
        error: error_callback.bind(callback),
        complete: complete
    } )
}

const make_multipart_data = function (args, files) {
    const boundary = '---------------------------' + Date.now().toString(16)
    const prefix = '--' + boundary + '\r\n' + 'Content-Disposition: multipart/form-data; '
    const result = ['']

    if (args)
        args.forEach( function (k) {
            result.push('name="' + k[0] + '"\r\n\r\n' + k[1] + '\r\n')
        } )
    if (files)
        files.forEach( function (k) {
            result.push('name="' + k[0] + '"; filename="' + k[1] + '"\r\n\r\n' + k[2] + '\r\n')
        } )

    return {
        data: result.join(prefix) + '--' + boundary + '--\r\n',
        contentType: 'multipart/form-data; boundary=' + boundary
    }
}

export default new Vue({
    computed: {
        isAuthenticated: function () {
            return is_authenticated()
        }
    },
    methods: {
        showError(err) {
            Vue.prototype.$message( {
                type: 'warning',
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
                  event.indexOf('api-new') === 0 ? 'post' :
                  event.indexOf('api-update') === 0 ? 'patch' :
                  event.indexOf('api-edit') === 0 ? 'put' :
                  event.indexOf('api-remove') === 0 ? 'delete' : 'get'

            const retry_callback = function (success, result) {
                if (success)
                    this.sendRequest(api, paras, event, options)
                else {
                    if (!silent)
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
                    if (!silent)
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
                if (!success && !silent)
                    this.showError(result.message)
                this.$emit('api-login', success, result)
            }.bind(this)
            get_token(username, password, callback)
        },
        logout: function (silent) {
            const callback = function (success, result) {
                if (!success && !silent)
                    this.showError(result.message)
                this.$emit('api-logout', success, result)
            }.bind(this)
            revoke_token(callback)
        },
        getLogon: function () {
            const api = '/api/users/info/'
            this.sendRequest(api, {}, 'api-get-logon', {silent: true})
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
        newCoursework: function (filename, content, course) {
            const api = '/api/courseworks/'
            let files = []
            files.push(['source', filename, content])
            let args = []
            if (course)
                args.push(['course', course.id])
            this.sendRequest(api, make_multipart_data(args, files), 'api-new-coursework')
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
            this.sendRequest(api, { responseType: 'blob' }, 'api-get-coursework-content')
        },
        updateCourseworkContent: function (coursework, content) {
            const api = '/api/courseworks/' + coursework.id
            let files = []
            files.push(['source', coursework.name, content])
            let args = []
            args.push([ 'id', coursework.id])
            this.sendRequest(api, make_multipart_data(args, files), 'api-update-coursework-content')
        },
        buildCoursework: function (coursework) {
            let timeout = 15000
            const loading = this.$loading( {
                lock: true,
                text: '正在编译 ' + coursework.name + ' ...',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
            } )

            const retry = function ( coursework ) {
                this.$once( 'api-build', ( success, data ) => {

                    let result = false
                    if ( success ) {
                        if ( data.state === 'SUCCESS' ) {
                            loading.close()
                            coursework.state = COMPILED
                            result = true
                        }
                        else if ( data.state === 'FAILURE' ) {
                            loading.close()
                            coursework.state = FAILURE
                        }
                        else if ( timeout < 0 ) {
                            loading.close()
                            coursework.state = TIMEOUT
                        }
                        else {
                            timeout -= 3000
                            window.setTimeout( retry, 3000, coursework )
                            result = null
                        }
                    }
                    else
                        loading.close()

                    if ( result !== null )
                        this.$emit( 'api-build-coursework', result )
                } )

                const api = '/api/courseworks/' + coursework.id + '/build/'
                this.sendRequest(api, { data: coursework }, 'api-build')

            }.bind( this )

            this.$once( 'api-rebuild', ( success, data ) => {

                let result = false
                if ( success ) {
                    if ( data.state === 'SUCCESS' ) {
                        loading.close()
                        coursework.state = COMPILED
                        result = true
                    }
                    else if ( data.state === 'FAILURE' ) {
                        loading.close()
                        coursework.state = FAILURE
                    }
                    else {
                        retry( coursework )
                        result = null
                    }
                }
                else
                    loading.close()

                if ( result !== null )
                    this.$emit( 'api-build-coursework', result )

            } ).bind( this )

            coursework.state = BUILDING
            const api = '/api/courseworks/' + coursework.id + '/rebuild/'
            this.sendRequest(api, { data: coursework }, 'api-rebuild')
        },
        taskCoursework: function (coursework) {
            const api = '/api/courseworks/' + coursework.id + '/result/'
            this.sendRequest(api, { data: coursework }, 'api-task')
        },
    }
})
