<template>
  <div id="app">
    <el-container>
      <el-header class="cb-titlebar">
        <div class="cb-brand">
          <img src="./assets/logo.png">
          <span>CodeBang</span>
        </div>
        <div class="cb-searchbox" style="display: none;">
          <el-input
            placeholder="请输入搜素内容"
            prefix-icon="el-icon-search"
            size="mini"
            clearable>
          </el-input>
        </div>
        <el-button
          @click="activePage=0"
          type="text">代码</el-button>
        <el-button
          @click="activePage=1"
          type="text">编译</el-button>
        <el-button
          @click="activePage=2"
          type="text">运行</el-button>
        <div class="cb-title">
          {{ displayTitle }}
          <el-button
            title="修改文件名称"
            v-show="displayTitle"
            icon="el-icon-edit"
            size="small"
            type="text"></el-button>
        </div>
        <div class="cb-toolbox">
          <el-button
            icon="el-icon-bell"
            type="text"></el-button>
          <el-dropdown trigger="click" @command="handleUserMenu">
            <el-button size="" type="text" class="el-icon-user">
              <i class="el-icon-caret-bottom"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <template v-if="isAuthenticated">
                <span>登陆为 {{ userName }}</span>
                <el-dropdown-item command="logout" divided>注销</el-dropdown-item>
              </template>
              <template v-else>
                <el-dropdown-item command="login">登陆</el-dropdown-item>
              </template>
              <el-dropdown-item command="profile" divided>偏好设置</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>
      <!-- <div class="cb-toolbar"> -->
      <!--   <el-row> -->
      <!--     <el-button type="info" size="mini" @click="handleNewFile">新建</el-button> -->
      <!--     <el-button type="info" size="mini" @click="handleOpenFile">打开 -->
      <!--       <input type="file" accept=".c,.cpp,.h,.hpp" style="display:none" -->
      <!--              @change="handleFiles"> -->
      <!--     </el-button> -->
      <!--     <el-button type="info" size="mini" @click="handleSaveFile">保存</el-button> -->
      <!--     <el-button type="info" size="mini" @click="handleBuildFile">编译</el-button> -->
      <!--     <el-button type="info" size="mini" @click="handleRunFile">运行</el-button> -->
      <!--   </el-row> -->
      <!-- </div> -->
      <div class="cb-main">
        <el-container class="cb-container" v-show="!activePage">
          <el-aside style="padding: 2px">
            <cb-code-manager></cb-code-manager>
          </el-aside>
          <el-main style="padding: 0 2px 2px 2px;">
            <div id="editor" class="cb-editor"></div>
          </el-main>
        </el-container>
        <div class="cb-container" v-show="activePage==1">
          <!-- <cb-builder></cb-builder> -->
        </div>
        <div class="cb-container" v-show="activePage==2">
          <!-- <cb-runner></cb-runner> -->
        </div>
      </div>
    </el-container>
  </div>
</template>

<script>
import ace from 'ace-builds'
import 'ace-builds/webpack-resolver'

import connector from './connector.js'

export default {
    name: 'app',
    computed: {
        displayTitle: function () {
            return this.activeBuffer ? this.activeBuffer.filename : ''
        }
    },
    data() {
        return {
            userName: '',
            isAuthenticated: false,
            buffers: [],
            activeBuffer: null,
            activePage: 0,
            editor: null
        }
    },
    mounted() {
        connector.$on('api-login', this.onLogin)
        connector.$on('api-logout', this.onLogout)

        var main = this.$el.querySelector('.cb-main');
        var rect = main.previousElementSibling.getBoundingClientRect();
        main.style.height = (window.innerHeight - rect.bottom) + 'px';

        this.editor = ace.edit("editor", {
            mode: "ace/mode/c_cpp",
            theme: "ace/theme/twilight",
            // maxLines: 30,
            // minLines: 10,
            // readOnly: true,
            fontSize: 18,
            autoScrollEditorIntoView: true,
            displayIndentGuides: false
        });
        // editor.renderer.setScrollMargin(10, 10, 10, 10);
        this.editor.getSession().setUseWrapMode(true);
        this.editor.getSession().setTabSize(8);
        this.editor.focus();
    },
    methods: {
        onLogin: function (success) {
            this.isAuthenticated = success
        },
        onLogout: function (success) {
            if (success)
                this.isAuthenticated = false
        },

        handleUserMenu: function (command) {
            if (command == 'login')
                connector.login('admin', 'admin')
            else if (command == 'logout')
                connector.logout()
        },
        
        handleNewFile: function () {
            this.editor.setValue(
                '#include <stdio.h>\n\nint main(int argc, char *argv[])\n' +
                    '{\n    printf("Hello World\\n");\n    return 0;\n}')
            this.editor.selection.clearSelection()
            this.editor.gotoLine(1);
            this.editor.focus()
        },
        handleOpenFile: function () {
            this.$el.querySelector('input[type="file"]').click()
        },
        handleFiles: function () {
            var file = this.$el.querySelector('input[type="file"]').files[0];
            this.title = file.name;
            // this.title = file.webkitRelativePath;
            var reader = new FileReader();
            reader.onload = function (evt) {
                this.editor.setValue(evt.target.result);
                this.editor.selection.clearSelection();
                this.editor.gotoLine(1);
                this.editor.focus();
            }.bind(this);
            reader.readAsText(file);
        },
        handleSaveFile: function () {
            var text = this.editor.getValue();
            if (text.length > 0) {
                var blob = new Blob([text], {type: 'text/plain'});
                var reader = new FileReader();
                reader.onload = function (evt) {
                    var a = document.createElement('a');
                    a.href = evt.target.result;
                    a.setAttribute('download', this.filename);
                    a.click();
                }.bind(this);
                reader.readAsDataURL(blob);
                // var url = URL.createObjectURL(blob);
                // URL.revokeObjectURL(url);
            }
        },
    }
}
</script>

<style>
html {
    height: 100%;
    width: 100%;
    overflow: hidden;
}
body {
    overflow: hidden;
    margin: 0;
    padding: 0;
    height: 100%;
    width: 100%;
    color: #f8f8f8;
    background-color: #333;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.cb-titlebar {
    display: flex;
    flex-direction: col;
    align-items: center;
}

.cb-titlebar > * {
    padding-right: 16px;
}

.cb-titlebar > *:last-child {
    margin-left: auto;
    padding-right: 0;
}

.cb-titlebar input {
    background-color: #555;
    border: 0;
    color: #eee;
}

.cb-titlebar .el-button--text {
    color: #f8f8f8;
}

.cb-titlebar .el-button--text:hover {
    color: #ccc;
}

.cb-toolbox > * {
    padding-left: 9px;
}

.cb-title {
    background-color: #3f3f3f;
    flex-grow: 1;
    text-align: center;
    margin-left: 16px;
    margin-right: 16px;
}

.cb-brand {
    display: inline-table;
}
.cb-brand img {
    display: table-cell;
    vertical-align: middle;
    width: 32px;
    height: 32px;
    padding: 12px 6px 12px 0;
}
.cb-brand span {
    display: table-cell;
    vertical-align: middle;
}

.cb-editor {
    width: 100%;
    height: 100%;
}

.cb-container {
    width: 100%;
    height: 100%;
}
</style>
