import random

import streamlit as st
import streamlit.components.v1 as components
from streamlit import session_state
from 主頁 import original_content


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

st.title("🦊 Test Zone 測驗區")
st.text("今天想要練習什麼類型的題目呢？點擊馬上開始吧(ﾉ>ω<)ﾉ")
st.divider()


show_add_question = st.button(" ▶ 點擊收放教師設定區 ")
if "show_add_question" not in st.session_state:
    st.session_state.show_add_question = False
if show_add_question:
    st.session_state.show_add_question = not st.session_state.show_add_question
    st.session_state.something = ''

if st.session_state.show_add_question:
    st.subheader("教師設定區")

    st.markdown("老師好！此處可以新增您想讓學生練習的題目")

    st.selectbox(
        '##### 題目類別',
        (
            '短句練習',
            '長篇練習',
            '新增類別',
        ),
    )

    st.write("##### 主題敘述")
    st.text_input("簡述您想讓ChatGPT出的題目內容，包含主題的關鍵字、文章長度等", '')
    st.button('送出')

    st.divider()


# Test Content
content_general = [
    "你認為家裡生活環境的維持應該是誰的責任？請寫一篇短文說明你的看法。文分兩段，第一段説明你對家事該如何分工的看法及理由，第二段舉例説明你家中家事分工的情形，並描迹你自己做家事的經驗及感想。",
    "近年有越來越多人喜歡在家裡利用網路購物 ，省去出門逛街的麻煩。請以'Do You Like Shopping Online?'為題，寫一篇文長至少 120 個單詞的文章，表達你你對網路購物的看法。文分兩段，第一段先敘述自己對網購的看法，第二段再說明自己或他人網購的經驗。",
    "在現今社會中，有愈來愈多人因為追求身體健康而吃素。請以'To Be or Not to Be a Vegetarian?'為主題，寫一篇文長至少 120 個單詞(words)的英文作文。第一段針對文章主題表明你的立場，第二段則説明原因為何。",
    "請你針對「全球水資源短缺問題以及氣候變遷對此的影響」為題，撰寫一篇約150字的英文作文。你可以從水資源短缺的原因、影響，以及個人應該如何參與改善等方面進行描述。作文中可以提及節約用水的方法、推廣環保教育等。請闡述你的觀點，並提出具體的解決方案，希望你能充分表達對於環境保護的關注和意識。",
    "請撰寫一篇以「台灣的文化與自然之美」為主題的英文作文，字數約200字。你可以描述台灣多元的文化特色以及令人驚嘆的自然景觀，並提出促進台灣形象宣傳的建議。",
    "請針對「選擇智能眼鏡的理由與對隱形斗篷的反對看法」為題，寫一篇字數約250字的英文作文。文章應詳細闡述你選擇智能眼鏡的原因以及對隱形斗篷的反對理由。同時，探討科技的雙面性以及在應用科技時應該謹慎思考的觀點。",
]
selected_general = random.choice(content_general)

content_essay = [
    "下圖為遊客到訪某場所的新聞畫面。你認為圖中呈現的是什麼景象？你對這個景象有什麼感想？請根據此圖片，寫一篇英文作文。文分兩段，第一段描述圖片的內容，包括其中人、事、物以及發生的事情；第二段則以遊客或場所主人的立場，表達你對這件事情的看法。",
    "隨著社群媒體的普及，表情符號（emoji）的使用也極為普遍。請參考下列表情符號，寫一篇英文作文，文分兩段。第一段說明人們何以喜歡使用表情符號，並從下列的表情符號中舉一至二例，說明表情符號在溝通上有何功能。第二段則以個人或親友的經驗為例，討論表情符號在訊息表達或解讀上可能造成的誤會或困擾，並提出可以化解的方法。",
    "不同的公園，可能樣貌不同，特色也不同。請以此為主題，並依據下列兩張圖片的內容，寫一篇英文作文，文分兩段。第一段描述圖 A 和圖 B 中的公園各有何特色，第二段則說明你心目中理想公園的樣貌與特色，並解釋你的理由。",
]
image_e_urls = [
    "image/e01.png",
    "image/e02.png",
    "image/e03.png",
]
selected_essay = random.choice(content_essay)
selected_image_e_url = image_e_urls[content_essay.index(selected_essay)]

