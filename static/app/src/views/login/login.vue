<template>
  <div class="login-container">
    <el-form ref="loginForm" :model="loginForm" class="login-form" autocomplete="on" label-position="left">

      <div class="title-container">
      	<img class="logo" src="/static/images/chinese_icon.png"/>
      </div>
      
	<el-form-item label="">
		<el-input ref="username" v-model="loginForm.username" :placeholder="$t('message.username_input')"></el-input>
	</el-form-item>
	<el-form-item label="">
		<el-input type="password" v-model="loginForm.password" :placeholder="$t('message.password_input')" @keyup.enter.native="login"></el-input>
	</el-form-item>
      
      <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;" @click.native.prevent="login">{{$t('message.login_btn')}}</el-button>

      <div class="footer">
        <h5>{{$t('message.version')}} {{ version }}</h5>
      </div>
    </el-form>

  </div>
</template>

<script>
import http from '@/fetch/http.js'
import userConfig from '@/config'
import router from '@/router'
import * as types from '@/store/mutation-types.js'

export default {
	name: 'Login',
	data () {
		return {
			loginForm : {
				username : '',
				password : ''
			},
			loading : false,
			version : userConfig.version
		}
	},
	created () {},
	mounted () {
		this.$refs.username.focus()
	},
	methods: {
		login(event){
			var self = this;
			self.loading = true

			http.post('/login/', self.loginForm).then(res => {
				self.loading = false
				if (res.response == 'ok') {
					router.push({
						name: 'main'
					})
				}else if(res.response=='expired'){
					self.$message.error(self.$t('errors.user_expired'))
				}else{
					self.$message.error(self.$t('errors.wrong_password'))
				}
			});
		}
	}
}
</script>

