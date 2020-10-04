<template>
  <div class="cb-launcher">
    <el-button-group>
      <el-button
        type="primary"
        icon="el-icon-position"
        :title="$t( '发射' )"></el-button>
      <el-button
        type="primary"
        icon="el-icon-video-play"
        :title="$t( '继续' )"></el-button>
      <el-button
        type="primary"
        icon="el-icon-video-pause"
        :title="$t( '暂停' )"></el-button>
      <el-button
        type="primary"
        icon="el-icon-arrow-right"
        :title="$t( '下一步' )"></el-button>
      <el-button
        type="primary"
        icon="el-icon-arrow-left"
        :title="$t( '上一步' )"></el-button>
      <el-button
        type="primary"
        icon="el-icon-arrow-up"
        :title="$t( '上一层' )"></el-button>
      <el-button
        type="primary"
        icon="el-icon-arrow-down"
        :title="$t( '下一层' )"></el-button>
      <el-button
        type="primary"
        icon="el-icon-switch-button"
        :title="$t( '停止' )"></el-button>
    </el-button-group>
  </div>
</template>

<script>
import connector from '../connector.js'

export default {
    name: 'LaunchManager',
    props: {
        coursework: Object,
    },
    data() {
        return {
            lanucher: null
        }
    },
    mounted() {
        connector.$on( 'api-login', (success) => {
            this.isAuthenticated = success
            if (success)
                connector.getLogon()
        } )
    },
    methods: {
        runCodeWithArguments ( obj, args ) {
            return Function( '"use strict"; return (' + obj + ')' )()( args )
        },
        testCode () {
            const code = 'function ( arg ) { return "CodeBang Welcome You" + arg }'
            let result = this.runCodeWithArguments( code, "efg" )
            this.$message( 'Get result: ' + result )
        },

        handleCourseworkStart: function ( ) {
            if ( this.coursework ) {
                connector.$once( 'api-task', ( success, data ) => {
                    if ( success ) {
                        this.runCodeWithArguments ( data )
                    }
                    else
                        this.$message( data )
                } )
                connector.taskCoursework( this.coursework )
            }
        }
    }
}
</script>

<style>
.cb-launcher {
}
</style>
