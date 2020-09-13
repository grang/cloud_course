import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from '@/store/actions'
import * as getters from '@/store/getters'
import * as types from '@/store/mutation-types';

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'


const state = {
	user: JSON.parse(localStorage.getItem('user'))
}

const mutations = {
	[types.LOGIN](state, data){
		state.user = data.user;
		localStorage.setItem('user', JSON.stringify(data.user));
  },
  [types.LOGOUT](state){
    console.log("on logout");
    localStorage.removeItem('user');
		state.user = {};
  }
}

export default new Vuex.Store({
  state,
  mutations,
  modules: {
  },
  strict: debug
 // plugins: debug ? [createLogger()] : []
})
