# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import time
from pathlib import Path

import streamlit as st
from streamlit_chat import message

from config import DEFAULT_PROMPT
from llm import ChatGLM26B
from llm.utils import make_prompt
from vector_utils import DBUtils, EncodeText

st.set_page_config(
    page_title="QA-LocalKnowledge-LLM",
    page_icon=":robot:",
    initial_sidebar_state="collapsed",
)


def init_sidebar():
    st.sidebar.title("🛠参数设置")
    max_length = st.sidebar.slider(
        "max_length",
        min_value=0,
        max_value=4096,
        value=1024,
        step=1,
        help="输入input_ids的最大长度",
    )

    st.session_state["params"] = {}
    st.session_state["params"]["max_length"] = max_length

    top_p = st.sidebar.slider(
        "top_p",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.01,
        help="限制模型为仅考虑最可能的前p个标记",
    )
    st.session_state["params"]["top_p"] = top_p

    temperature = st.sidebar.slider(
        "temperature",
        min_value=0.01,
        max_value=1.0,
        value=0.01,
        step=0.01,
        help="控制模型输出的随机性，温度越低将导致输出更加可预测和重复，越高将更富创意和自发的输出。",
    )
    st.session_state["params"]["temperature"] = temperature


def init_state():
    if "state" not in st.session_state:
        st.session_state["state"] = []

    if "openai_state" not in st.session_state:
        st.session_state["openai_state"] = []

    if "input_txt" not in st.session_state:
        st.session_state["input_txt"] = ""


def predict_only_llm(text, model, history=[]):
    params_dict = st.session_state["params"]

    print(f"Using {type(model).__name__}")

    with chat_container:
        if len(history) > 0:
            for i, (query, response) in enumerate(history):
                message(query, avatar_style="avataaars", key=f"{i}_user", is_user=False)
                message(response, avatar_style="bottts", key=f"{i}")

        message(
            input_txt,
            avatar_style="avataaars",
            key=f"{len(history)}_user",
            is_user=False,
        )

        with st.spinner("正在梳理内容，请稍等........"):
            with chat_empty:
                if len(input_txt) <= 0:
                    message("问题为空", avatar_style="bottts", key=f"{len(history) + 1}")
                else:
                    s_model = time.perf_counter()
                    response = model(text, history=history, **params_dict)
                    model_elapse = time.perf_counter() - s_model

                    print(f"model response: {response}\n")
                    if not response:
                        response = "抱歉，未能正确回答该问题"

                    history.append([input_txt, response])
                    print_res = f"**使用模型：{select_model}**\n**模型推理耗时：{model_elapse:.5f}s** \n\n{response}"
                    message(print_res, avatar_style="bottts", key=f"{len(history) + 1}")
    st.session_state["state"] = history


def predict(
    text,
    model,
    custom_prompt=None,
    history=[],
):
    params_dict = st.session_state["params"]

    print(f"Using {type(model).__name__}")

    with chat_container:
        if len(history) > 0:
            for i, (query, response) in enumerate(history):
                message(query, avatar_style="avataaars", key=f"{i}_user", is_user=False)
                message(response, avatar_style="bottts", key=f"{i}")

        message(
            input_txt,
            avatar_style="avataaars",
            key=f"{len(history)}_user",
            is_user=False,
        )

        print('提取问题的embedding')
        query_embedding = embedding_extract(text)

        s_context = time.perf_counter()
        with st.spinner("从文档中搜索相关内容"):
            context, which_file = db_tools.search_local(query_embedding)
        context_elapse = time.perf_counter() - s_context
        res_cxt = f"**从文档中检索到的相关内容Top5\n(相关性从高到低，耗时:{context_elapse:.5f}s):** \n\n"
        res_cxt += f'**来自{Path(str(which_file[0])).name}**\n\n{context}'
        print(context)
        message(res_cxt, avatar_style="bottts", key=f"{len(history)}_context")

        with st.spinner("正在梳理内容，请稍等........"):
            with chat_empty:
                if len(input_txt) <= 0:
                    message("问题为空", avatar_style="bottts", key=f"{len(history) + 1}")
                elif len(context) <= 0:
                    message(
                        "从文档中搜索相关内容为空，暂不能回答该问题",
                        avatar_style="bottts",
                        key=f"{len(history) + 1}",
                    )
                else:
                    s_model = time.perf_counter()
                    prompt_msg = make_prompt(text, context, custom_prompt)
                    print(f"最终拼接后的文本：\n{prompt_msg}\n")

                    response = model(prompt_msg, history=history, **params_dict)
                    model_elapse = time.perf_counter() - s_model

                    print(f"model response: {response}\n")
                    if not response:
                        response = "抱歉，未能正确回答该问题"

                    history = [[input_txt, response]]
                    print_res = f"**使用模型：{select_model}**\n**模型推理耗时：{model_elapse:.5f}s** \n\n{response}"
                    message(print_res, avatar_style="bottts", key=f"{len(history) + 1}")
    st.session_state["state"] = history


def tips(txt: str, tips_empty=None, wait_time=2):
    if tips_empty is None:
        tips_empty = st.empty()

    tips_empty.success(txt)
    time.sleep(wait_time)
    tips_empty.empty()


def clear_history():
    st.session_state["state"] = []


if __name__ == "__main__":
    db_tools = DBUtils('db/Vector.db')
    embedding_extract = EncodeText()

    chatglm26b = ChatGLM26B()

    init_sidebar()
    init_state()

    version = "0.0.1"
    st.markdown(
        f"<h3 style='text-align: center;'>QA-LocalKnowledge-LLM v{version}</h3><br/>",
        unsafe_allow_html=True,
    )

    MODEL_OPTIONS = {
        "ChatGLM2-6B": chatglm26b,
    }

    PLUGINS_OPTIONS = {
        "文档": 3,
        "模型本身": 0,
    }

    menu_col1, menu_col2 = st.columns([5, 5])
    select_model = menu_col1.selectbox("🎨基础模型：", MODEL_OPTIONS.keys())
    select_plugin = menu_col2.selectbox("🛠Plugin：", PLUGINS_OPTIONS.keys())

    chat_container = st.container()
    chat_empty = st.empty()
    input_prompt_container = st.container()
    input_container = st.container()
    tips_empty = input_container.empty()

    with input_prompt_container:
        with st.expander("💡Prompt", expanded=False):
            text_area = st.empty()
            input_prompt = text_area.text_area(
                label="输入",
                max_chars=500,
                height=200,
                label_visibility="hidden",
                value=DEFAULT_PROMPT,
                key="input_prompt",
                disabled=True,
            )

    with input_container:
        input_txt = st.text_area(
            label="😃 You:",
            max_chars=2000,
            height=150,
            placeholder="请在这儿输入您的问题",
            label_visibility="collapsed",
            key="input_txt",
        )
        col1, col2, col3, _, _ = st.columns([1, 1, 1, 1, 1], gap="small")
        btn_send = col1.button("发  送", key="btn_send")
        btn_stop = col2.button("停止生成")
        btn_clear = col3.button("清除历史")

    if btn_send:
        plugin_id = PLUGINS_OPTIONS[select_plugin]
        llm = MODEL_OPTIONS[select_model]

        if not input_prompt:
            input_prompt = DEFAULT_PROMPT

        if plugin_id == 3:
            clear_history()

            predict(
                input_txt,
                llm,
                input_prompt,
                st.session_state["state"],
            )
        elif plugin_id == 0:
            tips("该插件下，定制prompt功能将会失效", tips_empty, 1.5)
            predict_only_llm(input_txt, llm, st.session_state["state"])

    if btn_clear:
        clear_history()
