const path = require('path')

module.exports = {
  NODE_ENV: "development",
  outputDir: path.resolve(__dirname, '../../../static/dist/debug/app'),
  watch: true
}
