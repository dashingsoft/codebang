<template>
  <div class="cb-course-manage cb-container">
    <el-card class="cb-container">
      <div class="cb-titlebar">
        <span>课程管理</span>
        <div class="cb-toolbox">
          <el-button
            title="删除当前课程和相关的课程文件"
            type="text"
            :disabled="courseIndex === -1"
            icon="el-icon-delete"
            @click="handleCourseRemove"></el-button>
          <el-button
            title="修改课程名称"
            type="text"
            :disabled="courseIndex === -1"
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
        @change="handleCourseChange"
        class="w-100"
        filterable
        clearable
        placeholder="请选择课程">
        <el-option
          v-for="(item, index) in courses"
          :key="item.id"
          :label="item.name"
          :value="index">
        </el-option>
      </el-select>
      <el-table
        ref="singleTable"
        :data="courseItems"
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
              @click="handleCourseworkSave(scope.row)"></el-button>
          </template>
          <template slot-scope="scope">
            <el-button
              title="删除文件"
              type="danger"
              size="mini"
              plain
              icon="el-icon-delete"
              @click="handleCourseworkRemove(scope.row)"></el-button>
            <el-dropdown trigger="hover">
              <el-button
                size="mini"
                type="primary"
                plain
                class="el-icon-more">
            </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item
                  @click="handleCourseworkBuild(scope.$index, scope.row)">编译和运行
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
    name: 'CourseManage',
    props: {
        courseId: Number,
    },
    computed: {
        currentCourse: function () {
            return (this.courses && this.courseIndex !== -1 && this.courseIndex < this.courses.length) ? this.courses[this.courseIndex] : null;
        },
        currentCoursework: function () {
            return (this.courseItems && this.itemIndex !== -1 && this.itemIndex < this.courseItems.length) ? this.courseItems[this.itemIndex] : null;
        },
    },
    data() {
        return {
            courseIndex: -1,
            itemIndex: -1,
            courses: [],
            courseItems: [],
        }
    },
    mounted() {
        connector.$on('api-login', this.onLogin)
        connector.$on('api-logout', this.onLogout)
    },
    methods: {
        queryCourses() {
            connector.$once('api-list-courses', this.onListCourses)
            connector.listCourses()
        },
        queryCourseItems(course) {
            connector.$once('api-list-course-items', this.onListCourseItems)
            connector.listCourseItems(course)
        },
        clearData() {
            this.courseIndex = -1
            this.itemIndex = -1
            this.courses = []
            this.courseItems = []
        },
        refreshData() {
            this.clearData()
            this.queryCourses()
        },

        onLogin: function (success) {
            if (success) this.refreshData()
        },
        onLogout: function (success) {
            if (success) this.clearData()
        },
        onListCourses: function (success, data) {
            if (success) this.courses = data
        },
        onListCourseItems: function (success, data) {
            if (success) this.courseItems = data
        },
        onCourseCreated: function (success, data) {
            if (!success)
                return
            
            this.courses.append(data)
            this.courseIndex = this.courses.length - 1
        },
        onRemoveCourse: function (success) {
            if (!success)
                return
            
            let course = this.currentCourse
            if (!course)
                return
        },
        
        handleCourseAdd: function () {
            this.$prompt('请输入课程名称', '创建课程', {
                inputValue: 'hello-world.c',
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
                    connector.$once('api-remove-course', this.onRemoveCourse)
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
            else
                this.courseItems = []
        },
        
        handleCourseworkAdd: function () {
        },
        handleCourseworkSave: function (coursework) {
            connector.$once('api-update-coursework', this.onUpdateCoursewrok)
            connector.updateCoursework(coursework)
        },
        handleCourseworkUpdate: function (coursework) {
            connector.$once('api-update-coursework', this.onUpdateCoursewrok)
            connector.updateCoursework(coursework)
        },
        handleCourseworkRemove: function (coursework) {
            connector.$once('api-remove-coursework', this.onRemoveCoursewrok)
            connector.removeCoursework(coursework)
        },
        handleCourseworkBuild: function (coursework) {
            connector.$once('api-build-coursework', this.onBuildCoursewrok)
            connector.buildCoursework(coursework)
        },
    }
}
</script>

<style>

/* Color themem */
.cb-course-manage .el-card,
.cb-course-manage .el-card .el-input__inner,
.cb-course-manage .el-card .el-table,
.cb-course-manage .el-card .el-table * {
    background-color: inherit;
    color: inherit;
}

.cb-course-manage .el-card .el-table .el-table__body tr.current-row.hover-row td,
.cb-course-manage .el-card .el-table .el-table__body tr:hover {
    background-color: #3f3f3f;
}

.cb-course-manage .el-card .el-table .el-table__body tr.current-row {
    background-color: #454545;
}

.cb-course-manage .el-card,
.cb-course-manage .el-card .el-input__inner {
    border: 1px solid #666;
}

.cb-course-manage .el-card .el-table td,
.cb-course-manage .el-card .el-table th.is-leaf {
    border-bottom: 1px solid #666;
}

.cb-course-manage .el-card .el-table .el-table__body tr > td:first-child {
    border-left: 1px solid #666;
}
.cb-course-manage .el-card .el-table .el-table__body tr > td:last-child {
    border-right: 1px solid #666;
}

.cb-course-manage .el-card .el-table::before,
.cb-course-manage .el-card .el-table .el-table__fixed-right::before {
    background-color: #666;
}

.cb-course-manage .el-card__body .el-table .el-button {
    border: 0;
}

/* Padding and margin */
.cb-course-manage .el-card__body {
    padding: 9px 16px;
}

.cb-course-manage .el-card__body > * {
    margin-bottom: 9px;
}

.cb-course-manage .el-card__body .el-table td {
    padding: 6px 0;
    cursor: pointer;
}

.cb-course-manage .el-card__body .el-button {
    padding: 2px 6px;
    margin-left: 6px;
}

.cb-course-manage .el-card__body .el-table .is-right > .cell {
    padding: 0 6px;
}

.w-100 {
    width: 100%;
}

</style>
