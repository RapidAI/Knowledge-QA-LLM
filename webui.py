# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import importlib
import shutil
import time
from pathlib import Path

import numpy as np
import streamlit as st

from knowledge_qa_llm.encoder import EncodeText
from knowledge_qa_llm.file_loader import FileLoader
from knowledge_qa_llm.utils import get_timestamp, logger, make_prompt, mkdir, read_yaml
from knowledge_qa_llm.vector_utils import DBUtils

config = read_yaml("knowledge_qa_llm/config.yaml")

st.set_page_config(
    page_title=config.get("title"),
    page_icon=":robot:",
)


def init_sidebar():
    st.sidebar.markdown("### 🛶 Parameter Settings")
    param = config.get("Parameter")

    param_max_length = param.get("max_length")
    max_length = st.sidebar.slider(
        "max_length",
        min_value=param_max_length.get("min_value"),
        max_value=param_max_length.get("max_value"),
        value=param_max_length.get("default"),
        step=param_max_length.get("step"),
        help=param_max_length.get("tip"),
    )

    st.session_state["params"] = {}
    st.session_state["params"]["max_length"] = max_length

    param_top = param.get("top_p")
    top_p = st.sidebar.slider(
        "top_p",
        min_value=param_top.get("min_value"),
        max_value=param_top.get("max_value"),
        value=param_top.get("default"),
        step=param_top.get("step"),
        help=param_top.get("tip"),
    )
    st.session_state["params"]["top_p"] = top_p

    param_temp = param.get("temperature")
    temperature = st.sidebar.slider(
        "temperature",
        min_value=param_temp.get("min_value"),
        max_value=param_temp.get("max_value"),
        value=param_temp.get("default"),
        step=param_temp.get("stemp"),
        help=param_temp.get("tip"),
    )
    st.session_state["params"]["temperature"] = temperature

    st.sidebar.markdown("### 🧻 Knowledge DataBase")
    uploaded_files = st.sidebar.file_uploader(
        "default",
        accept_multiple_files=True,
        label_visibility="hidden",
        help="Support for multiple selections",
    )

    upload_dir = config.get("upload_dir")
    btn_upload = st.sidebar.button("Upload and load database", use_container_width=True)
    if btn_upload:
        time_stamp = get_timestamp()
        save_dir = Path(upload_dir) / time_stamp
        st.session_state["upload_dir"] = save_dir

        tips("Uploading files to platform...", icon="⏳")
        for file in uploaded_files:
            bytes_data = file.getvalue()

            mkdir(save_dir)
            save_path = save_dir / file.name
            with open(save_path, "wb") as f:
                f.write(bytes_data)
        tips("Upload completed！")

        doc_dir = st.session_state["upload_dir"]
        all_doc_contents = file_loader(doc_dir)

        pro_text = "Extracting embeddings..."
        batch_size = config.get("encoder_batch_size", 32)
        for file_path, one_doc_contents in all_doc_contents.items():
            my_bar = st.sidebar.progress(0, text=pro_text)
            content_nums = len(one_doc_contents)
            all_embeddings = []
            for i in range(0, content_nums, batch_size):
                start_idx = i
                end_idx = start_idx + batch_size
                end_idx = content_nums if end_idx > content_nums else end_idx
                embeddings = embedding_extract(one_doc_contents[start_idx:end_idx])
                all_embeddings.append(embeddings)

                my_bar.progress(
                    end_idx / content_nums,
                    f"Extract {file_path} datas: [{end_idx}/{content_nums}]",
                )
            my_bar.empty()
            all_embeddings = np.vstack(all_embeddings)
            db_tools.insert(file_path, all_embeddings, one_doc_contents)
        my_bar.empty()

        shutil.rmtree(doc_dir.resolve())
        tips("You can now ask a question!")

    had_files = db_tools.get_files()
    if had_files:
        st.sidebar.markdown("Existing documents:")
        st.sidebar.markdown("\n".join([f" - {v}" for v in had_files]))


def init_state():
    if "history" not in st.session_state:
        st.session_state["history"] = []

    if "openai_state" not in st.session_state:
        st.session_state["openai_state"] = []

    if "input_txt" not in st.session_state:
        st.session_state["input_txt"] = ""


