const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');

const path = require('path');
const dirSrc = path.join(__dirname, 'src');

const HtmlWebpackPlugin = require('html-webpack-plugin');


devConfig = {
  mode: 'development',
  output: {
    publicPath: '/',
  },
  devtool: 'source-map',
  devServer: {
    port: 8001,
    watchFiles: ['src/**/*']
  },
  watchOptions: {
    ignored: ['**/node_modules/**/*', '**/\.\#*'],
  },
  plugins:[
    new HtmlWebpackPlugin({
      template: path.join(dirSrc, 'index.ejs'),
      window: {
        conf: {
          //deviceUrl: 'http://localhost:8000',
          deviceUrl: 'http://192.168.2.112',
        }
      }
    }),
  ]
}

module.exports = merge(common, devConfig)

