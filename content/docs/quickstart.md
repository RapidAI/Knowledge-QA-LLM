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
本项目目前以Moka-AI的m3e模型作为提取特征向量的主要模型，当然其他模型，也可自行配置。

将[`moka-ai/m3e-small`](https://huggingface.co/moka-ai/m3e-small/tree/main)下载下来放到`assets/models/m3e-small`目录下，下载命令如下：
```python {linenos=table}
from sentence_transformers import SentenceTransformer

# 指定cache_dir即可
model = SentenceTransformer("moka-ai/m3e-small", cache_folder="assets/models")

# 验证是否可用
sentences = ["* Moka 此文本嵌入模型由 MokaAI 训练并开源，训练脚本使用 uniem",]
embeddings = model.encode(sentences)
for sentence, embedding in zip(sentences, embeddings):
    print("Sentence:", sentence)
    print("Embedding:", embedding)
    print("")
```

#### 4. 配置LLM API接口
首先需要单独在本地部署大模型，以API方式启动。以ChatGLM-6B为例，具体可参考[ChatGLM2-6B API](https://github.com/THUDM/ChatGLM2-6B/blob/main/api.py)

随后，[`knowledge_qa_llm/llm/chatglm2_6b.py`](./knowledge_qa_llm/llm/chatglm2_6b.py)是调用上一步LLM接口的类。

如果自己使用的LLM，没有该文件，可自行实现，保证输入和输出与现有的一致即可。

#### 5. 更改`config.yaml`配置文件
将调用ChatGLM-6B的`llm_api`的url写到[`knowledge_qa_llm/config.yaml`](./knowledge_qa_llm/config.yaml)配置文件中
```yaml {linenos=table}
LLM_API:
  ChatGLM2_6B: your_api
```

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