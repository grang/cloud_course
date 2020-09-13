const webpack = require('webpack')
const path = require('path')
const UglifyPlugin = require('uglifyjs-webpack-plugin')

var proEnv = require('./config/prod.env');  // 生产环境
var devEnv = require('./config/dev.env');  // 本地环境


let env_type = process.argv[4];

var env = {}
if(env_type === 'prod'){  
	env = proEnv;
	
	process.env.NODE_ENV = 'production'
	process.env.BABEL_ENV = 'production'
}else{
	env = devEnv;
	process.env.NODE_ENV = 'production1'
	process.env.BABEL_ENV = 'production1'
}

function resolve(dir) {
	return path.resolve(__dirname, dir);
}
module.exports = {
	publicPath : './', // 基本路径
	outputDir : env.outputDir, // 输出文件目录
	lintOnSave : false, // eslint-loader 是否在保存的时候检查
	
	filenameHashing: false,
	productionSourceMap: false,
	
	chainWebpack : (config) => {
		if(process.env.NODE_ENV=='production'){
			//config.plugin('webpack-bundle-analyzer').use(require('webpack-bundle-analyzer').BundleAnalyzerPlugin)
		}
        config.resolve.alias
		.set('@', path.resolve(__dirname, './src'))
	},
	configureWebpack : (config) => {
		config.watch = env.watch
		config.performance = false
		console.info(env)
		
		//只有打包生产环境才需要将console删除
	    if(process.env.NODE_ENV=='production'){
	    	let plugins = [
				new webpack.ProgressPlugin()
				
			];
	    	config.plugins = [...config.plugins, ...plugins];
		
			config.mode = 'production'
			// 将每个依赖包打包成单独的js文件
			let optimization = {
				//runtimeChunk : 'single',
				runtimeChunk: { name: 'runtime' },
				splitChunks : {
					chunks : 'all',
					maxInitialRequests : Infinity,
					minSize : 20000,
					cacheGroups : {
						vendor : {
							test : /[\\/]node_modules[\\/]/,
							chunks: 'initial',
					        name: 'vendors'
						}
					}
				},
				minimizer : [ new UglifyPlugin({
					uglifyOptions : {
						compress : {
							drop_console : true, // console
							drop_debugger : false,
							pure_funcs : [ 'console.log' ] // 移除console
						},
			        	output:{
			        		comments: false,
			        	}
					},
					sourceMap: false,
			    	parallel: true
				}) ]
			}
			Object.assign(config, {
				optimization
			})
			
		} else {
			config.mode = 'development'
		}
	},
	css: {
		extract : true, // 是否使用css分离插件 ExtractTextPlugin
		sourceMap : false, // 开启 CSS source maps?
		loaderOptions : {
			css : {}, // 这里的选项会传递给 css-loader
			postcss : {} // 这里的选项会传递给 postcss-loader
		}, 
		modules : false // 启用 CSS modules for all css / pre-processor files.
	},
	parallel : require('os').cpus().length > 1, // 是否为 Babel 或 TypeScript 使用 thread-loader。该选项在系统的 CPU 有多于一个内核时自动启用，仅作用于生产构建。
	pwa : {}, // PWA 插件相关配置 see https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-pwa
	devServer : {
		proxy: 'http://127.0.0.1:8000/classware'
	},
	// 第三方插件配置
	pluginOptions : {
		
	}
}