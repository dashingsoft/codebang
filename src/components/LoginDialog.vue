<template>
  <div class="cb-user">
      <el-dialog
        width="25%"
        :visible="dialogVisible"
        :close-on-click-modal="false"
        :before-close="handleDialogClose">
        <el-form
          :model="ruleForm"
          status-icon
          :rules="rules"
          ref="ruleForm"
          label-width="auto"
          class="ruleForm">
          <el-form-item label="账户" prop="name">
            <el-input v-model="ruleForm.name" autocomplete="off" placeholder="用户名/邮箱/手机号"></el-input>
          </el-form-item>
          <el-form-item v-if="!isRetrivePass" label="密码" prop="pass">
            <el-input type="password" v-model="ruleForm.pass" autocomplete="off" show-password></el-input>
          </el-form-item>
          <el-form-item v-if="isRegister" label="确认密码" prop="checkPass">
            <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off" show-password></el-input>
          </el-form-item>
          <el-form-item style="text-align: center;">
            <el-button
              v-if="isLogin"
              style="width: 100%;"
              type="primary"
              @click="onLogin('ruleForm')">登陆</el-button>
            <el-button
              v-if="isRegister"
              style="width: 100%;"
              type="primary"
              @click="onRegister('ruleForm')">注册</el-button>
            <el-button
              v-if="isRetrivePass"
              style="width: 100%;"
              type="primary"
              @click="onRetrivePass('ruleForm')">找回密码</el-button>
          </el-form-item>
          <el-form-item style="text-align: right;">
            <el-link :underline="false" v-if="!isRetrivePass" type="primary"
                     style="margin-right: 16px"
                     @click="onRetrivePass('ruleForm')">忘记密码</el-link>
            <el-link :underline="false"
                     v-if="isLogin || isRetrivePass"
                     type="primary"
                     @click="onRegister('ruleForm')">注册</el-link>
            <el-link :underline="false" v-if="isRegister || isRetrivePass" type="primary" @click="onLogin('ruleForm')">登陆</el-link>
          </el-form-item>
        </el-form>
      </el-dialog>
    </div>
</template>

<script>

import connector from '../connector.js'

export default {

    name: "LoginDialog",

    props: {
        isVisible: {
            type: Boolean,
            default: false
        },

        loginMode: {
            type: String,
            default: "login"
        },

        onClose: {
            type: Function,
            default: () => {}
        }
    },

    watch: {
        isVisible: function(newVal, oldVal) {
            if (newVal != oldVal && newVal) {
                this.dialogVisible = true
            }
        },

        loginMode: function(newVal, oldVal) {
            if (newVal !== oldVal) {
                if (newVal === "login") {
                    this.isRegister = false
                }
                else if (newVal === "register") {
                    this.isRegister = true
                }
            }
        }
    },

    data() {

        var validatePass = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入密码'));
            } else {
                if (this.ruleForm.checkPass !== '') {
                    this.$refs.ruleForm.validateField('checkPass');
                }
                callback();
            }
        };
        var validatePass2 = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请再次输入密码'));
            } else if (value !== this.ruleForm.pass) {
               callback(new Error('两次输入密码不一致!'));
            } else {
               callback();
            }
        };
        var validateName = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入用户名'));
            } else {
                callback();
            }
        };

        return {
            ruleForm: {
                name: '',
                pass: '',
                checkPass: '',
            },
            rules: {
                name: [
                    { validator: validateName, trigger: 'blur'}
                ],
                pass: [
                    { validator: validatePass, trigger: 'blur' }
                ],
                checkPass: [
                    { validator: validatePass2, trigger: 'blur' }
                ],
            },
            dialogVisible: false,
            isLogin: true,
            isRegister: false,
            isRetrivePass: false,
        }
    },
    mounted() {
        connector.$on( 'api-login', (success) => {
            console.log("login result: " + success);
            if (success) {
              this.dialogVisible = false;
              connector.showSuccess('登陆成功');
            }
        } );
    },
    methods: {
        onLogin(formName) {
            if (this.isLogin) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        let name = this.ruleForm.name;
                        let pass = this.ruleForm.pass;
                        connector.login(name, pass);
                        return true;
                    }
                    return false;
                });
            }
            else {
                this.isLogin = true;
                this.isRegister = false;
                this.isRetrivePass = false;
            }
        },

        onRegister(formName) {
            if(this.isRegister) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        connector.showError("现在还不能注册");
                        return true;
                    }
                    return false;
                });
            } else {
                this.isLogin = false;
                this.isRetrivePass = false;
                this.isRegister = true;
            }
        },

        onRetrivePass(formName) {
            if(this.isRetrivePass) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        connector.showError("现在还不能找回密码");
                        return true;
                    }
                    return false;
                });
            } else {
                this.isRetrivePass = true;
                this.isLogin = false;
                this.isRegister = false;
            }
        },

        handleDialogClose() {
            console.log("visible: " + this.dialogVisible);
            this.dialogVisible = false;
            this.onClose();
        },
    }
}
</script>

<style>
</style>
