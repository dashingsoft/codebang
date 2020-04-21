<template>
  <el-container class="cb-container">
    <input type="file" accept=".c,.h" style="display:none" @change="onFileSelected">
    <el-aside style="padding: 2px">
      <div class="cb-code-manager cb-container">
        <el-card class="cb-container">
          <div class="cb-navbar">
            <span>课程管理</span>
            <div class="cb-toolbox">
              <el-button
                title="删除当前课程和相关的课程文件"
                type="text"
                :disabled="!currentCourse"
                icon="el-icon-delete"
                @click="handleCourseRemove"></el-button>
              <el-button
                title="修改课程名称"
                type="text"
                :disabled="!currentCourse"
                icon="el-icon-edit"
                @click="handleCourseRename"></el-button>
              <el-button
                title="刷新"
                type="text"
                icon="el-icon-refresh-right"
                @click="handleCourseRefresh"></el-button>
              <el-button
                title="新增课程"
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
            filterable
            clearable
            remote
            :remote-method="onFilterCourse"
            :loading="loadingCourse"
            placeholder="请选择课程">
            <el-option
              v-for="(item, index) in matchedCourses"
              :key="item.id"
              :label="item.title"
              :value="index">
            </el-option>
          </el-select>
          <el-table
            :data="courseworkData"
            empty-text="没有内容"
            highlight-current-row
            @current-change="handleCourseworkSelect">
            <el-table-column
              property="name"
              sortable
              label="课程文件">
              <template v-slot="scope">
                <span
                  v-bind:class="{ 'cb-red-dot': courseworkData[scope.$index].dirty }">
                  {{ scope.row.name }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              fixed="right"
              align="right"
              width="80">
              <template v-slot:header>
                <el-button
                  title="新增文件"
                  type="primary"
                  plain
                  size="mini"
                  icon="el-icon-plus"
                  @click="handleCourseworkAdd"></el-button>
                <el-button
                  title="保存文件"
                  type="primary"
                  plain
                  size="mini"
                  icon="el-icon-document-copy"
                  @click="handleCourseworkSave"></el-button>
              </template>
              <template v-slot:default="scope">
                <el-button
                  title="编译和运行"
                  type="primary"
                  size="mini"
                  plain
                  icon="el-icon-position"
                  @click="handleCourseworkBuild(scope.row)"></el-button>
                <el-dropdown trigger="hover">
                  <el-button
                    size="mini"
                    type="primary"
                    plain
                    class="el-icon-more">
                  </el-button>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item>更改名称</el-dropdown-item>
                    <el-dropdown-item>下载</el-dropdown-item>
                    <el-dropdown-item
                      @click="handleCourseworkRemove(scope.row)">删除</el-dropdown-item>
                    <el-dropdown-item divided>切换折行模式</el-dropdown-item>
                    <el-dropdown-item>选项设置</el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            small
            layout="prev, pager, next"
            :hide-on-single-page="true"
            :total="5">
          </el-pagination>
        </el-card>
      </div>
    </el-aside>
    <el-main style="padding: 2px;">
      <cb-buffer-manager ref="editor"></cb-buffer-manager>
    </el-main>
  </el-container>
</template>

<script>
import connector from '../connector.js'

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
            courseData: undefined,
            matchedCourses: [],
            currentCoursework: undefined,
            courseworkData: [],
            loadingCourse: false,
            dirtyFlag: false,
            cachedData: {},
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
            this.courseData = undefined
            this.matchedCourses = []
            this.currentCoursework = null
            this.courseworkData = []
            this.loadingCourse = false
            this.cachedData = {}
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
                    item.dirty = false
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
            this.$prompt('请输入课程名称', '创建课程', {
                inputValue: '第一节课',
                confirmButtonText: '确定',
                cancelButtonText: '取消',
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
                this.$prompt('请输入课程的新名称', '修改课程', {
                    inputValue: this.currentCourse.title,
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
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
                this.$confirm('确认删除课程: ' + this.currentCourse.title + '?', '确认', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
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
            if ( this.currentCourse && this.courseworkData && this.courseworkData.length )
                this.cachedData[ prefix + this.currentCourse.id ] = this.courseworkData

            this.courseIndex = index
            this.currentCourse =  index === undefined ? undefined : this.matchedCourses[index]

            this.currentCoursework = undefined
            this.$refs.editor.handleCourseworkSelect()

            if ( this.currentCourse === undefined )
                this.courseworkData = []

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
        // onCourseworkXXX
        //
        onCourseworkCreated: function (success, data) {
            if ( success ) {
                data.dirty = false
                data.state = 0
                this.courseworkData.push( data )
                this.handleCourseworkSelect( data )
            }
        },
        onCourseworkRemoved: function ( success ) {
            if ( success && this.currentCoursework ) {
                for ( let index = 0; index < this.courseworkData.length; index ++ )
                    if ( this.courseworkData[ index ] === this.currentCoursework ) {
                        this.currentCoursework = undefined
                        this.courseworkData.pop( index )

                        if ( ! this.courseworkData.length )
                            this.handleCourseworkSelect( undefined )
                        else if ( index < this.courseworkData.length )
                            this.handleCourseworkSelect( this.courseworkData[ index ] )
                        else
                            this.handleCourseworkSelect( this.courseworkData[ index - 1 ] )
                        break
                    }
            }
        },

        //
        // handleCourseworkXXX
        //
        handleCourseworkSelect: function ( coursework ) {
            this.currentCoursework = coursework
            this.$refs.editor.handleCourseworkSelect( coursework )
            this.$emit( 'title-changed', this.title )
        },
        handleCourseworkAdd: function () {
            this.$prompt('请输入文件名称', '创建代码文件', {
                inputValue: 'foo.c',
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                callback: (action, instance) => {
                    if (action === 'confirm') {
                        connector.$once('api-new-coursework', this.onCourseworkCreated)
                        let name = instance.inputValue
                        let content = '/* CodeBang Course: ' + name + '*/'
                        connector.newCoursework(name, content, this.currentCourse)
                    }
                }
            })
        },
        handleCourseworkSave: function ( coursework ) {
            this.$refs.editor.handleCourseworkSave( coursework )
        },
        handleCourseworkRename: function ( coursework ) {
            if ( coursework ) {
                this.$prompt('请输入文件的新名称', '修改文件名称', {
                    inputValue: coursework.name,
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    callback: (action, instance) => {
                        if (action === 'confirm') {
                            coursework.name = instance.inputValue
                            this.$refs.editor.handleCourseworkSave( coursework )
                        }
                    }
                })
            }
        },
        handleCourseworkRemove: function ( coursework ) {
            if ( coursework ) {
                connector.$once( 'api-remove-coursework', this.onCoursewrokRemoved )
                connector.removeCoursework( coursework )
                 this.$refs.editor.handleCourseworkClose( coursework )
            }
        },
        handleCourseworkBuild: function ( coursework ) {
            if ( coursework ) {
                // connector.$once('api-build-coursework', this.onBuildCoursewrok)
                connector.buildCoursework( coursework )
                this.$emit( 'coder-build', coursework )
            }
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
        handleUploadFile: function () {
            this.$el.querySelector('input[type="file"]').click()
        },
        handleDownloadFile: function ( coursework ) {
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
.cb-code-manager .el-card,
.cb-code-manager .el-card .el-input__inner,
.cb-code-manager .el-card .el-pagination,
.cb-code-manager .el-card .el-pagination li,
.cb-code-manager .el-card .el-pagination button,
.cb-code-manager .el-card .el-table,
.cb-code-manager .el-card .el-table * {
    background-color: inherit;
    color: inherit;
}

.cb-code-manager .el-card .el-table .el-table__body tr.current-row.hover-row td,
.cb-code-manager .el-card .el-table .el-table__body tr:hover {
    background-color: #3f3f3f;
}

.cb-code-manager .el-card .el-table .el-table__body tr.current-row {
    background-color: #454545;
}

.cb-code-manager .el-card,
.cb-code-manager .el-card .el-input__inner {
    border: 1px solid #666;
}

.cb-code-manager .el-card .el-table td,
.cb-code-manager .el-card .el-table th.is-leaf {
    border-bottom: 1px solid #666;
}

.cb-code-manager .el-card .el-table .el-table__body tr > td:first-child {
    /* border-left: 1px solid #666; */
}
.cb-code-manager .el-card .el-table .el-table__body tr > td:last-child {
    /* border-right: 1px solid #666; */
}

.cb-code-manager .el-card .el-table::before,
.cb-code-manager .el-card .el-table .el-table__fixed-right::before {
    background-color: #666;
}

.cb-code-manager .el-card__body .el-table .el-button {
    border: 0;
}

/* Padding and margin */
.cb-code-manager .el-card__body {
    padding: 9px 16px;
}

.cb-code-manager .el-card__body > * {
    margin-bottom: 9px;
}

.cb-code-manager .el-card__body .el-table td {
    padding: 6px 0;
    cursor: pointer;
}

.cb-code-manager .el-card__body .el-button {
    padding: 2px 6px;
    margin-left: 6px;
}

.cb-code-manager .el-card__body .el-table .is-right > .cell {
    padding: 0 6px;
}

.cb-code-manager .el-card .el-pagination {
    text-align: center;
    margin-top: 16px;
}

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

</style>
