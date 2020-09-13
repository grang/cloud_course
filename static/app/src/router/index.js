import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store/index'



import login  from '@/views/login/login'
import main  from '@/views/main/main'

Vue.use(VueRouter)
const router = new VueRouter({
	mode: 'hash', 
	base: '/',
    routes: [
	   // {path: '/', name: 'index', component: Index},
	   
	   {path: '/login', name: 'login', component: login, meta:{} },
	   {path: '/main', name: 'main', component: main, meta:{}
		   
	   },
	]
})

import http from '@/fetch/http.js'

router.beforeEach((to, from, next) => {
	var params = {
	    	path: to.path
    };
	
	var full_path = to.fullPath;
	
    if (to.meta.requireAuth) {  
	    if (store.state.token) { 
	        next();
	    } else {
            next({
              path: '/login',
              query: { redirect: to.fullPath }  
            })
	    }
    }else {
    	let temp = ['login']
    	if(temp.some(x=>x==to.name) && store.state.token){
    		next({
                path: '/my',
                query: { redirect: '/' }
              })
    	}
        next();
    }
})

export default router