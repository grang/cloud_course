import Vue from 'vue'
import locale from 'element-ui/lib/locale'
import VueI18n from 'vue-i18n'
import messages from './langs'
Vue.use(VueI18n)


var lang = ''
var type = navigator.appName;
　　if (type == "Netscape"){
		lang = navigator.language;//获取浏览器配置语言，支持非IE浏览器
　　}else{
    　　lang = navigator.userLanguage;//获取浏览器配置语言，支持IE5+ == navigator.systemLanguage
　　}
lang = lang.substr(0, 2);//获取浏览器配置语言前两位

const i18n = new VueI18n({
  locale: lang || 'zh',
  messages
})
locale.i18n((key, value) => i18n.t(key, value))
export default i18n
