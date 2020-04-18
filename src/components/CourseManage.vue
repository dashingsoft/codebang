<template>
  <div class="cb-course-manage cb-container">
    <el-card class="cb-container">
      <div>课程管理</div>
      <!--   <el-button type="text" icon="el-icon-folder-add"></el-button> -->
      <!--   <el-button type="text" icon="el-icon-document-add"></el-button> -->
      <!--    -->
      <el-select v-model="course"
                 class="w-100"
                 filterable
                 clearable
                 placeholder="请选择课程">
        <el-button slot="prefix"
                   title="删除当前课程以及所有相关文件"
                   v-show="course"
                   type="text"
                   icon="el-icon-delete"></el-button>
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
      <el-table
        ref="singleTable"
        :data="tableData"
        highlight-current-row
        @current-change="handleCurrentChange">
        <el-table-column
          property="filename"
          sortable
          label="课程文件">
        </el-table-column>
        <el-table-column
          fixed="right"
          align="right"
          width="80">
          <template slot="header">
            <el-button title="保存全部修改过的内容"
                       type="primary"
                       plain
                       size="mini"
                       icon="el-icon-document-copy"></el-button>
            <el-button title="新增文件"
                       type="primary"
                       plain
                       size="mini"
                       icon="el-icon-plus"></el-button>
          </template>
          <template slot-scope="scope">
            <el-button title="编译和运行"
                       type="primary"
                       plain
                       size="mini"
                       icon="el-icon-position"
                       @click="handleEdit(scope.$index, scope.row)"></el-button>
            <el-button type="danger" size="mini" icon="el-icon-delete" plain></el-button>
          </template>
        </el-table-column>
      </el-table>

    </el-card>
  </div>
</template>

<script>

export default {
  name: 'CourseManage',
  props: {
msg: String,
course: String,
},
data() {
      return {
        options: [{
          value: '选项1',
          label: '黄金糕'
        }, {
          value: '选项2',
          label: '双皮奶'
}],

tableData: [{
          filename: 'foo.c',
        }, { filename: 'this is a very long.c' } ],
} },
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

.cb-course-manage .el-card__body .el-table .el-button {
    padding: 2px 6px;
}

.cb-course-manage .el-card__body .el-table .is-right > .cell {
    padding: 0 6px;
}

.w-100 {
    width: 100%;
}

</style>