content_translation = [
    "在過去,腳踏車主要是作為一種交通工具。",
    "每年它們都吸引了成千上萬來自不同國家的觀光客。",
    "一個成功的企業不應該把獲利當作最主要的目標。",
    "飼養寵物並非一項短暫的人生體驗，而是一個對動物的終生承諾。",
    "歷史一再證明，戰爭會造成極為可怕的災難。",
    "避免衝突、確保世界和平應該是所有人類追求的目標。",
    "在享受寵物所帶來的歡樂時，我們不該忽略要善盡照顧他們的責任。",
    "根據新聞報導，每年全球有超過百萬人在道路事故中喪失性命。",
    "因此，交通法規必須嚴格執行，以確保所有用路人的安全。",
]
selected_translation = random.choice(content_translation)

content_academic = [
    "The chart below shows the number of men and women in further education in Britain in three periods and whether they were studying fulltime or part-time. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.",
    "The graph below gives information from a 2008 report about consumption of energy in the USA since 1980 with projections until 2030. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.",
    "The graph below shows average carbon dioxide (CO2) emissions per person in the United Kingdom, Sweden, Italy and Portugal between 1967 and 2007. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.",
]

image_a_urls = [
    "image/a01.png",
    "image/a02.png",
    "image/a03.jpg",
]

selected_academic = random.choice(content_academic)
selected_image_a_url = image_a_urls[content_academic.index(selected_academic)]

short_essay = [
    "指定科目考試完畢後，高中同學決定召開畢業後的第一次同學會，你被公推負責主辦。請將你打算籌辦的活動寫成一篇短文。文分兩段，第一段詳細介紹同學會的時間、地點及活動內容，第二段則說明採取這種活動方式的理由。"
]
selected_short = random.choice(short_essay)

long_essay = [
    "小考、段考、複習考、畢業考、甚至校外其它各種大大小小的考試，已成為高中學生生活中不可或缺的一部份。請寫一篇120至150個單詞左右的英文作文。文分兩段，第一段以Exams of all kinds have become a necessary part of my high school life.為主題句；第二段則以The most unforgettable exam I have ever taken is…為開頭並加以發展。",
]
selected_long = random.choice(long_essay)


# Button Function
def test_translation():
    selected_image_url = " "
    session_state.show_topic = {
        "content": selected_translation,
        "image_url": selected_image_url,
    }


def test_essay():
    session_state.show_topic = {
        "content": selected_essay,
        "image_url": selected_image_e_url,
    }


def test_academic():
    session_state.show_topic = {
        "content": selected_academic,
        "image_url": selected_image_a_url,
    }


def test_general():
    selected_image_url = " "
    session_state.show_topic = {
        "content": selected_general,
        "image_url": selected_image_url,
    }


def test_short():
    selected_image_url = " "
    session_state.show_topic = {
        "content": selected_short,
        "image_url": selected_image_url,
    }


def test_long():
    selected_image_url = " "
    session_state.show_topic = {
        "content": selected_long,
        "image_url": selected_image_url,
    }


if "show_topic" not in session_state:
    selected_image_url = " "
    session_state.show_topic = {
        "content": original_content,
        "image_url": selected_image_url,
    }


# show test content
def temp():
    if session_state:
        content = session_state.show_topic["content"]
        pic = session_state.show_topic["image_url"]

        with st.expander("寫作題目", expanded=True):
            st.write(content)
            if pic != " ":
                st.image(
                    session_state.show_topic["image_url"],
                    use_column_width=True,
                )


col1, col2 = st.columns([2, 3])  # cut into two sections

# right page:test content
with col1:
    st.subheader("學測英文")
    # Test Types Button
    # with st.container():
    if st.button("Translation 中翻英", key="translation_btn"):
        test_translation()
    if st.button("Essay 作文", key="essay_btn"):
        test_essay()

    st.subheader("英文檢定考")
    if st.button("Academic Writing 學術寫作", key="academic_writing_btn"):
        test_academic()
    if st.button("General Writing 一般寫作", key="general_writing_btn"):
        test_general()

    st.subheader("教師自訂區")
    if st.button("短句練習（50字以內）", key="short_writing_btn"):
        test_short()
    if st.button("長篇練習", key="long_writing_btn"):
        test_long()

# left page：button
with col2:
    temp()
    subcol1, subcol2 = st.columns([3, 1])
    with subcol2:
        if st.button("開始寫作", key="start_writing_btn"):
            st.components.v1.html(
                """
                <script>
                    window.parent.document.querySelector('.css-lrlib li:nth-child(1) a').click()
                </script>
            """
            )
