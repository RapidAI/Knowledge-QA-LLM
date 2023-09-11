---
weight: 2
date: "2023-09-11"
draft: false
author: "SWHL"
title: "Architecture"
icon: "apartment"
toc: true
description: ""
publishdate: "2023-09-08"
tags:
categories:
---


### Parse the document and store it in the database
```mermaid
flowchart LR

A([Documents]) --ExtractText--> B([sentences])
B --Embeddings--> C([Embeddings])
C --Store--> D[(DataBase)]
```

### Retrieve and answer questions
```mermaid
flowchart LR
E([Query]) --Embedding--> F([Embeddings]) --> H[(Database)] --Search--> G([Context])
E --> I([Prompt])
G --> I --> J([LLM]) --> K([Answer])
```

### Tools Used
- Document analysis: [`extract_office_content`](https://github.com/SWHL/ExtractOfficeContent), [`rapidocr_pdf`](https://github.com/RapidAI/RapidOCRPDF), [`rapidocr_onnxruntime`](https://github.com/RapidAI/RapidOCR)
- Extract feature vector: [`moka-ai/m3e-small`](https://huggingface.co/moka-ai/m3e-base)
- Vector storage: `sqlite`
- Vector retrieval: [`faiss`](https://github.com/facebookresearch/faiss)
- UI: [`streamlit>=1.25.0`](https://github.com/streamlit/streamlit)
