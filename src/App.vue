<template>
  <div id="app">
    <el-container>
      <el-header class="cb-brand">
          <img src="./assets/logo.png">
          <span>CodeBang</span>
          <div class="cb-title">{{ title }}</div>
      </el-header>
      <div class="cb-toolbar">
        <el-row>
          <el-button type="info" size="mini" @click="handleNewFile">新建</el-button>
    <el-button type="info" size="mini" @click="handleOpenFile">打开
          <input type="file" accept=".c,.cpp,.h,.hpp" style="display:none"
                 @change="handleFiles">

</el-button>
          <el-button type="info" size="mini" @click="handleSaveFile">保存</el-button>
          <el-button type="info" size="mini" @click="handleBuildFile">编译</el-button>
          <el-button type="info" size="mini" @click="handleRunFile">运行</el-button>
        </el-row>
      </div>
      <div class="cb-main">
        <div id="editor" class="cb-editor"></div>
        <div class="cb-pixie hidden"></div>
      </div>
    </el-container>
  </div>
</template>

<script>
import ace from 'ace-builds';
import 'ace-builds/webpack-resolver';

export default {
    name: 'app',
    data() {
        return {
            title: "新文件",
            editor: null,
            filename: '',
        }
    },
    mounted() {
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
        this.editor.focus();
    },
    components: {
    },
    methods: {
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
        },
        handleBuildFile: function () {
        },
        handleRunFile: function () {
        }
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

.cb-brand {
    display: inline-table;
}
.cb-brand img {
    display: table-cell;
    vertical-align: middle;
    width: 32px;
    height: 32px;
    padding: 12px 6px;
}
.cb-brand span {
    display: table-cell;
    vertical-align: middle;
}
.cb-title {
    display: table-cell;
    width: 100%;
    text-align: center;
    vertical-align: middle;
}
.cb-toolbar {
    padding: 0px 20px 9px 20px;
}
.cb-main {
}
.cb-editor {
    width: 100%;
    height: 100%;
}
.cb-pixie {
    width: 100%;
    height: 100%;
}
</style>
