
const path = require('path')

module.exports = {
  NODE_ENV: "production",
  outputDir: path.resolve(__dirname, '../../../static/dist/prod/app'),
  watch: false
}
