<template>
  <div class="cb-launcher">
    <el-button-group>
      <el-button
        type="primary"
        icon="el-icon-video-play"
        :title="$t( '开始' )"></el-button>
      <el-button
        type="primary"
        icon="el-icon-video-pause"
        :title="$t( '暂停' )"></el-button>
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
            if ( coursework ) {
                connector.$once( 'api-task', ( success, data ) => {
                    if ( success ) {
                        this.runCodeWithArguments ( data )
                    }
                    else
                        this.$message( data )
                } )
                connector.taskCoursework( coursework )
            }
        }
    }
}
</script>

<style>
.cb-launcher {
}
</style>
