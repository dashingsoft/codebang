<template>
  <div class="cb-launcher">
    This is CodeBang Lanucher.
    <el-button
      @click="testCode"> Test</el-button>
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
            editor: null
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
            const code = 'function ( arg ) { return "abc" + arg }'
            let result = this.runCodeWithArguments( code, "efg" )
            this.$message( 'Get result: ' + result )
        },
    }
}
</script>

<style>
.cb-launcher {
}
</style>
