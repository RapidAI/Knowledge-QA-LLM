[English](https://github.com/RapidAI/Knowledge-QA-LLM) | 简体中文

## Knowledge QA LLM
<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.12-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href=""><img src="https://img.shields.io/github/v/tag/RapidAI/QA-LocalKnowledge-LLM?logo=github"></a>
    <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

- 基于本地知识库+LLM的问答。该项目的思路是由[langchain-ChatGLM](https://github.com/imClumsyPanda/langchain-ChatGLM)而来。
- 缘由：
  - 之前使用过这个项目，感觉不是太灵活，部署不太友好。
  - 借鉴[如何用大语言模型构建一个知识问答系统](https://mp.weixin.qq.com/s/movaNCWjJGBaes6KxhpYpg)中思路，尝试以此作为实践。
- 整个项目为模块化配置，不依赖`lanchain`库，各部分可轻易替换。
- 除需要单独部署大模型接口外，其他部分用CPU即可。

#### TODO
- [x] 完善解析office文档接口及单元测试
- [ ] 完善PDF提取接口及单元测试
- [ ] 完善图像内容提取接口及单元测试
- [x] 完善LLM接口
- [ ] 完善UI
- [ ] 增加上传文档接口

#### 整体框架
- 解析文档并存入数据库
    ```mermaid
    flowchart LR

    A(["文档（*.txt, *.pdf, *.docx, *.pptx, *.excel）"]) --ExtractText--> B([sentences])
    B --Embedding--> C([Embeddings])
    C --Store--> D[(DataBase)]
    ```
- 检索并回答问题
    ```mermaid
    flowchart LR
    E([Query]) --Embedding--> F([Embeddings]) --Search--> H[(Database)] --> G([Context])
    E --> I([Prompt])
    G --> I --> J([LLM]) --> K([Answer])
    ```

#### 使用
1. 使用之前要做的事情：
   1. 下载[`moka-ai/m3e-small`](https://huggingface.co/moka-ai/m3e-small/tree/main)模型，放到`assets/models/m3e-small`目录下
   2. 单独配置好`chatglm2-6b`的接口，接口启动参考：[ChatGLM2-6B API](https://github.com/THUDM/ChatGLM2-6B/blob/main/api.py)，具体使用方式参考：`knowledge_qa_llm/llm/chatglm2_6b.py`
   3. 将部署好的llm_api写到配置文件`config.yaml`中的`llm_api_url`字段下。
2. 运行
    ```bash
    streamlit run webui.py
    ```

#### 🛠 所用工具
- 文档解析：[`extract_office_content`](https://github.com/SWHL/ExtractOfficeContent), [`rapidocr_pdf`](https://github.com/RapidAI/RapidOCRPDF)
- 提取特征向量：[`moka-ai/m3e-small`](https://huggingface.co/moka-ai/m3e-base)
- 向量存储：`sqlite`
- 向量检索：[`faiss`](https://github.com/facebookresearch/faiss)


#### 📂 文件结构
```text
.
├── assets
│   ├── db                  # 存放向量数据库
│   ├── models              # 放置提取embedding的模型
│   └── raw_upload_files
├── cli.py
├── config.yaml             # 配置文件
├── knowledge_qa_llm
│   ├── __init__.py
│   ├── file_loader         # 处理各种格式的文档
│   ├── llm                 # 大模型接口，大模型需要单独部署，以接口方式调用
│   ├── utils
│   └── vector_utils        # embedding的存取和搜索
├── LICENSE
├── README.md
├── requirements.txt
├── tests
└── webui.py                # 基于streamlit的UI实现
```

#### 更新日志
- 2023-07-25 v0.0.2 update:
  - 规范现有目录结构，更加紧凑，提取部分变量到`config.yaml`中
  - 完善说明文档