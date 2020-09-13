import $ from 'jquery' 
import Vue from 'vue'
import axios from 'axios'


import Router from 'vue-router'
Vue.use(Router)
const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
	return originalPush.call(this, location).catch(err => err)
}

import i18n from './i18n/i18n'
import App from './App.vue'
import router from './router'
import store from './store/index.js'
import http from '@/fetch/http.js'

import "./assets/css/common.css"
import "./assets/css/web.css"


import ElementUI from 'element-ui';
//import 'element-ui/lib/theme-chalk/index.css';
import './assets/css/element_custom.css'
Vue.use(ElementUI, { size: 'medium', zIndex: 3000});


Vue.config.productionTip = false

new Vue({
	store,
	i18n,
	router,
	render: h => h(App),
	created:function(){
	}
}).$mount('#app')


