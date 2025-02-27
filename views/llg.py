
# app01/views/llg.py

from django.shortcuts import render, redirect
import time
import jwt
import requests


# ask_glm 函数
def ask_glm(key, model, max_tokens, temperature, content):
    url = "https://openai.api2d.net/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key
    }

    data = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": content
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()


# 视图函数
def llg_connect(request):
    # 从 session 中获取 API Token，如果没有则为空
    key = request.session.get('API_TOKEN', '')

    # 如果没有 Token，则检查 POST 请求中的 token 参数
    if not key and 'token' in request.POST:
        key = request.POST.get('token')
        request.session['API_TOKEN'] = key  # 保存 token 到 session

    # 如果仍然没有 Token，返回错误信息
    if not key:
        return render(request, 'llg_connect.html', {
            'error': 'API Token is required!',  # 提示用户 Token 缺失
        })

    # 初始化对话历史（如果尚未初始化）
    if 'messages' not in request.session:
        request.session['messages'] = [{"role": "assistant", "content": "你好，我是ChatGLM，有什么可以帮你？"}]

    if request.method == 'POST':
        model = request.POST.get('model', 'glm-3-turbo')
        max_tokens = int(request.POST.get('max_tokens', 512))
        temperature = float(request.POST.get('temperature', 0.8))

        # 获取用户输入的 prompt
        if 'prompt' in request.POST:
            prompt = request.POST.get('prompt')
            request.session["messages"].append({"role": "user", "content": prompt})

            # 调用 API 获取响应
            response_json = ask_glm(key, model, max_tokens, temperature, request.session["messages"])

            if "choices" in response_json and len(response_json["choices"]) > 0:
                full_response = response_json['choices'][0]['message']['content']
                request.session["messages"].append({"role": "assistant", "content": full_response})
            else:
                request.session["messages"].append({"role": "assistant", "content": "抱歉，没有收到有效的回复。"})

    # 渲染模板
    return render(request, 'llg_connect.html', {
        'messages': request.session.get("messages", []),
        'token': key,
    })


"""# app01/views/llg.py
from django.shortcuts import render, redirect
import time
import jwt
import requests

# 生成 Token
def generate_token(apikey: str, exp_seconds: int):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)

    payload = {
        "api_key": id,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
        "timestamp": int(round(time.time() * 1000)),
    }
    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )

def ask_glm(key, model, max_tokens, temperature, content):
    url = "https://openai.api2d.net/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key
    }

    data = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": content
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# 视图函数，用于渲染连接页面
def llg_connect(request):
    key = ""
    if 'API_TOKEN' in request.session and len(request.session['API_TOKEN']) > 1:
        key = request.session['API_TOKEN']

    if request.method == 'POST':
        # 获取表单数据
        key = request.POST.get('token')
        model = request.POST.get('model', 'glm-3-turbo')
        max_tokens = int(request.POST.get('max_tokens', 512))
        temperature = float(request.POST.get('temperature', 0.8))

        # 将 token 存入 session
        request.session['API_TOKEN'] = key

        # 初始化对话历史
        if "messages" not in request.session:
            request.session["messages"] = [{"role": "assistant", "content": "你好，我是ChatGLM，有什么可以帮你？"}]

        if key:
            if 'prompt' in request.POST:
                prompt = request.POST.get('prompt')
                request.session["messages"].append({"role": "user", "content": prompt})

                # 调用 API 获取响应
                response_json = ask_glm(key, model, max_tokens, temperature, request.session["messages"])

                if "choices" in response_json and len(response_json["choices"]) > 0:
                    full_response = response_json['choices'][0]['message']['content']
                    request.session["messages"].append({"role": "assistant", "content": full_response})
                else:
                    request.session["messages"].append({"role": "assistant", "content": "抱歉，没有收到有效的回复。"})

        # 渲染模板
        return render(request, 'llg_connect.html', {
            'messages': request.session.get("messages", []),
            'token': key,
            'model': model,
            'max_tokens': max_tokens,
            'temperature': temperature,
        })
    else:
        # 处理 GET 请求时，直接返回当前页面
        return render(request, 'llg_connect.html', {
            'messages': request.session.get("messages", []),
            'token': key,
        })"""



"""from django.shortcuts import render, redirect
from app01 import models
import time
import jwt
import requests


# 生成 Token
def generate_token(apikey: str, exp_seconds: int):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)

    payload = {
        "api_key": id,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
        "timestamp": int(round(time.time() * 1000)),
    }
    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )


def ask_glm(key, model, max_tokens, temperature, content):
    url = "https://openai.api2d.net/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key
    }

    data = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": content
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()


# 视图函数，用于渲染连接页面
def llg_connect(request):
    # 处理 Token
    key = ""
    if 'API_TOKEN' in request.session and len(request.session['API_TOKEN']) > 1:
        key = request.session['API_TOKEN']

    if request.method == 'POST':
        # 获取表单数据
        key = request.POST.get('token')
        model = request.POST.get('model', 'glm-3-turbo')
        max_tokens = int(request.POST.get('max_tokens', 512))
        temperature = float(request.POST.get('temperature', 0.8))

        # 将 token 存入 session
        request.session['API_TOKEN'] = key

        # 初始化对话历史
        if "messages" not in request.session:
            request.session["messages"] = [{"role": "assistant", "content": "你好，我是ChatGLM，有什么可以帮你？"}]

        if key:
            if 'prompt' in request.POST:
                prompt = request.POST.get('prompt')
                request.session["messages"].append({"role": "user", "content": prompt})

                # 调用 API 获取响应
                response_json = ask_glm(key, model, max_tokens, temperature, request.session["messages"])

                if "choices" in response_json and len(response_json["choices"]) > 0:
                    full_response = response_json['choices'][0]['message']['content']
                    request.session["messages"].append({"role": "assistant", "content": full_response})
                else:
                    request.session["messages"].append({"role": "assistant", "content": "抱歉，没有收到有效的回复。"})

        # 渲染模板
        return render(request, 'llg_connect.html', {
            'messages': request.session.get("messages", []),
            'token': key,
            'model': model,
            'max_tokens': max_tokens,
            'temperature': temperature,
        })
    else:
        # 处理 GET 请求时，直接返回当前页面
        return render(request, 'llg_connect.html', {
            'messages': request.session.get("messages", []),
            'token': key,
        })"""



