import grammaly
import wordchoice
import openai
import streamlit as st
import RhetoricalFunction

# from st_pages import Page, show_pages, add_page_title
from streamlit import session_state

# Set the page title
st.set_page_config(page_title='CleverFox', page_icon='🦊', layout='wide')
# 設定網頁的字體
st.markdown(
    """
      <style>
        html, body, [class*="css"]  {
        font-family: Courier New, "微軟正黑體";
        }
        [class="mord"], [class="vlist-r"] {
        font-family: Courier New, "微軟正黑體", Microsoft JhengHei;
        font-size: 16px;
        }
      </style>

      """,
    unsafe_allow_html=True,
)

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.imgur.com/Qj5z2Du.png);
                background-repeat: no-repeat;
                background-size: 30%;
                background-position:20px 100px;
                padding-top: 120px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def run():
    st.session_state.run = True

def refresh_mainpage():
    # 清空 session_state.show_topic 前先檢查是否存在
    session_state.show_topic = {
        "content": "",
        "image_url": " ",
    }
    st.session_state.run = False
    # 使用 st.experimental_rerun() 重新運行整個應用程序
    st.experimental_rerun()

add_logo()
st.title("🦊 I'd Rather Be a CleverFox")

# Import OpenAI API key
input_key = st.secrets["api_key"]
openai.api_key = input_key
st.divider()

col1, col2 = st.columns([4, 1])  # cut into two sections
original_content = ""
# Left page：article
with col1:
    subcol1, subcol2 = st.columns([2, 1])
    with subcol1:
        st.subheader("寫作區")
    with subcol2:
        # Exit Test Zone Button
        if session_state and (session_state.show_topic["content"] != original_content):
            if st.button("Exit Test Zone", on_click=run):
                refresh_mainpage()

    temp_text = "Water shortage has been a serious problem for many years and causes various crises. The land is crushing, overusing the underground water, and many people can’t get enough water, swarming the water cart like thirsty animals. All of these sounds horrible. Climate change, the biggest cause of environmental problems. Earth has become hotter and hotter these years, and the climate is getting extremely hot. No typhoons, less rain, both of them cause water shortages. All in all, the problem above is all because of yourself, and the only solution is also to attend to us. From now on, save water whenever possible, enhance education, and cherish our mother earth. I hope the world will be better."

    # input raw article
    # Synchronize testZone content
    with st.expander("### 原始文章", expanded=True):
        if session_state and (session_state.show_topic["content"] != original_content):
            st.write(session_state.show_topic["content"])
            if session_state.show_topic["image_url"] != " ":
                st.image(
                    session_state.show_topic["image_url"],
                    # caption="歷屆考古試題",
                    use_column_width=True,
                )
        else:
            st.write(original_content)
        uploaded_file = st.file_uploader('上傳你的文章（限PDF檔案）', type="pdf")
        text = st.text_area("", temp_text)


with col2:
    st.subheader("批改選項")
    revise_topic = st.radio("", ['文法改錯', '文字等級提升', '轉折詞分析'])

# output edited article
if not text:
    st.error('未有文章')
else:
    if revise_topic == '文法改錯':
        grammaly.grammar(text)

    if revise_topic == '文字等級提升':
        wordchoice.choice(text)

    if revise_topic == '轉折詞分析':
        RhetoricalFunction.process_article(text)
