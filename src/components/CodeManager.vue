<template>
  <el-container class="cb-coder h-100">
    <input type="file" accept=".c,.h" style="display:none" @change="onFileSelected">
    <el-aside>
      <div class="cb-card">
        <div class="cb-navbar">
          <span>{{ $t( '课程管理' ) }}</span>
          <div class="cb-toolbox">
            <el-button
              :title="$t( '删除当前课程和相关的课程文件' )"
              type="text"
              :disabled="!currentCourse"
              icon="el-icon-delete"
              @click="handleCourseRemove"></el-button>
            <el-button
              :title="$t( 'Change course title' )"
              type="text"
              :disabled="!currentCourse"
              icon="el-icon-edit"
              @click="handleCourseRename"></el-button>
            <el-button
              :title="$t( '刷新' )"
              type="text"
              icon="el-icon-refresh-right"
              @click="handleCourseRefresh"></el-button>
            <el-button
              :title="$t( '新增课程' )"
              type="text"
              icon="el-icon-document-add"
              @click="handleCourseAdd"></el-button>
          </div>
        </div>
        <el-select
          ref="course"
          v-model="courseIndex"
          @change="handleCourseChange"
          class="w-100"
          size="small"
          filterable
          clearable
          remote
          :remote-method="onFilterCourse"
          :loading="loadingCourse"
          :placeholder="$t( '请选择课程' )">
          <el-option
            v-for="(item, index) in matchedCourses"
            :key="item.id"
            :label="item.title"
            :value="index">
          </el-option>
        </el-select>
        <el-table
          :data="courseworkData"
          size="small"
          highlight-current-row
          @current-change="handleCourseworkSelect">
          <el-table-column
            property="name"
            sortable
            :label="$t( '课程文件' )">
            <template v-slot="scope">
              <span
                v-bind:class="{ 'cb-red-dot': isDirty( scope.row.state ),
                                'cb-tag-warning': isBuildFailed( scope.row.state ) }">
                {{ scope.row.name }}
              </span>
            </template>
          </el-table-column>
          <el-table-column
            fixed="right"
            align="right"
            width="100">
            <template v-slot:header>
              <el-button
                :title="$t( '新增文件' )"
                type="primary"
                plain
                size="mini"
                icon="el-icon-plus"
                @click="handleCourseworkAdd"></el-button>
              <el-button
                :title="$t( '保存文件' )"
                type="primary"
                plain
                size="mini"
                icon="el-icon-document-copy"
                @click="handleCourseworkSave"></el-button>
            </template>
            <template v-slot:default="scope">
              <el-button
                :title="$t( '保存' )"
                type="primary"
                size="mini"
                plain
                v-show="isDirty( scope.row.state )"
                icon="el-icon-document-copy"
                @click="handleCourseworkSave( scope.row )"></el-button>
              <el-button
                :title="$t( '编译并且运行' ) "
                type="primary"
                size="mini"
                plain
                v-show="isBuildEnabled( scope.row.state )"
                icon="el-icon-position"
                @click="handleCourseworkBuild( scope.row )"></el-button>
              <el-button
                :title="$t( '正在编译中' )"
                type="primary"
                size="mini"
                plain
                v-show="isBuilding( scope.row.state )"
                icon="el-icon-loading"></el-button>
              <el-dropdown
                trigger="hover"
                size="mini"
                @command="handleCourseworkCommand">
                <el-button
                  size="mini"
                  type="primary"
                  plain
                  class="el-icon-more">
                </el-button>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item
                    :command="{ action: 'rename', coursework: scope.row }">
                    {{ $t( '更改名称' ) }}
                  </el-dropdown-item>
                  <el-dropdown-item
                    :command="{ action: 'delete', coursework: scope.row }">
                    {{ $t( '删除' ) }}
                  </el-dropdown-item>
                  <el-dropdown-item
                    :command="{ action: 'download', coursework: scope.row }">
                    {{ $t( '下载' ) }}
                  </el-dropdown-item>
                  <el-dropdown-item
                    divided
                    :command="{ action: 'wrapmode', coursework: scope.row }">
                    {{ $t( '切换折行模式' ) }}
                  </el-dropdown-item>
                  <el-dropdown-item
                    :command="{ action: 'options', coursework: scope.row }">
                    {{ $t( '选项设置' ) }}
                  </el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-aside>
    <div class="cb-container">
      <cb-buffer-manager ref="editor"></cb-buffer-manager>
    </div>
  </el-container>
</template>

<script>
import { DIRTY, COMPILED, FAILURE, TIMEOUT, BUILDING } from '../definition.js'
import connector from '../connector.js'
import { _t } from '../plugins/gettext.js'

