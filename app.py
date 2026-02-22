import streamlit as st
from datetime import datetime
import json
import os
import glob
import time
from http import HTTPStatus
from dashscope import Application
from dotenv import load_dotenv
# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')
# 强制加载
load_dotenv(dotenv_path=env_path, override=True)
#定义删除会话的操作
def handle_session(current_time):
    # 本地.json文件存在，则删除会话信息。清空session_state
    if os.path.exists(f"resource/data/{current_time}.json"):
        os.remove(f"resource/data/{current_time}.json")
        st.session_state.current_time = ""
        st.session_state.messages = []

# 加载会话信息
def load_session(current_time):
    # 加载会话信息。保存信息到session_state
    if os.path.exists(f"resource/data/{current_time}.json"):
        with open(f"resource/data/{current_time}.json", 'r', encoding='utf-8') as current_file:
            json_data = json.load(current_file)
            st.session_state.current_time = json_data["current_time"]
            st.session_state.messages = json_data["messages"]

#开启新会话，需要保存历史对话信息
def new_session(current_time,messages):
    #用时间定义唯一标识。保存历史会话到json文件
    new_time = datetime.now().strftime("%Y%m%d%H%M%S")
    if current_time and messages and current_time != new_time:
        history_messages = {
            "current_time": current_time,
            "messages": messages
        }
        # 确保目录存在
        os.makedirs("resource/data", exist_ok=True)
        with open(f"resource/data/{current_time}.json", 'w', encoding='utf-8') as history_file:
            json.dump(history_messages, history_file, ensure_ascii=False, indent=4)

    # 初始化聊天消息
    st.session_state.messages = []
    st.session_state.current_time = new_time

#设置页面的配置项。标题，图标，页面布局。
st.set_page_config(
    page_title="AI聊天伴侣",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    }
)

#页面logo
st.logo("resource/logo.jpeg")

#AI聊天伴侣。标题
st.title("今天有什么可以帮到你？",text_alignment="center")

# 程序重载记录当前会话
if 'messages' not in st.session_state:
    st.session_state.messages = []
# 记录当前时间
if 'current_time' not in st.session_state:
    st.session_state.current_time = datetime.now().strftime("%Y%m%d%H%M%S")

#存在历史会话，需要展示历史信息
if st.session_state.messages:
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

#用户提问，调用大语言模型LLM（阿里云百炼平台API）
prompt = st.chat_input(placeholder="请输入您想咨询的问题")
if prompt:
    #展示用户输入的信息
    st.chat_message("user").write(prompt)

    #保存用户信息
    st.session_state.messages.append({"role":"user","content":prompt})

    # 调用大模型。参数：密钥，应用ID，提示词，是否流式输出。
    responses = Application.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        app_id='db7c5025954e41a7a75384c7db9be83a',
        prompt=prompt,
        stream=True,# 流式输出
        incremental_output=True
    )

    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # 创建占位符，用于实时更新
        #记录开始时间
        start_time = time.time()
        # 1. 立即显示"正在输入..."提示
        message_placeholder.markdown(f"⏳ 正在思考...")
        full_response = ""  # 用于拼接完整文本
        has_received = False
        last_update_time = time.time()
        try:
            #遍历消息
            for chunk in responses:
                #无效KEY访问。
                if chunk.status_code == HTTPStatus.UNAUTHORIZED:
                    full_response = "API_KEY未授权，检查配置信息"
                    break
                current_time = time.time()
                # 每秒更新一次显示（避免过度刷新）
                if int(current_time - start_time) > int(last_update_time - start_time):
                    elapsed_seconds = int(current_time - start_time)
                    if not has_received:

                        message_placeholder.markdown(f"⏳ 正在思考 {elapsed_seconds} 秒...")
                    last_update_time = current_time
                # 请求成功状态码200，返回数据
                if chunk.status_code == HTTPStatus.OK:
                    data = chunk.output.text
                    if data:
                        if not has_received:
                            # 第一次收到数据，清除"正在输入"提示
                            has_received = True
                            message_placeholder.markdown("")  # 清空
                        full_response  += data
                        # 实时更新显示（加光标效果）
                        message_placeholder.markdown(full_response + "▌")
        except Exception as e:
            error_msg = f"调用异常: {str(e)}"
            message_placeholder.markdown(f"❌ {error_msg}")
            full_response = error_msg

        # 流式结束后，去掉光标，显示完整文本
        final_elapsed = int(time.time() - start_time)
        if final_elapsed > 0 and not has_received:
            # 如果没有收到任何数据，显示最终等待时间
            message_placeholder.markdown(f"⏳ 等待结束 ({final_elapsed} 秒)\n\n{full_response}")
        else:
            message_placeholder.markdown(full_response)

        #保存大模型返回的信息
        st.session_state.messages.append({"role": "assistant", "content": full_response})

#侧边栏逻辑处理
with st.sidebar:
    st.subheader("AI聊天伴侣")
    # 侧边栏，开启新对话。重新加载程序执行new_session函数，传入参数args
    st.button("开启新对话",
              key="new_chat",
              width="stretch",
              icon="✏️",
              on_click=new_session,
              args=(st.session_state.current_time,st.session_state.messages)
              )
    # 侧边栏有历史消息，展示出来
    json_files = glob.glob(os.path.join("resource/data/", '*.json'))
    if json_files:
        st.text("会话信息")
        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            col1,col2 = st.columns([4,1])
            with col1:
                # 需要展示单个会话信息
                st.button(
                    data["current_time"],
                    on_click=load_session,
                    width = "stretch",
                    key=data["current_time"],
                    args=(data["current_time"],)
                )
            with col2:
                st.button(
                    "",
                    icon="❌️",
                    key=f"❌️{data["current_time"]}",
                    width="stretch",
                    on_click=handle_session,
                    args=(data["current_time"],)
                )