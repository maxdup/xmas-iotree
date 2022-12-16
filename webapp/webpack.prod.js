const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');

const path = require('path');
const dirSrc = path.join(__dirname, 'src');

const TerserJSPlugin = require('terser-webpack-plugin');
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const HtmlWebpackPlugin = require('html-webpack-plugin');

prodConfig = {
  mode: 'production',
  output: {
    clean: true,
    publicPath: '/build/'
  },
  plugins: [
    new CssMinimizerPlugin(),
    new HtmlWebpackPlugin({
      template: path.join(dirSrc, 'index.ejs'),
      window: {
        conf: {
          deviceUrl: 'http://192.168.2.112',
        }
      }
    })],
  optimization: {
    minimize: true,
    minimizer: [new TerserJSPlugin({}), new CssMinimizerPlugin()],
  },
}

module.exports = merge(common, prodConfig)
