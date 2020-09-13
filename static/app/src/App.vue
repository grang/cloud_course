<template>
	<router-view>
		<div class="load-box">
			<img src='@/assets/images/alert-loading.gif'>
		</div>
	</router-view>

</template>

<style>
.load-box{
	position: absolute;
	left: 0;
	right: 0;
	bottom: 0;
	top: 0;
	display: flex;
	align-items: center;
	justify-content: center;
}

.load-box img{
	width: 30px;
}

</style>

<script>
import http from '@/fetch/http.js'
import * as types from '@/store/mutation-types.js'
import router from '@/router'


export default {
    name: 'app',
		data () {
			return {
			}
		},
		created : function() {
			this.init()
		},
		methods : {
			init(){
        		var self = this;
        		var url = "/common/curuser/";
    			http.get(url).then(res => {
    				if(res.response=='expired'){
    					self.$store.commit(types.LOGOUT);
    	            	window.location.href = '/logout/';
    				}else if(res.user && res.user.id){
    					self.$store.commit(types.LOGIN, {'user': res.user});
    					router.push({
    		                'name': 'main'
    		            })
    				}
    			});
        	}
		},
		components : {
		}
	}
</script>