""""import streamlit as st
import os
import time
import jwt
import requests


# 实际KEY 过期时间
def generate_token(apikey: str, exp_seconds: int):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)

    payload = {
        "api_key": id,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
        "timestamp": int(round(time.time() * 1000)),
    }
    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )


def ask_glm(key, model, max_tokens, temperature, content):
    url = "https://openai.api2d.net/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',  # 注意修正拼写错误
        'Authorization': 'Bearer ' + key
    }

    data = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": content
    }

    response = requests.post(url, headers=headers, json=data)

    # 确保 API 返回的 JSON 格式被正确解析
    return response.json()


st.set_page_config(page_title="聊天机器人")

with st.sidebar:
    st.title('通过API与大模型的对话')

    # 从session_state获取API token，允许用户输入
    if 'API_TOKEN' in st.session_state and len(st.session_state['API_TOKEN']) > 1:
        st.success('API Token已经配置', icon="✅")
        key = st.session_state['API_TOKEN']
    else:
        key = ""

        # 用户输入API Token
    key = st.text_input('输入Token:', type='password', value=key)
    st.session_state['API_TOKEN'] = key

    # 选择模型
    model = st.sidebar.selectbox("选择模型", ['glm-3-turbo', 'glm-4'])

    # 设置max_tokens和temperature
    max_tokens = st.sidebar.slider("max_tokens", 0, 2000, value=512)
    temperature = st.sidebar.slider("temperature", 0.0, 2.0, value=0.8)

# 初始化的对话
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "你好，我是ChatGLM，有什么可以帮你？"}]

# 显示聊天记录
for messages in st.session_state.messages:
    with st.chat_message(messages["role"]):
        st.write(messages["content"])


# 清空聊天记录
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "你好，我是ChatGLM，有什么可以帮你？"}]


st.sidebar.button('清空聊天记录', on_click=clear_chat_history)

# 如果API Token存在
if len(key) > 1:
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("请求中..."):
                # 调用 API 获取响应
                response_json = ask_glm(key, model, max_tokens, temperature, st.session_state.messages)

                # 确保检查返回的 JSON 格式
                if "choices" in response_json and len(response_json["choices"]) > 0:
                    # 从返回的 JSON 中获取模型的回复
                    full_response = response_json['choices'][0]['message']['content']
                    st.markdown(full_response)

                    # 将模型的回答添加到对话历史中
                    messages = {"role": "assistant", "content": full_response}
                    st.session_state.messages.append(messages)
                else:
                    st.markdown("抱歉，没有收到有效的回复。")"""

"""import streamlit as st
import os
import time
import jwt
import requests

# 实际KEY 过期时间
def generate_token(apikey: str, exp_seconds: int):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)

    payload = {
        "api_key": id,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
        "timestamp": int(round(time.time() * 1000)),

    }
    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},

    )
"""

"""def ask_glm(key, model, max_tokens, temperature, content):
    url = "https://openai.api2d.net/v1/chat/completions"
    headers = {
        'Cotnet-Type': 'application/json',
        'Autorization':  'Bearer ' + key
    }

    data = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": content

    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()


st.set_page_config(page_title="聊天机器人")

with st.sidebar:
    st.title('通过API与大模型的对话')
    if 'API_TOKEN' in st.session_state and len(st.session_state['API_TOKEN']) > 1:
        st.success('API Token已经配置', icon="✅")
        key = st.session_state['API_TOKEN']
    else:
        key = ""

    key = st.text_input('输入Token:', type='password', value=key)

    st.session_state['API_TOKEN'] = key

    model = st.sidebar.selectbox("选择模型", ['glm-3-turbo', 'glm-4'])
    max_tokens = st.sidebar.slider("max_tokens", 0, 2000, value=512)
    temperature = st.sidebar.slider("temperature", 0.0, 2.0, value=0.8)

# 初始化的对话
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "你好我是ChatGLM, 有什么可以帮你"}]

for messages in st.session_state.messages:
    with st.chat_message(messages["role"]):
        st.write(messages["content"])


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "你好我是ChatGLM, 有什么可以帮你"}]


st.sidebar.button('清空聊天记录', on_click=clear_chat_history())

if len(key) > 1:
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("请求中..."):
                full_response = \
                ask_glm(key, model, max_tokens, temperature, st.session_state.messages)['choices'][0]['messages'][
                    'content']
                st.markdown(full_response)

                messages = {"role": "assistant", "content": full_response}
                st.session_state.messages.append(messages)
prompt = st.chat_input()"""

"""st.sidebar.header('大模型聊天页面')
key = st.sidebar.text_input('输入token')
model = st.sidebar.selectbox("选择模型", ['glm-3-turbo', 'glm-4'])
max_tokens = st.sidebar.slider("max_tokens", 0, 2000, value=512)
temperature = st.sidebar.slider("temperature", 0.0, 2.0, value=0.8)


st.session_state.messages = [
    {"role":"assistant", "content":"你好我是ChatGlm,有什么可以帮助你？"}
]

for messages in st.session_state.messages:
    with st.chat_message(messages["role"]):
        st.write(messages["content"])

prompt = st.chat_input()"""
