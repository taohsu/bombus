import streamlit as st
import requests
import json


def extract_final_answer(response):
    """
    从响应中提取Final Answer后的内容

    Args:
        response (dict): API响应的JSON数据

    Returns:
        str: Final Answer后的内容
    """
    try:
        content = response['choices'][0]['message']['content']
        final_answer_marker = "\nFinal Answer: "
        start_index = content.find(final_answer_marker)

        if start_index != -1:
            extracted_content = content[start_index + len(final_answer_marker):]
            return extracted_content.strip()
        return "未找到Final Answer"
    except (KeyError, IndexError) as e:
        return f"提取错误: {str(e)}"


def llm_api(prompt):
    """
    调用LLM chat API endpoint
    """
    url = 'http://39.153.220.86:5000/agent/chat'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'prompt': prompt
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"请求出错: {e}")
        return None


def main():

    # 初始化聊天历史
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 显示聊天历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 接收用户输入
    if user_query := st.chat_input("请输入您的问题"):
        # 添加用户消息到聊天历史
        st.session_state.messages.append({"role": "user", "content": user_query})

        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(user_query)

        # 获取AI响应
        with st.chat_message("assistant"):
            response = llm_api(user_query)
            if response:
                llm_response = extract_final_answer(response)
                st.markdown(llm_response)
                # 添加助手响应到聊天历史
                st.session_state.messages.append({"role": "assistant", "content": llm_response})


if __name__ == "__main__":
    main()