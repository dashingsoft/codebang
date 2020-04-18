import Vue from 'vue'
import App from './App.vue'
import CourseManage from './components/CourseManage.vue'

import './plugins/element.js'

Vue.config.productionTip = false
Vue.component('cb-course-manage', CourseManage)

new Vue({
  render: h => h(App),
}).$mount('#app')
