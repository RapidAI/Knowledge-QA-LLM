<div align="center">
  <div align="center">
    <h1><b>🧐 Knowledge QA LLM</b></h1>
  </div>
  <a href=""><img src="https://img.shields.io/badge/Python->=3.8,<3.12-aff.svg"></a>
  <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
  <a href=""><img src="https://img.shields.io/github/v/release/RapidAI/QA-LocalKnowledge-LLM?logo=github"></a>
  <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
  <a href="https://choosealicense.com/licenses/apache-2.0/"><img alt="GitHub" src="https://img.shields.io/github/license/RapidAI/Knowledge-QA-LLM"></a>

  简体中文 | [English](../README.md)
</div>

### 简介
基于本地知识库+LLM的问答系统。该项目的思路是由[langchain-ChatGLM](https://github.com/imClumsyPanda/langchain-ChatGLM)启发而来。
- 缘由：
  - 之前使用过这个项目，感觉不是太灵活，部署不太友好。
  - 借鉴[如何用大语言模型构建一个知识问答系统](https://mp.weixin.qq.com/s/movaNCWjJGBaes6KxhpYpg)中思路，尝试以此作为实践。
- 优势：
    - 整个项目为模块化配置，不依赖`lanchain`库，各部分可轻易替换，代码简单易懂。
    - 除需要单独部署大模型接口外，其他部分用CPU即可。
    - 支持常见格式文档，包括txt、md、pdf, docx, pptx, excel等等。当然，也可自定义支持其他类型文档。


### [Demo](https://aistudio.baidu.com/projectdetail/6675380?contributionType=1)
<div align="center">
    <img src="https://github.com/RapidAI/Knowledge-QA-LLM/releases/download/v0.0.1/UIDemo.gif" width="100%" height="100%">
</div>

### 文档
完整文档请移步：[docs](https://rapidai.github.io/Knowledge-QA-LLM/).

### TODO
- [ ] Support keyword + vector hybrid search.
- [ ] Vue.js based UI .

### 贡献者
<p align="left">
  <a href="https://github.com/RapidAI/Knowledge-QA-LLM/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=RapidAI/Knowledge-QA-LLM" width="20%"/>
  </a>
</p>

### 贡献指南
我们感谢所有的贡献者为改进和提升 RapidOCR 所作出的努力。
- 欢迎提交请求。对于重大更改，请先打开issue讨论您想要改变的内容。
- 请确保适当更新测试。

### [赞助](https://rapidai.github.io/Knowledge-QA-LLM/docs/sponsor/)
如果您想要赞助该项目，可直接点击当前页最上面的Sponsor按钮，请写好备注(**您的Github账号名称**)，方便添加到赞助列表中。


### 开源许可证
该项目采用[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)开源许可证。
