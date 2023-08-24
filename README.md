[简体中文](https://github.com/RapidAI/Knowledge-QA-LLM/blob/main/docs/README_zh.md) | English

# 🧐 Knowledge QA LLM
<p>
     <a href=""><img src="https://img.shields.io/badge/Python->=3.8,<3.12-aff.svg"></a>
     <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
     <a href=""><img src="https://img.shields.io/github/v/release/RapidAI/QA-LocalKnowledge-LLM?logo=github"></a>
     <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
     <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
     <a href="https://choosealicense.com/licenses/apache-2.0/"><img alt="GitHub" src="https://img.shields.io/github/license/RapidAI/Knowledge-QA-LLM"></a>
</p>

### 📣 We're looking for front-end development engineers interested in Knowledge QA with LLM, who can help us achieve front-end and back-end separation with our current implementation.

- Questions & Answers based on local knowledge base + LLM.
- Reason:
    - The idea of this project comes from [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat)
    - I have used this project before, but it is not very flexible and deployment is not very friendly.
    - Learn from the ideas in [How to build a knowledge question answering system with a large language model](https://mp.weixin.qq.com/s/movaNCWjJGBaes6KxhpYpg), and try to use this as a practice.
- Advantage:
    - The whole project is modularized and does not depend on the `lanchain` library, each part can be easily replaced, and the code is simple and easy to understand.
    - In addition to the large language model interface that needs to be deployed separately, other parts can use CPU.
    - Support documents in common formats, including `txt, md, pdf, docx, pptx, excel` etc. Of course, other types of documents can also be customized and supported.

### Architecture
- Parse the document and store it in the database
    ```mermaid
    flowchart LR

    A([Documents]) --ExtractText--> B([sentences])
    B --Embeddings--> C([Embeddings])
    C --Store--> D[(DataBase)]
    ```
- Retrieve and answer questions
    ```mermaid
    flowchart LR
    E([Query]) --Embedding--> F([Embeddings]) --> H[(Database)] --Search--> G([Context])
    E --> I([Prompt])
    G --> I --> J([LLM]) --> K([Answer])
    ```

### Installation
1. Clone the whole repo into local directory.
    ```bash
    git clone https://github.com/RapidAI/Knowledge-QA-LLM.git
    ```
2. Install the requirements.
    ```bash
    cd Knowledge-QA-LLM
    pip install -r requirements.txt
    ```
3. Download the [`moka-ai/m3e-small`](https://huggingface.co/moka-ai/m3e-small/tree/main) model and put it in the `assets/models/m3e-small` directory. This model is used to vectorize text content.
4. Separately configure the interface of `chatglm2-6b`, interface startup reference: [ChatGLM2-6B API](https://github.com/THUDM/ChatGLM2-6B/blob/main/api.py). The specific usage method Reference: [`knowledge_qa_llm/llm/chatglm2_6b.py`](./knowledge_qa_llm/llm/chatglm2_6b.py)
5. Write the deployed `llm_api` to the `llm_api_url` field in the configuration file [`knowledge_qa_llm/config.yaml`](./knowledge_qa_llm/config.yaml).

### Usage
1. Run
    ```bash
    streamlit run webui.py
    ```
2. UI Demo

    <div align="center">
        <img src="https://github.com/RapidAI/Knowledge-QA-LLM/releases/download/v0.0.1/UIDemo.gif" width="100%" height="100%">
    </div>

3. CLI Demo
    ```bash
    python cli.py
    ```
    <div align="center">
        <img src="https://github.com/RapidAI/Knowledge-QA-LLM/releases/download/v0.0.1/demo.gif" width="100%" height="100%">
    </div>

### 🛠 Tools Used
- Document analysis: [`extract_office_content`](https://github.com/SWHL/ExtractOfficeContent), [`rapidocr_pdf`](https://github.com/RapidAI/RapidOCRPDF), [`rapidocr_onnxruntime`](https://github.com/RapidAI/RapidOCR)
- Extract feature vector: [`moka-ai/m3e-small`](https://huggingface.co/moka-ai/m3e-base)
- Vector storage: `sqlite`
- Vector retrieval: [`faiss`](https://github.com/facebookresearch/faiss)
- UI: [`streamlit>=1.25.0`](https://github.com/streamlit/streamlit)


### 📂 File structure
```python
.
├── assets
│ ├── db                # store vector database
│ ├── models            # place the model for extracting embedding
│ └── raw_upload_files
├── knowledge_qa_llm
│ ├── __init__.py
│ ├── config.yaml       # configuration file
│ ├── file_loader       # Handle documents in various formats
│ ├── encoder           # Extract embeddings
│ ├── llm               # Large model interface, the large model needs to be deployed separately and called by interface
│ ├── utils
│ └── vector_utils      # embedding access and search
├── LICENSE
├── README.md
├── requirements.txt
├── tests
├── cli.py
└── webui.py            # UI implementation based on streamlit
```

### Changelog
<details>
    <summary>Click to expand</summary>

- 2023-08-11 v0.0.7 update:
  - Optimize layout, remove the plugin option, and put the extract vector model option on the home page.
  - The tips are translated into English for easy communication.
  - Add project logo:🧐
  - Update CLI module code.
- 2023-08-05 v0.0.6 update:
  - Adapt more llm_api, include online llm api, such ad ERNIE-Bot-Turbo.
  - Add the status of extracting embeddings.
- 2023-08-04 v0.0.5 update:
  - Fixed the problem of duplicate data inserted into the database.
- 2023-07-29 v0.0.4 update:
  - Reorganize the UI based `streamlit==1.25.0`
  - Optimize the code.
  - Record the GIF demo of UI.
- 2023-07-28 v0.0.3 update:
  - Finish the file_loader part.
- 2023-07-25 v0.0.2 update:
   - Standardize the existing directory structure, more compact, extract some variables into `config.yaml`
   - Perfect documentation
</details>

### Contributing
- Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
- Please make sure to update tests as appropriate.
