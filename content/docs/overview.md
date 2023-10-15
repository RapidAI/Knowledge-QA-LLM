---
weight: 100
date: "2023-09-08"
draft: false
author: "SWHL"
title: "概览"
icon: "circle"
toc: true
description: ""
publishdate: "2023-09-08"
---

<div align="center">
    <div>&nbsp;</div>
    <div align="center">
        <b><font size="6">🧐 Knowledge QA LLM</font></b>
    </div>
    <div>&nbsp;</div>
     <a href=""><img src="https://img.shields.io/badge/Python->=3.8,<3.12-aff.svg"></a>
     <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
     <a href=""><img src="https://img.shields.io/github/v/release/RapidAI/QA-LocalKnowledge-LLM?logo=github"></a>
     <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
     <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
     <a href="https://choosealicense.com/licenses/apache-2.0/"><img alt="GitHub" src="https://img.shields.io/github/license/RapidAI/Knowledge-QA-LLM"></a>
     <a href="https://github.com/RapidAI/Knowledge-QA-LLM"><img src="https://img.shields.io/badge/Github-KnowledgeQALLM-brightgreen"></a>

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

### 整体流程
#### 解析文档并存储在数据库
```mermaid
flowchart LR

A([Documents]) --ExtractText--> B([sentences])
B --Embeddings--> C([Embeddings])
C --Store--> D[(DataBase)]
```

#### 检索并回答问题
```mermaid
flowchart LR
E([Query]) --Embedding--> F([Embeddings]) --> H[(Database)] --Search--> G([Context])
E --> I([Prompt])
G --> I --> J([LLM]) --> K([Answer])
```

### 使用的工具
- 文档分析: [`extract_office_content`](https://github.com/SWHL/ExtractOfficeContent), [`rapidocr_pdf`](https://github.com/RapidAI/RapidOCRPDF), [`rapidocr_onnxruntime`](https://github.com/RapidAI/RapidOCR)
- 提取语义向量: [`moka-ai/m3e-small`](https://huggingface.co/moka-ai/m3e-base)
- 向量存储: `sqlite`
- 向量检索: [`faiss`](https://github.com/facebookresearch/faiss)
- UI搭建: [`streamlit>=1.25.0`](https://github.com/streamlit/streamlit)
