# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path

import faiss
import numpy as np
import streamlit as st
from streamlit_chat import message

from chat_glm import ChatGLM
from extract_vector import ExtractVector
from read_file import read_txt
from search_vector import SearchVector


st.set_page_config(
    page_title="QA-LocalKnowledge-ChatGLM",
    page_icon=":robot:"
)

MAX_TURNS = 20
MAX_BOXES = MAX_TURNS * 2


@st.cache_resource
def get_llm():
    model_dir = 'models/chatglm-6b-series/chatglm-6b-int4'
    chat_glm = ChatGLM(model_dir)
    return chat_glm.tokenizer, chat_glm.model


@st.cache_resource
def get_tokenizer_model():
    model_path = './models/text2vec-base-chinese'
    return ExtractVector(model_path)


@st.cache_resource
def get_searcher():
    return SearchVector('embeddings')


def predict(input, max_length, top_p, temperature, history=None):
    if history is None:
        history = []

    with container:
        if len(history) > 0:
            for i, (query, response) in enumerate(history):
                message(query, avatar_style="big-smile", key=str(i) + "_user")
                message(response, avatar_style="bottts", key=str(i))

        message(input, avatar_style="big-smile",
                key=str(len(history)) + "_user")
        st.write("AI正在回复:")
        with st.empty():
            for response, history in model.stream_chat(tokenizer, input,
                                                       history,
                                                       max_length=max_length,
                                                       top_p=top_p,
                                                       temperature=temperature):
                query, response = history[-1]
                st.write(response)
    return history


tokenizer, model = get_llm()
extracter = get_tokenizer_model()
searcher = get_searcher()

max_length = st.sidebar.slider('max_length', 0, 4096, 2048, step=1)
top_p = st.sidebar.slider('top_p', 0.0, 1.0, 0.6, step=0.01)
temperature = st.sidebar.slider('temperature', 0.0, 1.0, 0.95, step=0.01)

container = st.container()
prompt_text = st.text_area(label="用户命令输入", height=100,
                           placeholder="请在这儿输入您的命令")
if 'state' not in st.session_state:
    st.session_state['state'] = []

btn_res = st.button("发送", key="predict_btn")
uploaded_file = st.file_uploader("点击上传文件")

save_dir = 'upload_files'
if uploaded_file is not None:
    file_contents = uploaded_file.getvalue()
    file_name = uploaded_file.name
    save_path = Path(save_dir) / file_name
    with open(str(save_path), 'wb') as f:
        f.write(file_contents)

    if Path(file_name).suffix == '.txt':
        sentences = read_txt(save_path)
        save_dir = 'embeddings'
        embeddings = extracter.encode(sentences, save_dir, file_name=file_name)
        search_index = faiss.IndexFlatIP(embeddings.shape[1])
        search_index.add(embeddings)
        sentences = np.array(sentences)

if btn_res:
    with st.spinner("AI正在思考，请稍等........"):
        embedding_query = extracter.encode(prompt_text)
        prompt_text = searcher(prompt_text, embedding_query)
        st.session_state["state"] = predict(prompt_text, max_length,
                                            top_p, temperature,
                                            st.session_state["state"])
