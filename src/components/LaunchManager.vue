<template>
  <div class="cb-launcher">
    <yix-engineer ref="engineer">This is launcher for CodeBang</yix-engineer>
  </div>
</template>

<script>
import Vue from "vue"
import { RealComputer } from 'yix-engineer/src/lib.js'
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
        let engineer = this.$refs.engineer
        Vue.prototype.$i_engineer = engineer

        const RealComputerObject = Vue.extend( RealComputer )
        let computer = new RealComputerObject()
        engineer.initMainDomain( computer )
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
    background: #fff;
    height: 100%;
}
</style>
