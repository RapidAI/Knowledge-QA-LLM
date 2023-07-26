English | [简体中文](https://github.com/RapidAI/Knowledge-QA-LLM/blob/main/docs/README_zh.md)

## Knowledge QA LLM
<p>
     <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.12-aff.svg"></a>
     <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
     <a href=""><img src="https://img.shields.io/github/v/tag/RapidAI/QA-LocalKnowledge-LLM?logo=github"></a>
     <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
     <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

- Q&A based on local knowledge base + LLM. The idea of this project comes from [langchain-ChatGLM](https://github.com/imClumsyPanda/langchain-ChatGLM).
- Reason:
   - I have used this project before, but it is not very flexible and deployment is not very friendly.
   - Learn from the ideas in [How to build a knowledge question answering system with a large language model](https://mp.weixin.qq.com/s/movaNCWjJGBaes6KxhpYpg), and try to use this as a practice.
- The whole project is a modular configuration, does not depend on the `lanchain` library, and each part can be easily replaced.
- In addition to the large model interface that needs to be deployed separately, other parts can use CPU.

#### TODO
- [x] Improve parsing office document interface and unit test
- [ ] Improve PDF extraction interface and unit test
- [ ] Improve image content extraction interface and unit test
- [x] Improve the LLM interface
- [ ] Improve the UI
- [ ] Add interface for uploading documents

#### Overall framework
- Parse the document and store it in the database
     ```mermaid
     flowchart LR

     A(["Documents (*.txt, *.pdf, *.docx, *.pptx, *.excel)"]) --ExtractText--> B([sentences])
     B --Embeddings--> C([Embeddings])
     C --Store--> D[(DataBase)]
     ```
- Retrieve and answer questions
     ```mermaid
     flowchart LR
     E([Query]) --Embedding--> F([Embeddings]) --Search--> H[(Database)] --> G([Context])
     E --> I([Prompt])
     G --> I --> J([LLM]) --> K([Answer])
     ```

#### Run
1. Things to do before using:
    1. Download the [`moka-ai/m3e-small`](https://huggingface.co/moka-ai/m3e-small/tree/main) model and put it in the `assets/models/m3e-small` directory
    2. Separately configure the interface of `chatglm2-6b`, interface startup reference: [ChatGLM2-6B API](https://github.com/THUDM/ChatGLM2-6B/blob/main/api.py), the specific usage method Reference: `knowledge_qa_llm/llm/chatglm2_6b.py`
    3. Write the deployed llm_api to the `llm_api_url` field in the configuration file `config.yaml`.
2. Run
    ```bash
    streamlit run webui.py
    ```

#### 🛠 Tools Used
- Document analysis: [`extract_office_content`](https://github.com/SWHL/ExtractOfficeContent), [`rapidocr_pdf`](https://github.com/RapidAI/RapidOCRPDF)
- Extract feature vector: [`moka-ai/m3e-small`](https://huggingface.co/moka-ai/m3e-base)
- Vector storage: `sqlite`
- Vector retrieval: [`faiss`](https://github.com/facebookresearch/faiss)


#### 📂 File structure
```python
.
├── assets
│ ├── db # store vector database
│ ├── models # place the model for extracting embedding
│ └── raw_upload_files
├── cli.py
├── config.yaml # configuration file
├── knowledge_qa_llm
│ ├── __init__.py
│ ├── file_loader # Handle documents in various formats
│ ├── llm #Large model interface, the large model needs to be deployed separately and called by interface
│ ├── utils
│ └── vector_utils # embedding access and search
├── LICENSE
├── README.md
├── requirements.txt
├── tests
└── webui.py # UI implementation based on streamlit
```

#### Update Log
- 2023-07-25 v0.0.2 update:
   - Standardize the existing directory structure, more compact, extract some variables into `config.yaml`
   - Perfect documentation