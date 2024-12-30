import streamlit as st
from datetime import datetime, date
import requests
import json
import datetime
import uuid

# Initialize session state for screen management
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'main'
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to switch screen
def switch_to_question():
    st.session_state.current_screen = 'question'


def switch_to_main():
    st.session_state.current_screen = 'main'

# API for LLM
def llm_api(prompt):
    """
    call API & get response
    """
    url = "http://39.101.77.102:8000/chat"

    # prompt data
    prompts = [{
        "role": "user",
        "content": prompt
    }]

    # create request
    files = {
        'prompts': (None, json.dumps(prompts))
    }

    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text

    except requests.exceptions.RequestException as e:
        st.error(f"LLM API请求出错: {e}")
        return None


def render_list_item(date_str, title, content, data, show_button=True):
    unique_key = str(uuid.uuid4())[:8]
    if isinstance(data, str):
        data = json.loads(data)

    # card
    with st.container():
        card_html = f"""
        <div class="card-container">
            <p class="date-text">{date_str}</p>
            <h5 class="title-text">{title}</h5>
            <p class="content-text">{content}</p>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

        # display chart
        col1, col2 = st.columns(2)

        # chart data
        if data and isinstance(data, dict):
            # chart 1
            if 'irrigation' in data:
                irrigation_data = {
                    '日期': [item['time'][5:] for item in data['temperature']],  # 只取日期的天数
                    '灌溉量': [item['value'] for item in data['irrigation']]
                }
                with col1:
                    st.caption('灌溉量')
                    st.bar_chart(
                        irrigation_data,
                        y='灌溉量',
                        x='日期',
                        use_container_width=True
                    )

            # chart 2
            if 'temperature' in data:
                temperature_data = {
                    '日期': [item['time'][5:] for item in data['temperature']],  # 只取日期的天数
                    '温度变化': [item['value'] for item in data['temperature']]
                }
                with col2:
                    st.caption('气温')
                    st.line_chart(
                        temperature_data,
                        y='温度变化',
                        x='日期',
                        use_container_width=True
                    )

        if show_button:
            st.button("向Agromind提问",
                      on_click=switch_to_question,
                      key=unique_key,
                      use_container_width=True)

# API for list
def list_api(start_date, end_date):
    url = f"{st.secrets.LIST_API_URL}{start_date}/{end_date}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"列表API请求错误: {e}")
        return None

# list content
contents = []
def list_contents(api_data):
    for item in api_data:
        contents.append({
            "range": item['range'],
            "title": item["title"],
            "content": item["content"],
            "data": item["data"]
        })
    return contents


# streamlit page layout
st.set_page_config(layout="wide")

# CSS
st.markdown("""
    <style>
    .reportview-container .main .block-container {
        max-width: 100%;
        padding: 0;
    }
    /* Reset Streamlit's default padding */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
    }

    [data-testid="stAppViewContainer"] > section:first-child {
        padding: 0 !important;
    }

    div[data-testid="stToolbar"] {
        display: none;
    }

    /* Set page background color */
    .stApp {
        background-color: #F4F4F4;
    }

    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background-color: white;
        padding: 20px;
        border-bottom: 1px solid #ddd;
        height: 75px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Reset margins for content sections */
    .content-section {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .content-card {
        background-color: white;
        border-radius: 10px;
        padding: 24px;
        margin: 0 24px;
        border: 1px solid #ddd;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Remove spacing from section divider */
    .section-divider {
        margin: 0;
        border-bottom: 1px solid #eee;
    }

    /* Target Streamlit's auto-generated containers */
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Target specific Streamlit markdown containers */
    .stMarkdown {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Target Streamlit's emotion cache containers */
    .st-emotion-cache-1gjp2hn {
        margin: 0 !important;
        padding: 0 !important;
    }

    .st-emotion-cache-phe2gf {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Target all potential container variations */
    [data-testid="stElementContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Ensure no extra spacing in markdown containers */
    [data-testid="stMarkdownContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .content-wrapper {
        margin: 40px 0;
        max-width: 100%;
        padding: 0 !important;
    }

    /* Card container styles with responsive padding */
    .stCard {
        background-color: white;
        border-radius: 10px;
        margin: 10px 1rem;
        border: 1px solid #ddd;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        padding: 24px;
    }

    /* Media queries for different screen sizes */
    @media (min-width: 768px) {
        .stCard {
            margin: 10px 24px;
        }
        .main .block-container {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        [data-testid="stSidebarContent"] {
            padding-right: 0 !important;
        }
    }

    /* Hide the default Streamlit header elements */
    header {
        visibility: hidden;
    }

    /* Style the date input container */
    div[data-testid="stDateInput"] {
        position: fixed !important;
        top: -10px !important;
        right: 20px !important;
        z-index: 1000 !important;
        width: 200px !important;
    }

    /* Adjust sidebar width */
    [data-testid=stSidebar] {
        min-width: 250px !important;
        max-width: 250px !important;
    }

    /* Card typography styles */
    .stCard h3 {
        margin: 0 0 16px 0;
        font-size: 1.5rem;
    }
    .stCard p {
        margin: 8px 0;
        line-height: 1.5;
    }

    /* Override any extra padding from Streamlit containers */
    .element-container, .stMarkdown {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
        .stCard {
        background-color: white;
        border-radius: 10px;
        padding: 24px;
        margin: 10px 1rem;
        border: 1px solid #ddd;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    /* Style h6 (date) */
    .stCard h6 {
        color: #666;
        margin: 0 0 -16px 0;  /* Adjust space between date and title */
        font-size: 1rem;
    }

    /* Style h4 (title) */
    .stCard h4 {
        margin: 0 0 16px 0;  /* Adjust space between title and button */
        font-size: 1.2rem;
    }

    /* Style h4 (title) */
    .stCard p {
        margin: 0 0 32px 0;  /* Adjust space between title and button */
        font-size: 1rem;
    }

    /* Style button */
    .custom-button {
        background-color: #F4F4F4;
        color: #999999;
        padding: 8px 16px;
        border: 1px solid #CCCCCC;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        transition: background-color 0.3s;
        width: 100%;
        display: block;
        box-sizing: border-box;
        margin: 0;  /* Reset button margin */
    }

    .custom-button:hover {
        background-color: #F7F7F7;
        border: 1px solid #cccccc;
    }

    .custom-button.clicked {
        background-color: #dddddd;
        border-color: #000000;
        color: white;
        pointer-events: none;  /* Disable hover effects when clicked */
    }


    /* Focus - keyboard navigation state */
    .custom-button:focus {
        outline: 2px solid #ffffff;
        outline-offset: 2px;
    }

    /* Active - clicking/pressing state */
    .custom-button:active:not(:disabled) {
        background-color: #ffffff;
        border-color: #ffffff;
        color: white;
        transform: translateY(1px);
    }

    /* Style the vertical block container */
    [data-testid="stVerticalBlock"] > div:has(div.element-container) {
        background-color: white;
        border-radius: 10px;
        padding: 24px;
        margin: 0 1rem;
        border: 1px solid #ddd;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Add specific styling for chat messages to ensure they're not affected */
    [data-testid="stChatMessage"] {
        margin: 8px 32px !important;
        padding: 0 !important;
        background: none !important;
        border: none !important;
        box-shadow: none !important;
    }

    @media (min-width: 768px) {
        [data-testid="stVerticalBlock"] > div:has(div.element-container) {
            margin: 10px 24px;
        }
    }

    /* Style text elements */
    .date-text {
        color: #666;
        font-size: 1rem;
        margin-bottom: 0;
    }

    .title-text {
        font-size: 1.2rem;
        margin: 24px 0 16px 0;
    }

    .content-text {
        font-size: 1rem;
        margin: 0 0 32px 0;
    }

    /* Style the button */
    .stButton button {
        background-color: #F4F4F4 !important;
        color: #999999 !important;
        padding: 8px 16px !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 4px !important;
        cursor: pointer !important;
        font-size: 14px !important;
        transition: background-color 0.3s !important;
        width: 100% !important;
    }

    .stButton button:hover {
        background-color: #F7F7F7 !important;
        border: 1px solid #cccccc !important;
    }

    .stButton button:active {
        background-color: #ffffff !important;
        border-color: #ffffff !important;
        color: white !important;
        transform: translateY(1px) !important;
    }

    div[data-testid="stElementContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    .card-container {
    }

    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background-color: white;
        padding: 20px;
        border-bottom: 1px solid #ddd;
        height: 75px;
        display: flex;
        align-items: center;
    }
    
    /* 定位最外层容器 */
    .st-key-header_back_button {
        position: fixed !important;
        top: 20px !important;
        left: 20px !important;
        z-index: 1000000 !important;
        width: auto !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* 定位 stButton 容器 */
    .st-key-header_back_button .stButton {
        width: auto !important;
    }
    
    /* 定位按钮本身 */
    .st-key-header_back_button button[data-testid="stBaseButton-secondary"] {
        width: auto !important;
        padding: 8px 16px !important;
        background-color: #F4F4F4 !important;
        color: #999999 !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 4px !important;
        font-size: 14px !important;
        margin: 0 !important;
        min-width: 0 !important;
    }
    
    /* 定位按钮内的文字容器 */
    .st-key-header_back_button [data-testid="stMarkdownContainer"] {
        display: inline-block !important;
    }
    
    /* 定位按钮内的段落 */
    .st-key-header_back_button [data-testid="stMarkdownContainer"] p {
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }
    
    </style>
""", unsafe_allow_html=True)


# side bar
if st.session_state.current_screen == 'main':
    with st.sidebar:
        st.image("logo.png", use_container_width=True)
        st.markdown("# Hao Zhang")
        st.caption("13510004950")
        st.button("账号")
        st.markdown("---")
        st.markdown("设置您的农场或大棚")
        st.markdown("设置大语言模型")
        st.markdown("设置数据")
        st.markdown("关于")
        st.markdown("---")
        st.caption("Version 1.0")


# switch pages style
if st.session_state.current_screen == 'question':
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp {
            background-color: #F4F4F4 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# initiate date picker
today = datetime.datetime.now().date()
seven_days_ago = today - datetime.timedelta(days=7)
min_date = datetime.date(2023, 1, 1)

# switch page header
if st.session_state.current_screen == 'main':

    st.markdown("""
        <div class="fixed-header">
        </div>
    """, unsafe_allow_html=True)

    selected_date = st.date_input(
        "",
        (seven_days_ago, today),
        min_value=min_date,
        max_value=today,
        format="YYYY.MM.DD",
    )
    if isinstance(selected_date, tuple) and len(selected_date) == 2:
        selected_start_date = f"{selected_date[0].year}-{selected_date[0].month}-{selected_date[0].day}"
        selected_end_date = f"{selected_date[1].year}-{selected_date[1].month}-{selected_date[1].day}"

        api_data = list_api(selected_start_date, selected_end_date)
        contents = list_contents(api_data)

else:
    st.markdown("""
            <div class="fixed-header">
            </div>
        """, unsafe_allow_html=True)
    if st.button("返回", key="header_back_button", on_click=switch_to_main):
        st.session_state.current_screen = 'main'


# content wrapper
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)


# switch page contents
if st.session_state.current_screen == 'main':

    # Render each content section
    for idx, content_item in enumerate(contents):
        render_list_item(
            date_str=content_item["range"],
            title=content_item["title"],
            content=content_item["content"],
            data=content_item["data"],
            show_button=True
        )

elif st.session_state.current_screen == 'question':
    # chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=st.secrets.USER_AVATAR if message[
                                                                                   "role"] == "user" else st.secrets.ASSISTANT_AVATAR):
            st.markdown(message["content"])

    # user query
    if user_query := st.chat_input("请输入您的问题"):
        # add message to session_state
        st.session_state.messages.append({"role": "user", "content": user_query})

        # user message display
        with st.chat_message("user", avatar=st.secrets.USER_AVATAR):
            st.markdown(user_query)

        with st.chat_message("assistant", avatar=st.secrets.ASSISTANT_AVATAR):
            # Show loading message while waiting for response
            message_placeholder = st.empty()
            message_placeholder.markdown("<span style='color: #bbbbbb'>*...  思考中  ...*</span>", unsafe_allow_html=True)

            response = llm_api(user_query)
            if response:
                # Replace loading message with actual response
                message_placeholder.markdown(response)
                # add AI message to session_state
                st.session_state.messages.append({"role": "assistant", "content": response})

# close streamlit
if __name__ == "__main__":
    # Close content-wrapper div
    st.markdown('</div>', unsafe_allow_html=True)