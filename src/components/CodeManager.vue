<template>
  <el-container class="cb-container">
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
                @click="handleCourseUpdate"></el-button>
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
            @current-change="handleCourseworkChange">
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
                    <el-dropdown-item
                      @click="handleCourseworkRemove(scope.row)">删除
                    </el-dropdown-item>
                    <el-dropdown-item divided>切换折行模式</el-dropdown-item>
                    <el-dropdown-item>切换Tab宽度(4)</el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </template>
            </el-table-column>
          </el-table>
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
        currentCourse: function () {
            return this.courseIndex === undefined ? null : this.matchedCourses[this.courseIndex]
        },
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
        }
    },
    mounted() {
        connector.$on('api-login', this.onLogin)
        connector.$on('api-logout', this.onLogout)
        this.$on('coder-select-file', this.$refs.editor.onBufferSelected)
        // this.$watch( this.dirtyFlag, value => {
        //     if (value)
        //         this.setSaveFlags()
        // } )
    },
    methods: {
        clearData() {
            this.courseIndex = undefined
            this.courseData = undefined
            this.matchedCourses = []
            this.currentCoursework = null
            this.courseworkData = []
            this.loadingCourse = false
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

        onFilterCourse: function (query) {
            if (this.courseData) {
                this.matchedCourses = this.courseData.filter( item => {
                    return item.title.indexOf(query) > -1
                } )
            }
         },
        onLogin: function (success) {
            if (success)
                this.refreshData()
        },
        onLogout: function (success) {
            if (success)
                this.clearData()
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
                data.forEach( item => item.dirty = false )
                this.courseworkData = data
            }
        },
        onCourseCreated: function (success, data) {
            if (success) {
                this.courseData.push(data)
                this.matchedCourses.push(data)
                this.courseIndex = this.matchedCourses.length - 1
                this.handleCourseChange()
            }
        },
        onCourseRemoved: function (success) {
            if (success && this.currentCourse) {
                let index = this.courseData.indexOf(this.currentCourse)
                this.courseData.splice(index, 1)
                this.matchedCourses.splice(this.courseIndex, 1)
                if (this.matchedCourses.length) {
                    if (this.courseIndex >= this.matchedCourses.length)
                        this.courseIndex --
                    else
                        this.handleCourseChange()
                }
                else {
                    this.courseIndex = undefined
                    this.currentCoursework = undefined
                    this.courseworkData = []
                }
            }
        },
        onCourseUpdated: function (success, data) {
            if (success && this.currentCourse) {
                this.currentCourse.title = data.title
                this.$refs.course.$el.querySelector('input.el-input__inner').value = data.title
            }
        },

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
        handleCourseUpdate: function () {
            if (this.currentCourse) {
                this.$prompt('请输入课程的新名称', '修改课程', {
                    inputValue: this.currentCourse.title,
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    callback: (action, instance) => {
                        if (action === 'confirm') {
                            connector.$once('api-update-course', this.onCourseUpdated)
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
        handleCourseChange: function () {
            if (this.currentCourse) {
                this.queryCourseItems(this.currentCourse)
            }
            else {
                this.currentCoursework = undefined
                this.courseworkData = []
            }
        },

        onCourseworkCreated: function (success, data) {
            if (success) {
                this.courseworkData.push(data)
                this.$emit('coder-new-file', data)
            }
        },

        handleCourseworkChange: function (coursework) {
            this.currentCoursework = coursework
            this.$emit('coder-select-file', coursework)
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
        handleCourseworkSave: function () {
            if (this.currentCoursework) {
                connector.$once('api-save-coursework', this.onUpdateCoursewrok)
                connector.updateCoursework(this.currentCoursework)
                this.$emit('coder-save-file', this.currentCoursework)
            }
        },
        handleCourseworkRename: function () {
            if (this.currentCoursework) {
                connector.$once('api-update-coursework-name', this.onUpdateCoursewrok)
                connector.updateCoursework(this.currentCoursework)
                this.$emit('coder-rename-file', this.currentCoursework)
            }
        },
        handleCourseworkRemove: function (coursework) {
            connector.$once('api-remove-coursework', this.onRemoveCoursewrok)
            connector.removeCoursework(coursework)
            this.$emit('coder-remove-file', coursework)
        },
        handleCourseworkBuild: function (coursework) {
            connector.$once('api-build-coursework', this.onBuildCoursewrok)
            connector.buildCoursework(coursework)
            this.$emit('coder-build-file', coursework)
        },
    }
}
</script>

<style>
/* Color themem */
.cb-code-manager .el-card,
.cb-code-manager .el-card .el-input__inner,
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
    border-left: 1px solid #666;
}
.cb-code-manager .el-card .el-table .el-table__body tr > td:last-child {
    border-right: 1px solid #666;
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
</style>
