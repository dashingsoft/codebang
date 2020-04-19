import Vue from 'vue'
import reqwest from './reqwest.js'

const serverUrl = 'http://localhost:9092'

const ACCESS_TOKEN_KEY = 'ACCESS_TOKEN'
const REFERSH_TOKEN_KEY = 'REFRESH_TOKEN'

const clientId = '0gvr1GFNpCy9fSpxsKHPdUPUu7ZSCQS76zc8kAgl'
const clientSecret = 'dazoA4IhCGrWrkh2rA02FE1qm3AVWdAz9qKqSZDLAD22xWiVYsEeMtq2BmqVY748U8Qw9jecBo9BHYYG3nZDgOUUwaEFjjDir1VX25ejnCvEcwdzV3Wt2Rxcnt45lxaN'

// Fix this issue:
//   Do not access Object.prototype method ‘hasOwnProperty’ from target object no-prototype-builtins
const hasOwnProperty = Object.prototype.hasOwnProperty.call

// For debug
const crossOrigin = true;

let cachedData = {}

const get_key = function (key) {
    if (Object.prototype.hasOwnProperty(cachedData, key) && cachedData[key])
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
        Vue.prototype.$message({
            type: 'warning',
            message: '当前浏览器无法保存登陆信息，关闭页面之后登陆信息会丢失',
            showClose: true,
            duration: 0
        })
    }
}

const is_authenticated = function () {
    return !!get_key(ACCESS_TOKEN_KEY)
}

const request_token = function (url, data, callback) {
    reqwest( {
        url: url,
        method: 'post',
        type: 'json',
        contentType: 'application/json',
        headers: {
            Authorization: 'Basic ' + btoa(clientId + ':' + clientSecret)
        },
        data: data,
        crossOrigin: crossOrigin,
        success: function (data) {
            set_key(ACCESS_TOKEN_KEY, data['access_token'])
            set_key(REFRESH_TOKEN_KEY, data['refresh_token'])
            callback(true)
        },
        error: function (r, msg, err) {
            callback( false, {
                status: r.status,
                statusText: r.statusText,
                message: !!msg ? msg :
                    hasOwnProperty(r.response, 'error') ? r.response.error :
                    hasOwnProperty(err, 'message') ? err.message :
                    ''
            } )
        }
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

const revoke_token(callback) {
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
        contentType: 'application/json',
        data: data,
        crossOrigin: crossOrigin,
        success: function (data) {
            set_key(ACCESS_TOKEN_KEY, null)
            set_key(REFRESH_TOKEN_KEY, null)
            callback(true)
        },
        error: function (r, msg, err) {
            callback( false, {
                status: r.status,
                statusText: r.statusText,
                message: !!msg ? msg :
                    hasOwnProperty(r.response, 'error') ? r.response.error :
                    hasOwnProperty(err, 'message') ? err.message :
                    ''
            } )
        }
    } )
}

const request_api = function (api, method, data, callback, complete) {
    const url = serverUrl + api.slice(-1) === '/' ? api : (api + '/')
    reqwest( {
        url: url,
        method: method,
        type: 'json',
        contentType: 'application/json',
        headers: {
            Authorization: 'Bearer ' + get_key(ACCESS_TOKEN_KEY)
        },
        data: data,
        crossOrigin: crossOrigin,
        success: function (data) {
            callback(true, data)
        },
        error: function (r, msg, err) {
            callback( false, {
                status: r.status,
                statusText: r.statusText,
                message: !!msg ? msg :
                    hasOwnProperty(r.response, 'detail') ? r.response.detail :
                    hasOwnProperty(err, 'message') ? err.message :
                    ''
            } )
        },
        complete: complete
    } )
}

const upload_file = function (api, data, callback, complete) {
    let file = new File( [filedata], filename, { type: 'text/plain' } )
    paras.data = JSON.stringify( { file: file } )
    paras.contentType = 'multipart/form-data'
    reqwest( paras );
}

const download_file = function (api, callback, complete) {
}

export default new Vue({
    data() {
        return {
            connected: false,
        }
    },
    methods: {
        showError(err) {
            Vue.prototype.$message({
                type: 'error',
                message: err,
                showClose: true,
                duration: 0
            })
        },
        sendRequest: function (api, data, event, text) {
            const method = event.startswith('api-new') ? 'post' :
                  api.startswith('api-update') ? 'put' :
                  api.startswith('api-remove') ? 'delete' : 'get'
            const refresh_callback = function (success) {
                if (success)
                    this.sendRequest(api, data, event, text)
                else {
                    if (!!data.message)
                        this.showError(data.message)
                    this.$emit(event + '-fail')
                }
            }
            const callback = function (success, data) {
                if (success)
                    this.$emit(event, data)
                else if (data.status === 401 && is_authenticated()) {
                    refresh_token(refresh_callback)
                }
                else {
                    if (!!data.message)
                        this.showError(data.message)
                    this.$emit(event + '-fail')
                }
            }
            if (!text) {
                request_api(api, method, data, callback)
            }
            else {
                const loading = this.$loading( {
                    lock: true,
                    text: text,
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)'
                } )
                request_api(api, method, data, callback, loading.close)
            }
        },
        login(username, password) {
            const callback = function (success) {
                if (success)
                    this.$emit('api-login')
                else {
                    if (!!data.message)
                        this.showError(data.message)
                    this.$emit('api-login-fail')
                }
            }
            get_token(username, password, callback)
        },
        logout() {
            const callback = function (success) {
                if (success)
                    this.$emit('api-logout')
                else {
                    if (!!data.message)
                        this.showError(data.message)
                    this.$emit('api-logout-fail')
                }
            }
            revoke_token(callback)
        },
        newCourse: function (course) {
            const api = '/api/courses/'
            this.sendRequest(api, course, 'api-new-course')
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
            this.sendRequest(api, course, 'api-update-course')
        },
        removeCourse: function (course) {
            const api = '/api/courses/' + course.id
            this.sendRequest(api, course, 'api-remove-course')
        },
        listCourseItems: function (course) {
            const api = '/api/courses/' + course.id + '/items/'
            this.sendRequest(api, {}, 'api-list-course-items')
        },
        newCoursework: function (coursework) {
            const api = '/api/courseworks/'
            this.sendRequest(api, coursework, 'api-new-coursework')
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
            this.sendRequest(api, coursework, 'api-update-coursework')
        },
        removeCoursework: function (coursework) {
            const api = '/api/courseworks/' + coursework.id
            this.sendRequest(api, coursework, 'api-remove-coursework')
        },
        getCourseworkContent: function (coursework) {
            const api = '/api/courseworks/' + coursework.id + '/content/'
            this.sendRequest(api, {}, 'api-get-coursework')
        },
        buildCoursework: function (coursework) {
            const api = '/api/courseworks/' + coursework.id + '/build/'
            this.sendRequest(api, coursework, 'api-build-coursework')
        },
        taskCoursework: function (coursework) {
            const api = '/api/courseworks/' + coursework.id + '/task/'
            this.sendRequest(api, coursework, 'api-task-coursework')
        },
    }
})
