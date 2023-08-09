[English](https://github.com/RapidAI/Knowledge-QA-LLM) | 简体中文

## Knowledge QA LLM
<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.8,<3.12-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href=""><img src="https://img.shields.io/github/v/tag/RapidAI/QA-LocalKnowledge-LLM?logo=github"></a>
    <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

- 基于本地知识库+LLM的问答系统。该项目的思路是由[langchain-ChatGLM](https://github.com/imClumsyPanda/langchain-ChatGLM)启发而来。
- 缘由：
  - 之前使用过这个项目，感觉不是太灵活，部署不太友好。
  - 借鉴[如何用大语言模型构建一个知识问答系统](https://mp.weixin.qq.com/s/movaNCWjJGBaes6KxhpYpg)中思路，尝试以此作为实践。
- 优势：
    - 整个项目为模块化配置，不依赖`lanchain`库，各部分可轻易替换，代码简单易懂。
    - 除需要单独部署大模型接口外，其他部分用CPU即可。
    - 支持常见格式文档，包括txt、md、pdf, docx, pptx, excel等等。当然，也可自定义支持其他类型文档。
- 📣 **招募：前端开发工程师，用于开发前端界面，做到前后端分离。**

#### 整体流程
- 解析文档并存入数据库
    ```mermaid
    flowchart LR

    A(["文档"]) --ExtractText--> B([sentences])
    B --Embedding--> C([Embeddings])
    C --Store--> D[(DataBase)]
    ```
- 检索并回答问题
    ```mermaid
    flowchart LR
    E([Query]) --Embedding--> F([Embeddings]) --> H[(Database)] --Search--> G([Context])
    E --> I([Prompt])
    G --> I --> J([LLM]) --> K([Answer])
    ```

#### 使用
1. 下载和部署模型
   1. 下载[`moka-ai/m3e-small`](https://huggingface.co/moka-ai/m3e-small/tree/main)模型，放到`assets/models/m3e-small`目录下，用于向量化文本内容。
   2. 单独配置好`chatglm2-6b`的接口，接口启动参考：[ChatGLM2-6B API](https://github.com/THUDM/ChatGLM2-6B/blob/main/api.py)。具体使用方式可参考：`knowledge_qa_llm/llm/chatglm2_6b.py`
   3. 将部署好的`llm_api`写到配置文件`knowledge_qa_llm/config.yaml`中的`llm_api_url`字段下。
2. 安装运行环境
    ```bash
    pip install -r requirements.txt --no-cache-dir
    ```
3. 运行
    ```bash
    streamlit run webui.py
    ```
4. UI Demo

    <div align="center">
        <img src="https://github.com/RapidAI/Knowledge-QA-LLM/releases/download/v0.0.1/UIDemo.gif" width="100%" height="100%">
    </div>
5. CLI Demo

    <div align="center">
        <img src="https://github.com/RapidAI/Knowledge-QA-LLM/releases/download/v0.0.1/demo.gif" width="100%" height="100%">
    </div>

#### 🛠 所用工具
- 文档解析：[`extract_office_content`](https://github.com/SWHL/ExtractOfficeContent), [`rapidocr_pdf`](https://github.com/RapidAI/RapidOCRPDF), [`rapidocr_onnxruntime`](https://github.com/RapidAI/RapidOCR)
- 提取特征向量：[`moka-ai/m3e-small`](https://huggingface.co/moka-ai/m3e-base)
- 向量存储：`sqlite`
- 向量检索：[`faiss`](https://github.com/facebookresearch/faiss)
- UI: [`streamlit>=1.25.0`](https://github.com/streamlit/streamlit)


#### 📂 文件结构
```text
.
├── assets
│   ├── db                  # 存放向量数据库
│   ├── models              # 放置提取embedding的模型
│   └── raw_upload_files
├── knowledge_qa_llm
│   ├── __init__.py
│   ├── config.yaml         # 配置文件
│   ├── file_loader         # 处理各种格式的文档
│   ├── llm                 # 大模型接口，大模型需要单独部署，以接口方式调用
│   ├── utils
│   └── vector_utils        # embedding的存取和搜索
├── LICENSE
├── README.md
├── requirements.txt
├── tests
├── cli.py
└── webui.py                # 基于streamlit的UI实现
```

#### 更新日志
- 2023-08-05 v0.0.6 update:
  - 适配更多模型接口，包括在线大模型接口，例如文心一言
  - 添加提取特征向量的状态提示
- 2023-08-04 v0.0.5 update:
  - 修复了插入数据库数据重复的问题。
- 2023-07-29 v0.0.4 update:
  - 基于`streamlit==1.25.0`优化UI
  - 优化代码
  - 录制UI GIF demo
- 2023-07-28 v0.0.3 update:
  - 完成文件解析部分
- 2023-07-25 v0.0.2 update:
  - 规范现有目录结构，更加紧凑，提取部分变量到`config.yaml`中
  - 完善说明文档