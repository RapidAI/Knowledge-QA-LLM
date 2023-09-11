---
weight: 4
date: "2023-09-11"
draft: false
author: "SWHL"
title: "Installation"
icon: "interactive_space"
toc: true
description: ""
publishdate: "2023-09-08"
tags:
categories:
---


### 1. Clone the whole repo into local directory.
```bash
git clone https://github.com/RapidAI/Knowledge-QA-LLM.git
```
### 2. Install the requirements.
```bash
cd Knowledge-QA-LLM
pip install -r requirements.txt
```

### 3. Download models.
Download the [`moka-ai/m3e-small`](https://huggingface.co/moka-ai/m3e-small/tree/main) model and put it in the `assets/models/m3e-small` directory. This model is used to vectorize text content.

### 4. Configure the LLM API.
Separately configure the interface of `chatglm2-6b`, interface startup reference: [ChatGLM2-6B API](https://github.com/THUDM/ChatGLM2-6B/blob/main/api.py). The specific usage method Reference: [`knowledge_qa_llm/llm/chatglm2_6b.py`](./knowledge_qa_llm/llm/chatglm2_6b.py)

### 5. Change the `config.yaml`.
Write the deployed `llm_api` to the `llm_api_url` field in the configuration file [`knowledge_qa_llm/config.yaml`](./knowledge_qa_llm/config.yaml).
