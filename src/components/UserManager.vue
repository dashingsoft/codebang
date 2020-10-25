<template>
  <div class="cb-user">
      <el-dialog
        title="请输入"
        :visible="dialogVisible"
        width="30%"
        :close-on-click-modal="false"
        :before-close="handleDialogClose">
        <el-form 
          :model="ruleForm"
          status-icon
          :rules="rules"
          ref="ruleForm"
          label-width="130px"
          class="demo-ruleForm">
          <el-form-item label="账户" prop="name">
            <el-input v-model="ruleForm.name" autocomplete="off" placeholder="用户名/邮箱/手机号"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="pass">
            <el-input type="password" v-model="ruleForm.pass" autocomplete="off" show-password></el-input>
          </el-form-item>
          <el-form-item v-if="isRegister" label="确认密码" prop="checkPass">
            <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off" show-password></el-input>
          </el-form-item>
          <el-form-item>
            <el-button v-if="isRegister" 
              type="primary" 
              @click="submitForm('ruleForm')"
              :disabled="enableLoginBtn">注册</el-button>
            <el-button v-else 
              type="primary" 
              @click="submitForm('ruleForm')"
              :disabled="enableLoginBtn">登录</el-button>
            <el-button @click="resetForm('ruleForm')">清空</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
    </div>
</template>

<script>

import connector from '../connector.js'

export default {

    name: "UserManger",

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
            console.log("new: " + newVal + "    " + "old: " + oldVal);
            if (newVal != oldVal && newVal) {
                this.dialogVisible = true
            }
        },

        loginMode: function(newVal, oldVal) {
            console.log("new: " + newVal + "    " + "old: " + oldVal);
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
            isRegister: false,
            enableLoginBtn: false
        }
    },
    mounted() {
        connector.$on( 'api-login', (success) => {
            console.log("login result: " + success);
            if (success) {
              this.dialogVisible = false;
              connector.showSuccess('登录成功');
            }
        } );
    },
    methods: {
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    let name = this.ruleForm.name
                    let pass = this.ruleForm.pass
                    connector.login(name, pass)
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
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
