<template>
  <div class="cb-editor cb-container">
    <!-- <div class="cb-toolbox"> -->
    <!--   <el-button type="info" size="mini" @click="handleUploadFile">上传 -->
    <!--     <input type="file" accept=".c,.h" style="display:none" @change="onFileSelected"> -->
    <!--   </el-button> -->
    <!--   <el-button type="info" size="mini" @click="handleDownloadFile">下载</el-button> -->
    <!-- </div> -->
  </div>
</template>

<script>
import ace from 'ace-builds'
import 'ace-builds/webpack-resolver'

import connector from '../connector.js'

export default {
    name: 'BufferManager',
    data() {
        return {
            editor: null,
            bufferIndex: undefined,
            buffers: [],
            mode: 'ace/mode/c_cpp',
            theme: 'ace/theme/twilight',
            fontSize: 18,
            tabSize: 4,
            wrapMode: true,
        }
    },
    mounted() {
        if (!this.$el.style.height)
            this.resizeEditor()

        this.editor = ace.edit(this.$el, {
            mode: this.mode,
            theme: this.theme,
            fontSize: this.fontSize,
            autoScrollEditorIntoView: true,
            displayIndentGuides: false
        });
        // editor.renderer.setScrollMargin(10, 10, 10, 10);
        this.editor.getSession().setUseWrapMode(this.wrapMode);
        this.editor.getSession().setTabSize(this.tabSize);
        this.editor.focus();
    },
    methods: {
        resizeEditor() {
            var navbar = document.querySelector('.cb-navbar')
            var rect = navbar.getBoundingClientRect()
            this.$el.style.height = (window.innerHeight - rect.bottom - 4) + 'px'
        },
        saveBuffer() {
            connector.updateCoursework()
        },
        selectBuffer(index) {
            if (this.bufferIndex !== index) {
                this.bufferIndex = index
                this.editor.setSession( this.buffers[index].buffer )
            }
        },

        onBufferSelected: function (coursework) {
            let index;
            for (index = 0; index < this.buffers.length; index ++)
                if (this.buffers[index].coursework.id === coursework.id) {
                    this.selectBuffer(index)
                    return
                }

            connector.$once('api-get-coursework-content', ( success, data ) => {
                if ( success ) {
                    let buf = new ace.EditSession( data )
                    this.buffers.push( {
                        coursework: coursework,
                        buffer: buf
                    } )
                    this.selectBuffer( this.buffers.length - 1 )
                }
            } )
            connector.getCourseworkContent(coursework)
        },

        onLocalFileSelected: function () {
            var file = this.$el.querySelector('input[type="file"]').files[0]
            var reader = new FileReader()
            reader.onload = (evt) => {
                this.editor.setValue(evt.target.result)
                this.editor.selection.clearSelection()
                this.editor.gotoLine(1)
                this.editor.focus()
            }
            reader.readAsText(file)
        },
        handleUploadFile: function () {
            this.$el.querySelector('input[type="file"]').click()
        },
        handleDownloadFile: function () {
            var text = this.editor.getValue()
            if (text.length > 0) {
                var blob = new Blob([text], {type: 'text/plain'})
                var reader = new FileReader()
                reader.onload = (evt) => {
                    var a = document.createElement('a')
                    a.href = evt.target.result
                    a.setAttribute('download', this.filename)
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
</style>
