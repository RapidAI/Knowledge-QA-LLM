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
        <b><font size="6"><i>🧐 Knowledge QA LLM</i></font></b>
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

### Introduction
- Questions & Answers based on local knowledge base + LLM.
- Reason:
    - The idea of this project comes from [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat)
    - I have used this project before, but it is not very flexible and deployment is not very friendly.
    - Learn from the ideas in [How to build a knowledge question answering system with a large language model](https://mp.weixin.qq.com/s/movaNCWjJGBaes6KxhpYpg), and try to use this as a practice.
- Advantage:
    - The whole project is modularized and does not depend on the `lanchain` library, each part can be easily replaced, and the code is simple and easy to understand.
    - In addition to the large language model interface that needs to be deployed separately, other parts can use CPU.
    - Support documents in common formats, including `txt, md, pdf, docx, pptx, excel` etc. Of course, other types of documents can also be customized and supported.

### 📣 We're looking for front-end development engineers interested in Knowledge QA with LLM, who can help us achieve front-end and back-end separation with our current implementation.

### Architecture
#### Parse the document and store it in the database
```mermaid
flowchart LR

A([Documents]) --ExtractText--> B([sentences])
B --Embeddings--> C([Embeddings])
C --Store--> D[(DataBase)]
```

#### Retrieve and answer questions
```mermaid
flowchart LR
E([Query]) --Embedding--> F([Embeddings]) --> H[(Database)] --Search--> G([Context])
E --> I([Prompt])
G --> I --> J([LLM]) --> K([Answer])
```

#### Tools Used
- Document analysis: [`extract_office_content`](https://github.com/SWHL/ExtractOfficeContent), [`rapidocr_pdf`](https://github.com/RapidAI/RapidOCRPDF), [`rapidocr_onnxruntime`](https://github.com/RapidAI/RapidOCR)
- Extract feature vector: [`moka-ai/m3e-small`](https://huggingface.co/moka-ai/m3e-base)
- Vector storage: `sqlite`
- Vector retrieval: [`faiss`](https://github.com/facebookresearch/faiss)
- UI: [`streamlit>=1.25.0`](https://github.com/streamlit/streamlit)
