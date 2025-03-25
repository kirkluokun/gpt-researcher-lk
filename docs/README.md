# 网站

本网站使用 [Docusaurus 2](https://docusaurus.io/)，一款现代的静态网站生成器构建。

## 前提条件

要在本地构建和测试文档，首先需要下载并安装 [Node.js](https://nodejs.org/en/download/)，然后安装 [Yarn](https://classic.yarnpkg.com/en/)。  
在 Windows 上，你可以通过 Node.js 自带的 npm 包管理器安装 Yarn：

```console
npm install --global yarn
```

## 安装

```console
pip install pydoc-markdown
cd website
yarn install
```

## 本地开发

进入网站目录并运行以下命令：

```console
pydoc-markdown
yarn start
```

这会启动一个本地开发服务器，并自动打开浏览器窗口。大多数更改都会实时反映，无需重启服务器。