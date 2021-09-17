const path = require("path");
const fs = require("fs");
const webpack = require("webpack");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");
// const HtmlWebpackPugPlugin = require('html-webpack-pug-plugin');
const ImageminWebpWebpackPlugin = require("imagemin-webp-webpack-plugin");
const env = process.env.NODE_ENV;
const CopyWebpackPlugin = require("copy-webpack-plugin");

let templates = [];
// let dir = 'app';
// let files = fs.readdirSync(dir);
//
// files.forEach(file => {
//   if (file.match(/\.pug$/)) {
//     let filename = file.substring(0, file.length - 4);
//     // templates.push(
//     //   new HtmlWebpackPlugin({
//     //     template: dir + '/' + filename + '.pug',
//     //     favicon: dir+'/favicon.png',
//     //     filename: filename + '.html'
//     //   })
//     // );
//   }
// });
// console.log({ path: path.join(__dirname, "../django/static") });

module.exports = {
  entry: {
    bundle: "./app/index.js",
  },

  mode: env,
  optimization: {
    nodeEnv: "production",
    minimize: true,
  },
  output: {
    path: path.resolve(__dirname, "../django/static"),

    filename: "[name].bundle.js",
    publicPath: "/",
  },

  devServer: {
    contentBase: path.join(__dirname, "../django/static"),
    compress: true,
    host: "0.0.0.0",
    // disableHostCheck: true,
    port: 3500,
    hot: true,
  },

  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,

        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            // Here you should change 'env' to '@babel/preset-env'
            presets: ["@babel/preset-env"],
          },
        },
      },

      {
        test: /\.pug$/,
        use: [
          {
            loader: "html-loader",
            options: {
              attributes: {
                list: [
                  {
                    tag: "img",
                    attribute: "src",
                    type: "src",
                  },
                  {
                    tag: "img",
                    attribute: "srcset",
                    type: "srcset",
                  },
                  {
                    tag: "img",
                    attribute: "data-src",
                    type: "src",
                  },
                ],
              },
            },
          },
          "pug-html-loader?pretty&exports=false",
        ],
      },
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          /*env == "development" ? "style-loader" :*/ MiniCssExtractPlugin.loader,
          "css-loader",
          "postcss-loader",
          "sass-loader",
        ],
      },
      {
        test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
        use: [
          {
            loader: "file-loader",
            options: {
              name: "[name].[ext]",
              outputPath: "app/fonts/",
            },
          },
        ],
      },
      {
        test: /\.(jpe?g|png|gif|ico|svg)$/i,
        use: [
          {
            loader: "file-loader",
            options: {
              esModule: false,
              name: "[name].[ext]",
              outputPath: "app/img/",
            },
          },
        ],
      },
    ],
  },
  resolve: {
    alias: {
      jquery: require.resolve("jquery"),
    },
  },
  plugins: [
    new CopyWebpackPlugin({
      patterns: [
        {
          from: path.resolve(__dirname, "./app/images"),
          to: path.resolve(__dirname, "../django/static/app/img"),
        },
        {
          from: path.resolve(__dirname, "./app/fonts"),
          to: path.resolve(__dirname, "../django/static/app/fonts"),
        },
      ],
    }),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
    }),

    new MiniCssExtractPlugin({
      // Options similar to the same options in webpackOptions.output
      // both options are optional
      filename: "[name].css",
      chunkFilename: "[id].css",
    }),

    // ...templates,
    // new HtmlWebpackPugPlugin({
    //   favicon: "./app/favicon.png",
    // }),
    //new ImageminWebpWebpackPlugin()
  ],
};
