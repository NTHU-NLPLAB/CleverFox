import openai
import streamlit as st
from streamlit_chat import message

# openai.api_key = "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"


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


add_logo()
# initial state
question_related = '''Fake news can be defined as news containing false or misleading information that appears truthful.
Although fake news has long been in existence and this issue is as old as the news industry itself,
the Internet and social media have made creating and sharing fake news easier and faster than ever.
Consequently, people may be deceived by fake news, believing the content to be genuine without questioning the sources.
With so much fake news being spread every day, it is now more important than ever to understand where such news comes from and to question the news stories we read.
'''
ans_related = "Grammar"
response_tone = "Formal English Writing"
Word_limit = 50


# 預設問題：文法、單字、結構，老師可以填入有關課程prompt（可以點擊讓學生看）
def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Who are you?"},
            {"role": "assistant", "content": "I am your remote English Teacher Assistant"},
            {"role": "user", "content": "Introduce the system"},
            {
                "role": "assistant",
                "content": "We can automatic check you grammar and spelling, also list the error in a table below the modified article. There are test zones where you can find problems to start writing.",
            },
            {"role": "user", "content": f"Your answer should be related to {ans_related}"},
            {"role": "assistant", "content": f"Ok, I got it."},
            {"role": "user", "content": f"看到中文輸入時，請用中文回答我"},
            {"role": "assistant", "content": f"好的，我看到中文輸入時，一定會回答中文"},
            {"role": "user", "content": f"你是誰"},
            {"role": "assistant", "content": f"我是你的AI教學助教"},
            {"role": "user", "content": f"Plus是一個好的轉折語嗎？"},
            {"role": "assistant", "content": f"不是，正式英文中我們會使用其他字，如in addition to、furthermore等等"},
            {
                "role": "user",
                "content": f"Answer the question with {response_tone}tone within {Word_limit} words",
            },
            {"role": "assistant", "content": f"Ok, I got it."},
            {"role": "user", "content": f"{prompt}"},
        ],
        temperature=0.3,
        max_tokens=700,
    )
    return response['choices'][0]['message']['content']


##Showing setting button
st.title("🦊 嗨！我是你的AI教學助教💡")

input_key = st.secrets["api_key"]
openai.api_key = input_key
st.divider()

show_teacher = st.button(" ▶ 點擊收放教師設定區 ")

if "show_teacher" not in st.session_state:
    st.session_state.show_teacher = False
if show_teacher:
    st.session_state.show_teacher = not st.session_state.show_teacher
    st.session_state.something = ''

if st.session_state.show_teacher:
    st.markdown("### 教師設定區")

    st.markdown("老師好！請更改以下設定讓助教更符合您需求的助教")
    col1, col2 = st.columns([2, 1])  # cut into two sections

    # left page：article
    with col1:
        st.markdown('#### 教學素材')
        text = ''

        # input raw article
        with st.expander('您希望學生多多詢問有關以下課程內容的問題', expanded=True):
            question = st.text_area('', question_related)

    with col2:
        st.markdown("#### 著重面向")
        st.markdown('您希望助教的回答著重在以下某個方面')
        ans_related = st.radio('', ['文法', '字彙', '易混肴字詞', '文章結構'])
        st.write(' ')

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### 字數")
        Word_limit = st.text_input('助教回覆的字數限制', Word_limit)
    with col4:
        st.markdown("#### 語調")
        response_tone = st.selectbox(
            '您希望助教的回答符合下述語調', ('正式英文寫作', '正式英文口說', '標準英文使用', '專業的英文老師', '英文母語者')
        )
    st.divider()


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

## Clear input_text when submit
if 'something' not in st.session_state:
    st.session_state.something = ''


def submit():
    st.session_state.something = st.session_state.widget
    st.session_state.widget = ''


st.text_input("你想了解什麼？", key="widget", placeholder='在這裡輸入問題', on_change=submit)

if st.button('產生建議問題'):
    st.session_state.something = ''
    following_question = generate_response(
        f"Randomly generate three questions related to {question_related} within 10 words"
    )
    st.write(f"🦊 你可以試著問問：\n{following_question}")

user_input = st.session_state.something

if user_input:
    output = generate_response(user_input)
    st.session_state['generated'].append(output)
    st.session_state['past'].append(user_input)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
