<template>
  <div class="cb-code-manager cb-container">
    <el-card class="cb-container">
      <div class="cb-titlebar">
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
        v-model="courseIndex"
        @change="handleCourseChange"
        class="w-100"
        filterable
        clearable
        remote
        :remote-method="onSearchCourse"
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
        </el-table-column>
        <el-table-column
          fixed="right"
          align="right"
          width="80">
          <template slot="header" slot-scope="scope">
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
              @click="handleCourseworkSave(scope.$index)"></el-button>
          </template>
          <template slot-scope="scope">
            <el-button
              title="编译和运行"
              type="primary"
              size="mini"
              plain
              icon="el-icon-position"
              @click="handleCourseworkBuild(scope.$index)"></el-button>
            <el-dropdown trigger="hover">
              <el-button
                size="mini"
                type="primary"
                plain
                class="el-icon-more">
            </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item
                  @click="handleCourseworkRemove(scope.$index)">删除
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
        currentCoursework: function () {
            return this.courseIndex === undefined ? null : this.courseData[this.courseIndex]
        },
    },
    data() {
        return {
            courseIndex: undefined,
            courseworkIndex: undefined,
            courseData: undefined,
            matchedCourses: [],
            courseworkData: [],
            loadingCourse: false,
        }
    },
    mounted() {
        connector.$on('api-login', this.onLogin)
        connector.$on('api-logout', this.onLogout)
    },
    methods: {
        clearData() {
            this.courseIndex = undefined
            this.courseworkIndex = undefined
            this.courseData = undefined
            this.matchedCourses = []
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

        onSearchCourse: function (query) {
            if (this.courseData === undefined) {
                this.loadingCourse = true
                this.queryCourses()
            }
            else {
                this.loadingCourse = false
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
                this.matchedCourses = data
            }
        },
        onListCourseItems: function (success, data) {
            if (success)
                this.courseworkData = data
        },
        onCourseCreated: function (success, data) {
            if (success) {
                this.courseData.push(data)
                this.matchedCourses.push(data)
                this.courseIndex = this.matchedCourses.length - 1
            }
        },
        onCourseRemoved: function (success) {
            if (success && this.currentCourse) {
                this.courseworkIndex = undefined
                this.courseworkData = []
            }
        },

        handleCourseAdd: function () {
            this.$prompt('请输入课程名称', '创建课程', {
                inputValue: 'foo.c',
                confirmButtonText: '确定',
                cancelButtonText: '取消',
            }).then(({ value }) => {
                let data = {
                    'title': value
                }
                connector.$once('api-new-course', this.onCourseCreated)
                connector.newCourse(data)
            })
        },
        handleCourseUpdate: function () {
            if (this.currentCourse) {
                connector.$once('api-update-course', this.onCourseUpdated)
                connector.updateCourse(this.currentCourse)
            }
        },
        handleCourseRemove: function () {
            let course = this.currentCourse
            if (course) {
                this.$confirm('确认删除课程: ' + course.title + '?', '确认', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    connector.$once('api-remove-course', this.onCourseRemoved)
                    connector.removeCourse(course)
                })
            }
        },
        handleCourseRefresh: function () {
            this.refreshData()
        },
        handleCourseChange: function () {
            if (this.currentCourse) {
                this.queryCourseItems(this.currentCourse)
            }
            else {
                this.courseworkIndex = undefined
                this.courseworkData = []
            }
        },

        handleCourseworkChange: function (index) {
            this.courseworkIndex = index
        },
        handleCourseworkAdd: function () {
        },
        handleCourseworkSave: function () {
            const coursework = this.courseworkIndex
            connector.$once('api-update-coursework', this.onUpdateCoursewrok)
            connector.updateCoursework(coursework)
        },
        handleCourseworkUpdate: function (index) {
            const coursework = this.courseworkData[index]
            connector.$once('api-update-coursework', this.onUpdateCoursewrok)
            connector.updateCoursework(coursework)
        },
        handleCourseworkRemove: function (index) {
            const coursework = this.courseworkData[index]
            connector.$once('api-remove-coursework', this.onRemoveCoursewrok)
            connector.removeCoursework(coursework)
        },
        handleCourseworkBuild: function (index) {
            const coursework = this.courseworkData[index]
            connector.$once('api-build-coursework', this.onBuildCoursewrok)
            connector.buildCoursework(coursework)
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

.w-100 {
    width: 100%;
}

</style>
