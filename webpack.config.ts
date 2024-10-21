import * as path from 'path';
import * as webpack from 'webpack';

const extConfig: webpack.Configuration = {
  target: 'node',
  entry: './vscode/extension.ts',
  output: {
    filename: 'extension.js',
    libraryTarget: 'commonjs2',
    path: path.resolve(__dirname, 'out'),
  },
  resolve: { extensions: ['.ts', '.js'] },
  module: { rules: [{ test: /\.ts$/, loader: 'ts-loader' }] },
  externals: { vscode: 'vscode' },
};

const webviewConfig: webpack.Configuration = {
  target: 'web',
  entry: './vscode/webview/index.tsx',
  output: {
    filename: '[name].wv.js',
    path: path.resolve(__dirname, 'out'),
  },
  resolve: {
    extensions: ['.js', '.ts', '.tsx'],
  },
  module: {
    rules: [
      { test: /\.tsx?$/, use: ['babel-loader', 'ts-loader'] },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
};

export default [webviewConfig, extConfig];