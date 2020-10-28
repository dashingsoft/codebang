<template>
    <transition name="cb-lanch-cover">
      <div v-if="visible"
        v-bind:style="coverStyle">
        <div class="controler-area">
          <el-button id="start-button" @click="onStart">开始</el-button>
          <el-switch
            v-model="isFullscreen"
            active-text="全屏">
          </el-switch>
          <el-slider v-model="speed" :format-tooltip="formatSpeed"></el-slider>
        </div>
      </div>
    </transition>
</template>

<script>
export default {
    data() {
        return{
            speed: 1,
            isFullscreen: true,
            visible: true,
            coverStyle: {
                height: "100%",
                width: "100%",
                overflow: "hidden !important",
                background: "url('https://photo.16pic.com/00/49/77/16pic_4977980_b.jpg')",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                zIndex: "100",
                position: "fixed",
                left: 0,
                top: 0,
            }
        }
    },
    
    methods: {
        formatSpeed(val) {
            return 'X' + (1 + val / 50).toFixed(2);
        },

        onStart() {
            this.visible = false;
        }
    }
}
</script>

<style>
#start-button {
    width: 210px;
    display: block;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 50px;
}

.constroler-area {
    width: fit-content;
    height: fit-content;
}

.el-switch {
    height: fit-content;
    margin-right: 15px;
}

.el-slider {
    display: inline-block;
    vertical-align: middle;
    margin-left: 15px;
    width: 100px;
}

.cb-lanch-cover-enter-active, .cb-lanch-cover-leave-active {
  transition: opacity .5s;
}
.cb-lanch-cover-enter, .cb-lanch-cover-leave-to {
  opacity: 0;
}
</style>
