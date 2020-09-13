<template>
<div class="menu-wrap">
	<el-tree :data="menu_list" :props="defaultProps" :highlight-current="true" @node-click="clickNode"></el-tree>
</div>

</template>

<script>
  import http from '@/fetch/http.js'
  import * as types from '@/store/mutation-types.js'
  import router from '@/router'
  export default {
    name: 'left_nav',
    data() {
      return {
        menu_list: [],
      	defaultProps: {
            children: 'children',
            label: 'label'
          }
      }
    },
    created: function () {
		
    },
    mounted: function () {
    	var self = this;
		var url = "/common/menu/";
		http.get(url).then(res => {
			if(res.response=='ok'){
				self.menu_list = res.menu;
			}
		});
		
		
    },
	methods : {
		clickNode(data, node) {
			if(data.link){
				this.$parent.updateIframeSrc(data.link);
			}
		}
	},
	components: {}
  }
</script>