@st.cache_resource
def init_encoder(model_path: str):
    return EncodeText(model_path)


def predict(
    text,
    model,
    custom_prompt=None,
):
    logger.info(f"Using {type(model).__name__}")

    query_embedding = embedding_extract(text)
    with st.spinner("Search for relevant contents from docs..."):
        search_res, search_elapse = db_tools.search_local(
            query_embedding, top_k=search_top
        )
    if search_res is None:
        bot_print("The results of searching from docs is empty.")
    else:
        res_cxt = f"**Find Top{search_top}\n(Scores from high to low，cost:{search_elapse:.5f}s):** \n"
        bot_print(res_cxt)

        for file, content in search_res.items():
            content = "\n".join(content)
            one_context = f"**From：《{file}》** \n{content}"
            bot_print(one_context)

            logger.info(f"Context：\n{one_context}\n")

        context = "\n".join(sum(search_res.values(), []))
        response, elapse = get_model_response(text, context, custom_prompt, model)
        print_res = f"**Use：{select_model}**\n**Infer model cost：{elapse:.5f}s**"
        bot_print(print_res)
        bot_print(response)


def bot_print(content):
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in content.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)


def get_model_response(text, context, custom_prompt, model):
    params_dict = st.session_state["params"]

    s_model = time.perf_counter()
    prompt_msg = make_prompt(text, context, custom_prompt)
    logger.info(f"Final prompt: \n{prompt_msg}\n")

    response = model(prompt_msg, history=None, **params_dict)
    elapse = time.perf_counter() - s_model

    logger.info(f"Reponse of LLM: \n{response}\n")
    if not response:
        response = "Sorry, I didn't answer the question correctly"
    return response, elapse


def tips(txt: str, wait_time: int = 2, icon: str = "🎉"):
    st.toast(txt, icon=icon)
    time.sleep(wait_time)


if __name__ == "__main__":
    title = config.get("title")
    version = config.get("version", "0.0.1")
    st.markdown(
        f"<h3 style='text-align: center;'>{title} v{version}</h3><br/>",
        unsafe_allow_html=True,
    )

    file_loader = FileLoader()

    db_path = config.get("vector_db_path")
    db_tools = DBUtils(db_path)

    llm_module = importlib.import_module("knowledge_qa_llm.llm")
    MODEL_OPTIONS = {
        name: getattr(llm_module, name)(api)
        for name, api in config.get("LLM_API").items()
    }

    online_llm_api = config.get("OnlineLLMAPI", None)
    if online_llm_api:
        MODEL_OPTIONS.update(
            {
                name: getattr(llm_module, name)(**params)
                for name, params in online_llm_api.items()
            }
        )

    TOP_OPTIONS = [5, 10, 15]
    ENCODER_OPTIONS = config.get("Encoder")

    menu_col1, menu_col2, menu_col3 = st.columns([1, 1, 1])
    select_model = menu_col1.selectbox("🎨Base model:", MODEL_OPTIONS.keys())
    select_encoder = menu_col2.selectbox(
        "🧬Extract Embedding Model:", ENCODER_OPTIONS.keys()
    )
    search_top = menu_col3.selectbox("🔍Search Top_K:", TOP_OPTIONS)

    embedding_extract = init_encoder(ENCODER_OPTIONS[select_encoder])

    init_sidebar()
    init_state()

    input_prompt_container = st.container()
    with input_prompt_container:
        with st.expander("💡Prompt", expanded=False):
            text_area = st.empty()
            input_prompt = text_area.text_area(
                label="Input",
                max_chars=500,
                height=200,
                label_visibility="hidden",
                value=config.get("DEFAULT_PROMPT"),
                key="input_prompt",
            )

    input_txt = st.chat_input("What is up?")
    if input_txt:
        with st.chat_message("user", avatar="😀"):
            st.markdown(input_txt)

        llm = MODEL_OPTIONS[select_model]

        if not input_prompt:
            input_prompt = config.get("DEFAULT_PROMPT")

        predict(
            input_txt,
            llm,
            input_prompt,
        )