export default {
    name: 'CodeManager',
    props: {
        courseId: Number,
    },
    computed: {
        title: function () {
            let text = []
            if ( this.currentCourse )
                text.push( this.currentCourse.title )
            if ( this.currentCoursework )
                text.push( this.currentCoursework.name )
            return text.join( ': ' )
        }
    },
    data() {
        return {
            courseIndex: undefined,
            currentCourse: undefined,
            courseData: undefined,
            matchedCourses: [],
            currentCoursework: undefined,
            courseworkData: [],
            tempCourseworks: [],
            loadingCourse: false,
            cachedData: { 'pk_0': [] },
        }
    },
    mounted() {
        connector.$on('api-login', this.onLogin)
        connector.$on('api-logout', this.onLogout)
        if (connector.isAuthenticated)
            this.queryCourses()
    },
    methods: {
        clearData() {
            this.courseIndex = undefined
            this.currentCourse = undefined
            this.courseData = undefined
            this.matchedCourses = []
            this.currentCoursework = null
            this.courseworkData = []
            this.loadingCourse = false
            this.cachedData = {
                'pk_0': this.cachedData[ 'pk_0' ]
            }
        },
        refreshData() {
            this.clearData()
            this.queryCourses()
        },
        queryCourses() {
            connector.$once('api-list-courses', this.onListCourses)
            connector.listCourses()
        },
        queryCourseItems(course) {
            connector.$once('api-list-course-items', this.onListCourseItems)
            connector.listCourseItems(course)
        },
        isDirty( state ) {
            return  state === DIRTY
        },
        isBuildFailed( state ) {
            return state === FAILURE || state === TIMEOUT
        },
        isBuilding( state ) {
            return state === BUILDING
        },
        isBuildEnabled( state ) {
            return [ 0, COMPILED, FAILURE, TIMEOUT ].indexOf( state ) > -1
        },

        //
        // Common onXXX
        //
        onLogin: function (success) {
            if (success)
                this.refreshData()
        },
        onLogout: function (success) {
            if (success)
                this.clearData()
        },

        //
        // onCourseXXX
        //
        onFilterCourse: function (query) {
            if (this.courseData) {
                this.matchedCourses = this.courseData.filter( item => {
                    return item.title.indexOf(query) > -1
                } )
            }
         },
        onListCourses: function (success, data) {
            this.loadingCourse = false
            if (success) {
                this.courseData = data
                this.matchedCourses = data.filter( () => true )
            }
        },
        onListCourseItems: function (success, data) {
            if (success) {
                data.forEach( item => {
                    item.state = 0
                } )
                this.courseworkData = data
            }
        },
        onCourseCreated: function (success, data) {
            if (success) {
                this.courseData.push(data)
                this.matchedCourses.push(data)
                this.handleCourseChange(this.matchedCourses.length - 1)
            }
        },
        onCourseRemoved: function (success) {
            if (success && this.currentCourse) {
                let index = this.courseData.indexOf(this.currentCourse)
                this.courseData.splice(index, 1)
                this.matchedCourses.splice(this.courseIndex, 1)
                if (this.matchedCourses.length) {
                    if (this.courseIndex >= this.matchedCourses.length)
                        this.handleCourseChange(this.courseIndex - 1)
                    else
                        this.handleCourseChange(this.courseIndex)
                }
                else {
                    this.handleCourseChange(undefined)
                }
            }
        },
        onCourseRenamed: function (success, data) {
            if (success && this.currentCourse) {
                this.currentCourse.title = data.title
                this.$refs.course.$el.querySelector('input.el-input__inner').value = data.title
                this.$emit( 'title-changed', this.title )
            }
        },

        //
        // handleCourseXXX
        //
        handleCourseAdd: function () {
            if ( ! connector.isAuthenticated ) {
                this.$message( _t( '未登录用户不能创建课程' ) )
                return
            }

            this.$prompt( _t( '请输入课程名称' ), _t( '创建课程' ), {
                inputValue: _t( '第一节课' ),
                callback: (action, instance) => {
                    if (action === 'confirm') {
                        connector.$once('api-new-course', this.onCourseCreated)
                        connector.newCourse({ title: instance.inputValue })
                    }
                }
            })
        },
        handleCourseRename: function () {
            if (this.currentCourse) {
                this.$prompt( _t( '请输入课程的新名称' ), _t( '修改课程' ), {
                    inputValue: this.currentCourse.title,
                    callback: (action, instance) => {
                        if (action === 'confirm') {
                            connector.$once('api-update-course', this.onCourseRenamed)
                            connector.updateCourse({
                                id: this.currentCourse.id,
                                title: instance.inputValue
                            })
                        }
                    }
                })
            }
        },
        handleCourseRemove: function () {
            if (this.currentCourse) {
                this.$confirm( _t( '确认删除课程: %1 ?', this.currentCourse.title ), _t( '确认' ), {
                    type: 'warning',
                    callback: (action) => {
                        if (action === 'confirm') {
                            connector.$once('api-remove-course', this.onCourseRemoved)
                            connector.removeCourse(this.currentCourse)
                        }
                    }
                })
            }
        },
        handleCourseRefresh: function () {
            this.refreshData()
            this.$refs.course.focus()
        },
        handleCourseChange: function ( index ) {
            let prefix = 'pk_'
            if ( this.currentCourse === undefined )
                this.cachedData[ prefix + '0'] = this.courseworkData
            else if ( this.currentCourse && this.courseworkData && this.courseworkData.length )
                this.cachedData[ prefix + this.currentCourse.id ] = this.courseworkData

            this.courseIndex = index
            this.currentCourse =  index === undefined ? undefined : this.matchedCourses[index]

            this.currentCoursework = undefined
            this.$refs.editor.handleCourseworkSelect()

            if ( this.currentCourse === undefined )
                this.courseworkData = this.cachedData[ prefix + '0' ]

            else {
                let key = prefix + this.currentCourse.id
                if ( Object.prototype.hasOwnProperty.call( this.cachedData, key ) )
                    this.courseworkData = this.cachedData[ key ]
                else
                    this.queryCourseItems(this.currentCourse)
            }
            this.$emit( 'title-changed', this.title )
        },

        //
        // Coursework functions
        //
        addCoursework( name ) {
            connector.$once('api-new-coursework', this.onCourseworkCreated)
            let content = '/* CodeBang Course: ' + name + '*/'
            connector.newCoursework(name, content, this.currentCourse)
        },
        removeCoursework ( coursework ) {
            if ( coursework ) {
                for ( let index = 0; index < this.courseworkData.length; index ++ )
                    if ( this.courseworkData[ index ].id === coursework.id ) {
                        this.courseworkData.splice( index, 1 )
                        if ( ! this.courseworkData.length )
                            this.handleCourseworkSelect( undefined )
                        else if ( index < this.courseworkData.length )
                            this.handleCourseworkSelect( this.courseworkData[ index ] )
                        else
                            this.handleCourseworkSelect( this.courseworkData[ index - 1 ] )
                        break
                    }
                this.$refs.editor.handleCourseworkClose( coursework )
            }
        },

        //
        // onCourseworkXXX
        //
        onCourseworkCreated: function (success, data) {
            if ( success ) {
                data.state = 0
                this.courseworkData.push( data )
                this.handleCourseworkSelect( data )
            }
        },

        //
        // handleCourseworkXXX
        //
        handleCourseworkSelect: function ( coursework ) {
            this.currentCoursework = coursework
            this.$refs.editor.handleCourseworkSelect( coursework )
            this.$emit( 'changed', coursework )
            this.$emit( 'title-changed', this.title )
        },
        handleCourseworkAdd: function () {
            this.$prompt( _t( '请输入文件名称' ), _t( '创建代码文件' ), {
                inputValue: 'foo.c',
                callback: ( action, instance ) => {
                    if ( action === 'confirm' && instance.inputValue ) {
                        this.addCoursework( instance.inputValue )
                        if ( this.currentCourse === undefined )
                            this.$message( {
                                type: 'info',
                                message: _t( '注意：当前没有课程被选中，所以增加的文件都是临时文件，' +
                                             '当前页面一旦被关闭之后就无法在找回' ),
                                showClose: true,
                                duration: 6000
                            } )
                    }
                }
            })
        },
        handleCourseworkSave: function ( coursework ) {
            this.$refs.editor.handleCourseworkSave( coursework )
        },
        handleCourseworkRename: function ( coursework ) {
            if ( coursework ) {
                this.$prompt( _t( '请输入文件的新名称' ), _t( '修改文件名称' ), {
                    inputValue: coursework.name,
                    callback: (action, instance) => {
                        if (action === 'confirm') {
                            coursework.name = instance.inputValue
                            coursework.state = DIRTY
                            this.$refs.editor.handleCourseworkSave( coursework )
                        }
                    }
                })
            }
        },
        handleCourseworkRemove: function ( coursework ) {
            if ( coursework ) {
                this.$confirm( _t( '确认删除文件: %1 ?', coursework.name ), _t( '确认' ), {
                    type: 'warning',
                    callback: (action) => {
                        if (action === 'confirm') {
                            connector.$once( 'api-remove-coursework', success => {
                                if ( success )
                                    this.removeCoursework( coursework )
                            } )
                            connector.removeCoursework( coursework )
                        }
                    }
                })
            }
        },
        handlecourseworkbuild: function ( coursework ) {
            if ( coursework && coursework.state === COMPILED )
                this.pageIndex = 2
            else if ( coursework ) {
                connector.$once( 'api-build-coursework', success => {
                    if ( ! success )
                        this.$message( _t( '编译出错了' ) )
                } )
                connector.buildCoursework( coursework )
            }
        },
        handleCourseworkCommand: function ( command ) {
            if ( command.action === 'rename' )
                this.handleCourseworkRename( command.coursework )
            else if ( command.action === 'delete' )
                this.handleCourseworkRemove( command.coursework )
            else if ( command.action === 'download' )
                this.handleCourseworkDownload( command.coursework )
            else if ( command.action === 'wrapmode' )
                this.handleWrapModeToggle( command.coursework )
            else if ( command.action === 'options' )
                this.handleBufferSetting( command.coursework )
        },
        handleWrapModeToggle: function ( coursework ) {
            this.$refs.editor.handleCourseworkChangeSetting( coursework, {
                wrapMode: 'toggle',
            } )
        },
        handleBufferSetting: function ( coursework ) {
            this.$refs.editor.handleCourseworkChangeSetting( coursework )
        },

        //
        // Local file
        //
        onFileSelected: function () {
            let file = this.$el.querySelector('input[type="file"]').files[0]
            let reader = new FileReader()
            let session = this.$refs.editor.getBuffer( this.currentCoursework ).session
            reader.onload = (evt) => {
                session.setValue(evt.target.result)
                session.selection.clearSelection()
                session.gotoLine(1)
                session.focus()
            }
            reader.readAsText(file)
        },
        handleCourseworkUpload: function () {
            this.$el.querySelector('input[type="file"]').click()
        },
        handleCourseworkDownload: function ( coursework ) {
            let buf = this.$refs.editor.getBuffer( coursework )
            let text = buf && buf.session.getValue()
            if (text && text.length) {
                var blob = new Blob([text], {type: 'text/plain'})
                var reader = new FileReader()
                reader.onload = (evt) => {
                    var a = document.createElement('a')
                    a.href = evt.target.result
                    a.setAttribute('download', coursework.name)
                    a.click()
                }
                reader.readAsDataURL(blob)
                // var url = URL.createObjectURL(blob);
                // URL.revokeObjectURL(url);
            }
        },
    }
}
</script>

