# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import time
from pathlib import Path

import streamlit as st
from streamlit_chat import message

from llm import ChatGLM26B
from utils import make_prompt, read_yaml
from vector_utils import DBUtils, EncodeText

config = read_yaml("config.yaml")


st.set_page_config(
    page_title="QA-LocalKnowledge-LLM",
    page_icon=":robot:",
    initial_sidebar_state="collapsed",
)


def init_sidebar():
    st.sidebar.title("🛠参数设置")
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
        value=param_top.get("value"),
        step=param_top.get("step"),
        help=param_top.get("tip"),
    )
    st.session_state["params"]["top_p"] = top_p

    param_temp = param.get("temperature")
    temperature = st.sidebar.slider(
        "temperature",
        min_value=param_temp.get("min_value"),
        max_value=param_temp.get("max_value"),
        value=param_temp.get("value"),
        step=param_temp.get("stemp"),
        help=param_temp.get("tip"),
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

        print("提取问题的embedding")
        query_embedding = embedding_extract(text)

        s_context = time.perf_counter()
        with st.spinner("从文档中搜索相关内容"):
            context, which_file = db_tools.search_local(query_embedding)
        context_elapse = time.perf_counter() - s_context
        res_cxt = f"**从文档中检索到的相关内容Top5\n(相关性从高到低，耗时:{context_elapse:.5f}s):** \n\n"
        res_cxt += f"**来自{Path(str(which_file[0])).name}**\n\n{context}"
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
    db_tools = DBUtils(config["vector_db_path"])
    embedding_extract = EncodeText()
    chatglm26b = ChatGLM26B(config["llm_api_url"])

    init_sidebar()
    init_state()

    version = config.get("version", "0.0.1")
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
                value=config.get("DEFAULT_PROMPT"),
                key="input_prompt",
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
