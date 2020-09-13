import Vue from 'vue'
import axios from 'axios'
import qs from 'qs';

import store from '@/store/index.js'
import * as types from '@/store/mutation-types'
import router from '@/router'

// axios 配置
axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded';

//'X-CSRFToken':mos.getToken()

axios.defaults.timeout = 5000;
axios.defaults.baseURL = '';

// http request 拦截器
axios.interceptors.request.use(
    config => {
        let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
	  	config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
        return config;
    },
    err => {
        return Promise.reject(err);
    });

// http response 拦截器
axios.interceptors.response.use(
    response => {
    	if(response.data.response=='NoLogin'){
    		store.commit(types.LOGOUT);
    		
    		if(router.currentRoute.path!='/login'){
    			router.replace({
                    path: '/login',
                    query: {}
                })
        		return
    		}
    		
    		
    	}
        return response;
    },
    error => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    // 401 清除token信息并跳转到登录页面
                	store.commit(types.LOGOUT);
    				router.replace({
    	                path: '/login',
    	                query: {redirect: router.currentRoute.fullPath}
    	            })
            }
        }
        return Promise.reject(error.response.data)
    });

//export default axios;


//封装axios的post请求
export function get(url, params) {
	return new Promise((resolve, reject) => {
	    axios.get(url, {params: params}).then(response => {
	    	if(response){
	    		resolve(response.data);
	    	}
		}).catch((error) => {
			reject(error);
		})
	})
}

//封装axios的post请求
export function post(url, params) {
	return new Promise((resolve, reject) => {
		if(!params){
			params = {};
		}

		//params = $.param(params)
		params = qs.stringify(params)
		axios.post(url, params).then(response => {
			resolve(response.data);
		}).catch((error) => {
			reject(error);
		})
	})
}

//封装axios的post请求
export function postJson(url, params) {
	var headers = {"Content-Type": "application/json"}
	
	return new Promise((resolve, reject) => {
		if(!params){
			params = {};
		}
		
		axios.post(url, params, {headers: headers}).then(response => {
			resolve(response.data);
		}).catch((error) => {
			reject(error);
		})
	})
}

export function postUpload(url, params) {
	var headers = {'Content-Type':'multipart/form-data'}
	
	return new Promise((resolve, reject) => {
		if(!params){
			params = {};
		}
		
		axios.post(url, params, {headers: headers}).then(response => {
			resolve(response.data);
		}).catch((error) => {
			reject(error);
		})
	})
}


export default {
	get(url, params) {
		return get(url, params);
	},
	post(url, params) {
		return post(url, params);
	},
	postJson(url, params) {
		return postJson(url, params);
	},
	postUpload(url, params) {
		return postUpload(url, params);
	},
	axios
}