<style>
/* Color themem */
.cb-coder .cb-card .el-input__inner,
.cb-coder .cb-card .el-table,
.cb-coder .cb-card .el-table * {
    background-color: inherit;
    color: inherit;
}

.cb-coder .cb-card .el-table .el-table__body tr.current-row.hover-row td,
.cb-coder .cb-card .el-table .el-table__body tr:hover {
    background-color: #3f3f3f;
}

.cb-coder .cb-card .el-table .el-table__body tr.current-row {
    background-color: #454545;
}

.cb-coder .cb-card .el-table::before,
.cb-coder .cb-card .el-table .el-table__fixed-right::before {
    background-color: #666;
}

/* Border, padding and margin */
.cb-coder .cb-card {
    border: 0;
    padding: 9px 16px;
    max-height: 100%;
}

.cb-coder .cb-card > * {
    margin-bottom: 9px;
}

.cb-coder .cb-card .el-button {
    border: 0;
    padding: 2px 6px;
    margin-left: 6px;
}

.cb-coder .cb-card .el-table td {
    cursor: pointer;
}

.cb-coder .el-aside,
.cb-coder .cb-card .el-input__inner {
    border: 1px solid #666;
}

.cb-coder .cb-card .el-table td {
    border-bottom: 0;
}

.cb-coder .cb-card .el-table th.is-leaf {
    border-bottom: 1px solid #666;
}

.cb-coder .cb-card .el-table .el-table__body tr > td:first-child {
    border-left: 1px solid #666;
}
.cb-coder .cb-card .el-table .el-table__body tr > td:last-child {
    border-right: 1px solid #666;
}

/* Status */
.cb-red-dot::after {
    background-color: rgba(245, 110, 110, 0.3);
    content: '';
    height: 9px;
    width: 9px;
    position: absolute;
    top: 2px;
    left: 2px;
    border-radius: 50%;
}
.cb-tag-warning::after {
    background-color: rgba(227, 162, 195, 0.3);
    content: '';
    height: 9px;
    width: 9px;
    position: absolute;
    top: 2px;
    left: 2px;
    border-radius: 50%;
}
</style>
