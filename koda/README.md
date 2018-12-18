### React 装饰器
为了支持装饰器，需要加载babel的装饰器插件
```bash
yarn add @babel/plugin-proposal-decorators --dev
yarn add @babel/plugin-transform-react-jsx --dev
```
同时在`create-react-app`中配置babel
```javascript
"babel": {
    "presets": [
      "react-app"
    ],
    "plugins": [
      [
        "@babel/plugin-proposal-decorators",
        {
          "legacy": true
        }
      ],
      [
        "@babel/plugin-transform-react-jsx"
      ]
    ]
  },
```