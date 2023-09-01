import streamlit as st
import pandas as pd

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

st.title("🦊 您好！郝多章老師")
st.subheader('以下是您指導的學生寫作紀錄')

names = ['許宗儒',
        '陳昱翔',
        '蔡宜庭',
        '張宇軒',
        '林子傑',
        '何思妤',
        '陳雅築',
        '張家豪',
        '柯宥辰',
        '藍佳穎',
        '古彥均',
        '莊庭瑜',
    ]
category = ['3', '4', '6', '2', '8', '3', '8', '4', '6', '1', '4', '8']
grammer = ['10', '12', '15', '13', '4', '20', '22', '12', '1', '10', '21', '16']
level = ['1', '13', '12', '28', '10', '9', '9', '7', '23', '27', '10', '11']
tran = ['6', '7', '5', '28', '7', '6', '4', '2', '6', '8', '5', '3']
data = {'姓名': names, '文章數': category, '最新文章的文法改錯(錯誤次數)': grammer, '最新文章的文字等級提升(替換次數)': level, '最新文章的轉折詞分析(出現次數)': tran}
df = pd.DataFrame(data)

st.dataframe(data=df, width=1000)
comment = st.button('回饋區')
if comment:
    st.markdown("老師好！此處可以留下您想給學生的回饋")

    st.selectbox(
        '##### 選擇學生',
        (
            '許宗儒',
        '陳昱翔',
        '蔡宜庭',
        '張宇軒',
        '林子傑',
        '何思妤',
        '陳雅築',
        '張家豪',
        '柯宥辰',
        '藍佳穎',
        '古彥均',
        '莊庭瑜',
        ),
    )

    st.text_input("##### 回饋內容", '')
    st.button('送出')
