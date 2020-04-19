import Vue from 'vue'
import App from './App.vue'
import CodeManager from './components/CodeManager.vue'

import './plugins/element.js'

Vue.config.productionTip = false
Vue.component('cb-code-manager', CodeManager)

new Vue({
  render: h => h(App),
}).$mount('#app')
