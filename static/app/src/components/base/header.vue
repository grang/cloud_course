<template>
	<div class="app-header">
		<div class="header-logo">
	          <img class="logo" src="/static/images/chinese_icon.png"/>
        </div>
      
      <div class="nav-status hide" v-if="$store.state.user.id">;
     		<div class="username"> {{$store.state.user.username}} </div>
			<div class="expired-time">{{$t('message.expired_time')}}：{{$store.state.user.expire_date}}</div>
			<div class="logout"><el-button class="logout-btn" size="mini" @click="logout" plain>{{$t('message.logout')}}</el-button></div>
      </div>
      
      <div class="nav-status" v-if="$store.state.user && $store.state.user.id">
        	<div class="quanping" :title="$t('message.fullscreen')"><i class="iconfont icon-quanping" @click="clickFullscreen"></i></div>
        	<el-dropdown trigger="click" class="test">
		    	<span class="account-info">
		      		<i class="iconfont icon-user-info hide" ></i>
		        	{{$store.state.user.username}}<i class="el-icon-arrow-down el-icon--right"></i>
		    	</span>
				<el-dropdown-menu slot="dropdown">
					<el-dropdown-item><div class="nav-my-item"><i class="iconfont icon-expired"></i>{{$t('message.expired_time')}}：{{$store.state.user.expire_date}}</div></el-dropdown-item>
		        	<el-dropdown-item><div class="nav-my-item" @click="logout"><i class="iconfont icon-logout"></i>{{$t('message.logout')}}</div></el-dropdown-item>
		    	</el-dropdown-menu>
			</el-dropdown>
		</div>
      
      
      
    </div>	
</template>

<script>
	import * as types from '@/store/mutation-types.js'
	import http from '@/fetch/http.js'
	import router from '@/router'
    export default {
    	name:'header_box',
    	data(){
            return{
            }
        },
        created: function(){
        	this.init()
    	},
        methods: {
        	init(){
        		var self = this;
        		var url = "/common/curuser/";
    			http.get(url).then(res => {
    				if(res.response=='expired'){
    					self.$store.commit(types.LOGOUT);
    	            	window.location.href = '/logout/';
    				}else if(res.user && res.user.id){
    					self.$store.commit(types.LOGIN, {'user': res.user});
    					self.$i18n.locale = res.user.language;
    					router.push({
    		                'name': 'main'
    		            })
    				}
    			});
        	},
            logout() {
            	var self = this;
            	self.$store.commit(types.LOGOUT);
            	window.location.href = '/logout/';
            },
            clickFullscreen() {
   				this.$parent.fullScreen();
    		}
        }
    }

</script>

