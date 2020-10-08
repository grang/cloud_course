<template>
<div class="app-box" id="app">
	<HeaderBox></HeaderBox>

	<div class="app-side">
		<LeftNavBox></LeftNavBox>
	</div>

	<div class="app-content">
		
		<div v-if="iframeSrc" class="player">
			<iframe 
				class="player-iframe" 
				:src="iframeSrc" 
				@load='iframeLoaded' 
				id="iframe" 
				name="mainIframe" 
				ref="mainIframe" 
				allowFullScreen="true" 
				frameborder="no" 
				border="0" 
			/>
	  	</div>
	  	
	</div>
	
</div>
</template>


<script>
import $ from 'jquery' 
import screenfull from 'screenfull'

import userConfig from '@/config'
import HeaderBox from '@/components/base/header'
import LeftNavBox from '@/components/base/left_nav'


String.prototype.endWith=function(endStr){
    var d=this.length-endStr.length;
    return (d>=0&&this.lastIndexOf(endStr)==d)
}
  
export default {
	name: 'main_page',
	data () {
		return {
			iframeSrc: ''
		}
	},
	created () {},
	mounted () {},
	methods : {
		iframeLoaded () {
		},
		updateIframeSrc(src){
			var self = this;
			if(src.endWith("pdf")){
				src = '/static/js/pdfjs/web/viewer.html?file='+src
			}
			self.iframeSrc = src;
		},
		fullScreen(){
			var self = this;
			if(screenfull.isEnabled){
				if(self.$refs.mainIframe){
					screenfull.request(self.$refs.mainIframe);
				}
			}else{
				alert('你的浏览器暂不支持全屏')
			}
		}
	},
	components : {
		HeaderBox ,
		LeftNavBox
	}
}
</script>

