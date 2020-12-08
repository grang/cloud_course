<template>
	<div class="login-container">
		<div class="content" :style="contentBackground">
			<div class="left">
				<img src="../../assets/images/left.png" width="80%" height="80%"/>
			</div>
			<div class="right">
				<!-- <el-image
					src="../../assets/images/title_logo.png"
					fit="contain"
					lazy
				>
				</el-image> -->
				<img class="logo"  src="../../assets/images/title_logo.png"  />
				<div>
				<el-form 
					ref="loginForm" 
					:model="loginForm"  
					autocomplete="on" 
				>
					<el-form-item>
						<el-input 
							ref="username" 
							v-model="loginForm.username" 
							:placeholder="$t('message.username_input')"
							prefix-icon="el-icon-user-solid"
						>
							<!-- <i slot="prefix" style="display: flex;align-items: center;">
							<img
								style="width:18px;height:22px"
								src="../../assets/images/username_icon.png"
								alt
							/>
							</i> -->
						</el-input>
					</el-form-item>
					<el-form-item>
						<el-input 
							type="password" 
							v-model="loginForm.password" 
							:placeholder="$t('message.password_input')" 
							@keyup.enter.native="login"
							prefix-icon="el-icon-lock"
						>
							<!-- <i slot="prefix" style="display: flex;align-items: center;">
							<img
								style="width:18px;height:22px"
								src="../../assets/images/pwd_icon.png"
								alt
							/>
							</i> -->
						</el-input>
					</el-form-item>

					<el-button 
						:loading="loading" 
						round
						type="primary"
						style="width:100%;margin-bottom:30px;" 
						@click.native.prevent="login"
					>{{$t('message.login_btn')}}
					</el-button>
				</el-form>
				</div>
			</div>
		</div>
		
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
			version : userConfig.version,
			// setBackground: {
			// 	backgroundImage: "url(" + require("../../assets/images/back.png") + ")",
			// },
			contentBackground: {
				backgroundImage: "url(" + require("../../assets/images/contentBack.png") + ")",
			}
		}
	},
	created () {},
	mounted () {
		// this.$refs.username.focus()
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

