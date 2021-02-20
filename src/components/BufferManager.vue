<template>
    <div class="cb-editor cb-container"></div>
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
        this.$el.style.height = "100%"
        this.editor = ace.edit( this.$el, {
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
    methods: {
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

        handleCourseworkSelect: function (coursework) {
            if ( ! coursework ) {
                this.selectBuffer( null )
            }
            else {
                let buf = this.getBuffer( coursework )
                if ( buf ) {
                    if ( buf.coursework !== coursework ) {
                        buf.coursework = coursework
                    }
                    this.selectBuffer( buf )
                }
                else {
                    connector.$once('api-get-coursework-content', ( success, data ) => {
                        if ( success ) {
                            let session = new ace.EditSession( data )
                            session.setUndoManager( new ace.UndoManager() )
                            let buf =  {
                                coursework: coursework,
                                session: session
                            }
                            session.setMode( this.mode )
                            session.setUseWrapMode(this.wrapMode)
                            session.on( 'change', () => {
                                buf.coursework.state = -1
                            } )
                            this.bufferList.push( buf )
                            this.selectBuffer( buf )
                        }
                    } )
                    connector.getCourseworkContent( coursework )
                }
            }
        },
        handleCourseworkClose: function ( coursework ) {
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
        handleCourseworkSave: function ( coursework ) {
            let buffers = coursework ? this.bufferList : [ this.getBuffer( coursework ) ]
            buffers.forEach( buf => {
                if ( buf && ( buf.coursework.state === -1 ) ) {
                    connector.$once('api-update-coursework-content', function ( success, data ) {
                        if ( success ) {
                            if ( buf.coursework.name !== data.name )
                                data.name = buf.coursework.name
                            buf.coursework.state = 0
                        }
                    } )
                    // if ( ! buf.session.getUndoManager().canUndo() )
                    //     buf.coursework.state = 0;
                    // else
                    connector.updateCourseworkContent( buf.coursework, buf.session.getValue() )
                }
            } )
        },
        handleCourseworkChangeSetting: function ( coursework, options ) {
            let buf = this.getBuffer( coursework )
            if ( buf && options ) {
                if ( Object.prototype.hasOwnProperty.call( options, 'wrapMode' ) )
                    buf.session.setUseWrapMode( ! this.wrapMode )
                else if ( Object.prototype.hasOwnProperty.call( options, 'tabSize' ) )
                    buf.session.setTabSize( options.tabSize )
            }
        },
    }
}
</script>

<style>
</style>
