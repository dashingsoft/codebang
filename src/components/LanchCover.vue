<template>
    <div class="cb-lanch-cover">
        <el-dialog
         fullscreen
         center
         :show-close="false"
         :visible.sync="lancherCoverVisibility">
          <div class="center-ui">
            <el-button id="start-button" @click="onStart">开始</el-button>
            <el-switch
            v-model="isFullscreen"
            active-text="全屏">
            </el-switch>
            <el-slider v-model="speed" :format-tooltip="formatSpeed"></el-slider>
          </div>
        </el-dialog>
    </div>
</template>

<script>
export default {
    data() {
        return{
            lancherCoverVisibility: true,
            isFullscreen: true,
            speed: 1,
        }
    },
    
    methods: {
        formatSpeed(val) {
            return 'X' + (1 + val / 50).toFixed(2);
        },

        onStart() {
            this.lancherCoverVisibility = false;
        }
    }
}
</script>

<style>
#start-button {
    display: block;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 20px;
    width: 40%;
}

.center-ui {
    width: 50%;
    text-align: center;
}

.el-dialog {
    overflow: hidden !important;
    text-align: center;
}

.el-dialog__header, .el-dialog__body {
    background: url('https://photo.16pic.com/00/49/77/16pic_4977980_b.jpg');
    display: flex;
    justify-content: center;
    align-items: center;
}

.el-dialog__header {
    height: 0;
}

.el-dialog__body {
    height: 100%;
}

.el-switch {
    margin-right: 15px;
}

.el-slider {
    width: 10%;
    display: inline-block;
    vertical-align: middle;
    margin-left: 15px;
}
</style>
