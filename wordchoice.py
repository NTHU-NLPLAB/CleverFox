import openai
import streamlit as st
from doubleSpace import diff_tokens, get_a_line, replaceBlank

# openai.api_key = "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"
CEFR = "A1 - Beginner, A2 - Elementary, B1 - Intermediate, B2 - Upper Intermediate, C1 - Advanced, C2 - Proficient"


def choice(text):
    level = st.selectbox(
        '請選擇CEFR語言分級：',
        (
            'A1 - Beginner',
            'A2 - Elementary',
            'B1 - Intermediate',
            'B2 - Upper Intermediate',
            'C1 - Advanced',
            'C2 - Proficient',
        ),
    )
    st.write('你所選的語言分級', level)

    messages = [
        {
            "role": "user",
            "content": f"Act as if you are a seasoned English teacher to help improve my text into \"{level}\" accordding to \"{CEFR}\" with better word choices and idiomatic collocations, in Standard English use.\
                                Now, proofread the \"{text}\". \
                                Precisly mark EACH word to be replaced with square brackets (i.e., \"[-\", \"-]\"), \
                                and insert the suggested word to replace with curly brackets (i.e., \"{{+\", \"+}}\") right before EACH word to be replaced.\
                                If the word is good enough, don't replace it.\
                                Don't change the meaning of the text and don't change the words into lower level. \
                                Given a text = \"I like sports.\" \
                                Example of the modified text: \"I {{+enjoy+}} [-like-] sports.\"",
        },
        {"role": "assistant", "content": f"OK. I will strictly follow the specified format above."},
        {
            "role": "user",
            "content": f"Do the task with given Text = \"As a diligent student, taking notes is improtant to get started.\"",
        },
        {
            "role": "assistant",
            "content": f"As a diligent student, {{+jotting down+}} [-taking-] notes is {{+necessary+}} [-improtant-] {{+for starters+}}[-to get started-].",
        },
        {
            "role": "user",
            "content": f"Do the task with given Text = \"I'd love to walk in the streets at night.\"",
        },
        {
            "role": "assistant",
            "content": f"I'd love to {{+stroll+}} [-walk-] in the streets at night.",
        },
        {
            "role": "user",
            "content": f"Now, do the task with given \"{text}\", and generate modified text in the specified format. Note that special attention should be paid to \"idiomatic collocations\" when doing the task, which means using the phrases more common and widely used, if the word doesn't need to be replaced, don't force substitutions. The output contains ONLY modified text.",
        },
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3,
        max_tokens=512,
        # top_p=1,
        # frequency_penalty=0,
        # presence_penalty=0
    )
    # res = response['choices'][0]['message']['content']
    # if st.button('check'):
    #     st.write(res)

    check = st.button('送出')
    st.subheader('**批改結果**')

    if check:
        # Get ChatGPT answer
        res = response['choices'][0]['message']['content']
        fixed_sentence = res
        # Display double space format
        with st.container():
            sent_tokens = diff_tokens(fixed_sentence)
            while sent_tokens != [0]:
                lines, sent_tokens = get_a_line(sent_tokens)
                print(lines[0])
                print(lines[1])
                line1 = replaceBlank(lines[0])
                line2 = replaceBlank(lines[1])
                st.write(line1)
                st.write(line2)

        getExplain(res)
        # Original fixed sentence
        # with st.expander('Original Fixed Sentence'):
        #     st.write(fixed_sentence)
        # All content of reponse
        # with st.expander('Whole Response'):
        #     st.write(response)


# explain
def getExplain(fixed_sentence):
    # fixed_sentence = st.text_area('Fixed Sentence', f'{fixed_sentence}')
    QUES1 = "Compare the modified parts to the original text of the following setnece, precisly explain why the replacement is better than original word in a markdown table : Last summer, I went on a trip to a {+stunning+} [-beautiful-] beach. The weather was {+bright+} [-sunny-] and {+pleasantly+} [-warm-]."
    ANS1 = "| 原字詞 | 替代字詞 | 詞組(span of words) | 解釋 |\n|---|---|---|---|\n|  beautiful  |  stunning  | a stunning beach  | \"Stunning\"（令人驚嘆的）傳達了比\"beautiful\"（美麗的）更強烈的敬畏和欽佩的感覺。 |\n| sunny | bright | The weather was bright | \"Bright\" （明亮的）是對天氣狀況更具體生動的描述。 |\n| warm | pleasantly | The weather was bright and pleasantly | \"Pleasantly\"（愉快地）為溫度添加了積極和愉悅的涵義。 |"
    QUES2 = "Compare the modified parts to the original text of the following setnece, precisly explain why the replacement is better than original word in a markdown table : I {+constructed+} [-built-] sandcastles with my family and {+gathered+} [-collected-] seashells."
    ANS2 = "| 原字詞 | 替代字詞 | 詞組(span of words) | 解釋 |\n|---|---|---|---|\n| built | constructed | I constructed sandcastles with my family | \"Constructed\" （建造）強調了在建造沙堡時所投入的努力和創意。 |\n| collected | gathered | gathered seashells | \"Gathered\" （收集）是更精確的動詞，用於描述收集海貝殼的行動。 |"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": QUES1},
            {"role": "assistant", "content": ANS1},
            {"role": "user", "content": QUES2},
            {"role": "assistant", "content": ANS2},
            {
                "role": "user",
                "content": f"Compare the modified parts to the original text of the following setnece, precisly explain the replacement in a markdown table :{fixed_sentence}",
            },
        ],
        temperature=0,
        max_tokens=1500,
    )
    response_text = response["choices"][0]['message']['content']
    st.write('以下為解釋表格： \n', response_text)

    # with st.expander('Whole Response'):
    #     st.write(response)
    return response_text


# Explain the modified part of following setnece in a markdown table
