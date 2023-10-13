---
weight: 200
date: "2023-09-11"
draft: false
author: "SWHL"
title: "快速开始"
icon: "rocket_launch"
toc: true
publishdate: "2023-09-08"
---


#### 1. 克隆整个项目到本地
```bash {linenos=table}
git clone https://github.com/RapidAI/Knowledge-QA-LLM.git
```

#### 2. 安装运行环境
```bash {linenos=table}
cd Knowledge-QA-LLM
pip install -r requirements.txt
```

#### 3. 下载提取向量模型到本地
Download the [`moka-ai/m3e-small`](https://huggingface.co/moka-ai/m3e-small/tree/main) model and put it in the `assets/models/m3e-small` directory. This model is used to vectorize text content.

#### 4. 配置LLM API接口
Separately configure the interface of `chatglm2-6b`, interface startup reference: [ChatGLM2-6B API](https://github.com/THUDM/ChatGLM2-6B/blob/main/api.py). The specific usage method Reference: [`knowledge_qa_llm/llm/chatglm2_6b.py`](./knowledge_qa_llm/llm/chatglm2_6b.py)

#### 5. 更改`config.yaml`配置文件
Write the deployed `llm_api` to the `llm_api_url` field in the configuration file [`knowledge_qa_llm/config.yaml`](./knowledge_qa_llm/config.yaml).

#### 6. 运行
{{< alert context="info" text="streamlit框架的启动，不可以用`python webui.py`方式启动，必须用以下方式启动。" />}}

{{< tabs tabTotal="2">}}
{{% tab tabName="UI Demo" %}}

```bash {linenos=table}
streamlit run webui.py
```

<div align="center">
    <img src="https://github.com/RapidAI/Knowledge-QA-LLM/releases/download/v0.0.1/UIDemo.gif" width="100%" height="100%">
</div>

{{% /tab %}}
{{% tab tabName="CLI Demo" %}}

```bash {linenos=table}
python cli.py
```

<div align="center">
    <img src="https://github.com/RapidAI/Knowledge-QA-LLM/releases/download/v0.0.1/demo.gif" width="100%" height="100%">
</div>

{{% /tab %}}
{{< /tabs >}}