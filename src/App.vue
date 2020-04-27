<template>
  <div id="app">
    <div class="cb-navbar cb-header">
      <div class="cb-brand">
        <img src="./assets/logo.png">
        <span>{{ $t( '代码帮' ) }} </span>
      </div>
      <div class="cb-searchbox" style="display: none;">
        <el-input
          :placeholder="$t( '请输入搜索内容' )"
          prefix-icon="el-icon-search"
          size="mini"
          clearable>
        </el-input>
      </div>
      <el-button
        @click="pageIndex=0"
        type="text">{{ $t( '代码' ) }}</el-button>
      <el-button
        @click="pageIndex=1"
        type="text">{{ $t( '编译' ) }}</el-button>
      <el-button
        @click="pageIndex=2"
        type="text">{{ $t( '运行' ) }}</el-button>
      <div class="cb-title">
        {{ title }}
      </div>
      <div class="cb-toolbox">
        <el-button
          icon="el-icon-bell"
          type="text"></el-button>
        <el-dropdown
          trigger="click"
          size="small"
          @command="handleUserMenu">
          <el-button size="" type="text" class="el-icon-user">
            <i class="el-icon-caret-bottom"></i>
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <template v-if="isAuthenticated">
              <el-dropdown-item disabled>{{ $t( '登陆为 %1', logonName ) }}</el-dropdown-item>
              <el-dropdown-item command="logout" divided>{{ $t( '注销' ) }}</el-dropdown-item>
            </template>
            <template v-else>
              <el-dropdown-item command="login">{{ $t( '登陆' ) }}</el-dropdown-item>
            </template>
            <el-dropdown-item command="profile" divided>{{ $t( '设置' ) }}</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
    <div class="cb-main">
      <div class="cb-container" v-show="pageIndex==0">
        <cb-code-manager
          v-on:title-changed="resetTitle"
          v-on:changed="resetCoursework"
          ref="coder"></cb-code-manager>
      </div>
      <div class="cb-container" v-show="pageIndex==1">
        <cb-build-manager
          :coursework="coursework"
          ref="builder"></cb-build-manager>
      </div>
      <div class="cb-container" v-show="pageIndex==2">
        <cb-lanuch-manager
          :coursework="coursework"
          ref="launcher"></cb-lanuch-manager>
      </div>
    </div>
  </div>
</template>

<script>
import connector from './connector.js'
import { setLocale } from './plugins/gettext.js'

export default {
    name: 'app',
    data() {
        return {
            title: '',
            logonName: '',
            isAuthenticated: false,
            pageIndex: 0,
            coursework: undefined
        }
    },
    mounted() {
        connector.$on( 'api-login', (success) => {
            this.isAuthenticated = success
            if (success)
                connector.getLogon()
        } )
        connector.$on( 'api-logout', (success) => {
            this.isAuthenticated = !success
        } )
        connector.$on( 'api-get-logon', (success, data) => {
            if (success)
                this.logonName = data.username
        } )

        this.isAuthenticated = connector.isAuthenticated
        if (this.isAuthenticated)
            connector.getLogon()

        this.resizeEditor()
    },
    methods: {
        resetTitle( title ) {
            this.title = title
        },
        resetCoursework( coursework ) {
            this.coursework = coursework
        },
        resizeEditor() {
            // var navbar = document.querySelector('.cb-navbar')
            // var rect = navbar.getBoundingClientRect()
            this.$el.querySelector( '.cb-main' ).style.height = ( window.innerHeight - 60 ) + 'px'
        },
        resetLocale( lang ) {
            setLocale(lang)
            // Force update all the components
            let update = function (obj) {
                obj.$forceUpdate()
                obj.$children.forEach( child => update( child ) )
            }
            update( this )
            // localStorage.setItem( 'language', lang )
        },

        handleUserMenu: function (command) {
            if (command == 'login')
                connector.login('admin', 'admin')
            else if (command == 'logout')
                connector.logout()
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

.cb-header {
    height: 60px;
    padding: 0 16px;
}

.cb-navbar {
    display: flex;
    flex-direction: col;
    align-items: center;
}

.cb-navbar > * {
    padding-right: 16px;
}

.cb-navbar > *:last-child {
    margin-left: auto;
    padding-right: 0;
}

.cb-navbar input {
    background-color: #555;
    border: 0;
    color: #eee;
}

.cb-navbar .el-button--text {
    color: #f8f8f8;
}

.cb-navbar .el-button--text:hover {
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

/* Help class */
.cb-container {
    width: 100%;
    height: 100%;
}
.w-100 {
    width: 100%;
}
.h-100 {
    height: 100%;
}
</style>
