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
            scratch: null,
            buffer: null,
            bufferList: [],
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
        // this.editor.renderer.setScrollMargin(10, 10, 10, 10);
        this.scratch = this.editor.getSession()
        this.scratch.setUseWrapMode(this.wrapMode)
        this.scratch.setTabSize(this.tabSize)
        this.editor.focus()
    },
    computed: {
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
        getBuffer( coursework ) {
            let i = this.getIndex( coursework )
            return i === undefined ? null : this.bufferList[i]
        },
        getIndex( coursework ) {
            if ( coursework && coursework.id )
                for ( let index = 0; index < this.bufferList.length; index ++ )
                    if ( this.bufferList[index].coursework.id === coursework.id )
                        return index
            return undefined
        },
        selectBuffer(buffer) {
            if ( ! buffer ) {
                this.buffer = null
                this.editor.setSession( this.scratch )
            }
            else {
                this.buffer = buffer
                this.editor.setSession( buffer.session )
            }
        },

        // onXXX for coursework
        onSelectCoursework: function (coursework) {
            if ( ! coursework ) {
                this.selectBuffer( null )
            }
            else {
                let buf = this.getBuffer( coursework )
                if ( buf ) {
                    if ( buf.coursework !== coursework ) {
                        coursework.dirty = buf.session.$modified
                        buf.coursework = coursework
                    }
                    this.selectBuffer( buf )
                }
                else {
                    connector.$once('api-get-coursework-content', ( success, data ) => {
                        if ( success ) {
                            let session = new ace.EditSession( data )
                            let buf =  {
                                coursework: coursework,
                                session: session
                            }
                            session.setMode( this.mode )
                            session.on( 'change', () => {
                                buf.coursework.dirty = session.$modified
                            } )
                            this.bufferList.push( buf )
                            this.selectBuffer( buf )
                        }
                    } )
                    connector.getCourseworkContent( coursework )
                }
            }
        },
        onCloseCoursework: function ( coursework ) {
            if ( coursework === undefined ) {
                this.editor.setSession( this.scratch )
                this.bufferList.forEach( buf => delete buf.session )
                this.bufferList = []
            }
            else {
                let buf = this.getBuffer( coursework )
                if ( buf ) {
                    if ( buf === this.buffer ) {
                        this.editor.setSession( this.scratch )
                        this.buffer = null
                    }
                    delete buf.session
                    this.bufferList.pop( this.getIndex( coursework ) )
                }
            }
        },
        onSaveCoursework: function ( coursework ) {
            let buffers = coursework ? this.bufferList : [ this.getBuffer( coursework ) ]
            buffers.forEach( buf => {
                if ( buf && buf.dirty ) {
                    connector.$once('api-update-coursework-content', function ( success ) {
                        if ( success )
                            buf.coursework.dirty = false
                    } )
                    connector.updateCourseworkContent( buf.coursework, buf.session.getValue() )
                }
            } )
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
