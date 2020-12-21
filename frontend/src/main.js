import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import 'normalize.css'
import App from './App.vue'
import router from './router'
import store from './store'
import VueProgressBar from 'vue-progressbar'
import service from '@/utils/request'

import '@/styles/index.scss' // global css


Vue.prototype.$axios = service

Vue.config.devtools = true;
Vue.config.productionTip = true
// Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.use(VueProgressBar, {
    color: 'rgb(143, 255, 199)',
    failedColor: 'red',
    height: '2px'
})

// Vue.prototype.$eventBus = new Vue()

var app = new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
})

export default app


