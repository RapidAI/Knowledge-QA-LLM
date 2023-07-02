## QA-LocalKnowledge-LLM
- 基于本地知识库+LLM的问答。该项目的思路是由[langchain-ChatGLM](https://github.com/imClumsyPanda/langchain-ChatGLM)而来。
- 缘由：
  - 之前使用过这个项目，感觉不是太灵活，部署不太友好。
  - 借鉴[如何用大语言模型构建一个知识问答系统](https://mp.weixin.qq.com/s/movaNCWjJGBaes6KxhpYpg)中思路，尝试以为作为实践。
- 整个项目为模块化配置，不依赖`lanchain`库，各部分可轻易替换。

#### 整体框架
1. 解析文档并存入数据库
    ```mermaid
    flowchart TD

    A(["文档（*.txt, *.pdf, *.docx, *.pptx, *.excel）"]) --ExtractText--> B([sentences])
    B --Embedding--> C([Embeddings])
    C --Store--> D[(DataBase)]
    ```
2. 检索并回答问题
    ```mermaid
    flowchart LR
    E([问题]) --Embedding--> F([Embeddings]) --Search--> H[(Database)] --> G([Context])
    E --> I([Prompt])
    G --> I --> J([LLM]) --> K([Answer])
    ```

#### 🛠 所用工具
- 文档解析：[`extract_office_content`](https://github.com/SWHL/ExtractOfficeContent), [`rapidocr_pdf`](https://github.com/RapidAI/RapidOCRPDF)
- 提取特征向量：[`moka-ai/m3e-small`](https://huggingface.co/moka-ai/m3e-base)
- 向量存储：`sqlite`
- 向量检索：[`faiss`](https://github.com/facebookresearch/faiss)
