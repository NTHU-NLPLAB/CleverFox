import openai
import streamlit as st
from doubleSpace import diff_tokens, get_a_line, replaceBlank

# openai.api_key = "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"


def chat(prompt, text, tmpr, num_token):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Act as if you are a seasoned English teacher."},
            {"role": "system", "content": "OK. I am a seasoned English teacher."},
            {"role": "user", "content": rf"{prompt}"},
            {
                "role": "assistant",
                "content": "OK. I will strictly follow the specified format above.",
            },
            {"role": "user",
                "content": r"Do the task with given Text = \"She was involved in big accident.\""},
            {"role": "system", "content": "She was involved in {+a+} big accident."},
            {
                "role": "user",
                "content": rf"Now, do the task with given \"{text}\", and generate modified text in the specified format. Note that special attention should be paid to \"idiomatic collocations\" when doing the task, which means using the phrases more common and widely used, if the word doesn't need to be replaced, don't force substitutions. The output contains ONLY modified text.",
            },
        ],
        temperature=float(tmpr),
        max_tokens=int(num_token),
    )
    return response


def grammar(text):
    '''
    call ChatGPT to correct the text(article)
    '''
    temp_prompt = """Help improve my text by making EVERY sentence more grammatical and logical in Standard English use. \
                    Precisly mark EACH word to be replaced with square brackets (i.e., \"[-\", \"-]\"), \
                    and insert the suggested word to replace with curly brackets (i.e., \"{{+\", \"+}}\") right before EACH word to be replaced.\
                    If gramma is correct, don't replace it.\
                    Text = I'm writing to You in order to express my feelings.
                    Corrected Text =  I'm writing to {+you+} [-You-] in order to express my feelings.
    """
    # temp_tmpr = 0.3
    # temp_max = 500

    # using ChatGPT to revise article
    # promptGpt = st.text_area('Write down the word you want to prompt:', temp_prompt)
    # subcol1, subcol2 = st.columns(2)
    # with subcol1:
    #     tmpr = st.text_input('Write down temperature', temp_tmpr)
    # with subcol2:
    #     num_token = st.text_input('Write down # of max tokens', temp_max)

    submit_prompt = st.button('送出')
    st.subheader('**批改結果**')
    if submit_prompt:
        # Get ChatGPT answer
        response = chat(temp_prompt, text, 0.3, 500)
        fixed_sentence = response['choices'][0]['message']['content']

        # Display double space format
        with st.container():
            sent_tokens = diff_tokens(fixed_sentence)
            while sent_tokens != [0]:
                lines, sent_tokens = get_a_line(sent_tokens)
                print(lines[0])
                print(lines[1])
                line1 = replaceBlank(lines[0])
                line2 = replaceBlank(lines[1])
                st.write(line1, '\n', line2)

        getExplain(fixed_sentence)
        # Original fixed sentence
        # with st.expander('Original Fixed Sentence'):
        #     st.write(fixed_sentence)
        # All content of reponse
        # with st.expander('Whole Response'):
        #     st.write(response)


# explain
def getExplain(fixed_sentence):
    # fixed_sentence = st.text_area('Fixed Sentence', f'{fixed_sentence}')
    QUES1 = "Compare the modified parts to the original text of the following setnece, precisly explain why the replacement is better than original word in a markdown table : Last summer, I {+went+} [-go-] on a trip to {+a+} [-an-] beautiful beach. The weather was sunny and warm."
    ANS1 = "| 原字詞 | 替代字詞 | 詞組(span of words) | 解釋 |\n|---|---|---|---|\n|  go | went | I went on a trip | 將\"go\"改為\"went\"是為了修正動詞的時態錯誤。 |\n| an | a | a beautiful beach | 由於 \"beautiful beach\" 以子音音素開頭，所以需要使用 \"a\" 這個冠詞，而不是 \"an\"。 |"
    QUES2 = "Compare the modified parts to the original text of the following setnece, precisly explain why the replacement is better than original word in a markdown table : I built {+sandcastles+} [-sendcastles-] with my family {+and+} [-or-] collected seashells."
    ANS2 = "| 原字詞 | 替代字詞 | 詞組(span of words) | 解釋 |\n|---|---|---|---|\n| sendcastles | sandcastles | built sandcastles | 原本的 \"sendcastles\" 拼寫錯誤，正確的是 \"sandcastles\"。 |\n| and | or | and collected seashells | \原文使用的 \"or\" 暗示只能選擇其中一個活動，但根據上下文，你的意圖是同時進行兩個活動，所以需要使用 \"and\" 來連接兩個動詞。 |"
    QUES3 = "Compare the modified parts to the original text of the following setnece, precisly explain why the replacement is better than original word in a markdown table : I am against the other product, {+the+} invisible cloaks."
    ANS3 = "| 原字詞 | 替代字詞 | 詞組(span of words) | 解釋 |\n|---|---|---|---|\n| N/A | the | the invisible cloaks | \"invisible cloaks\" 是特指的名詞片語，需要使用定冠詞 \"the\" 來指明你所提到的具體產品是哪一種。|"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": QUES1},
            {"role": "assistant", "content": ANS1},
            {"role": "user", "content": QUES2},
            {"role": "assistant", "content": ANS2},
            {"role": "user", "content": QUES3},
            {"role": "assistant", "content": ANS3},
            {
                "role": "user",
                "content": f"Compare the modified parts to the original text of the following setnece, precisly explain the replacement in a markdown table :{fixed_sentence}\
                                                    If there is NO error, DON'T need to print out the table and any content. Just leave it blank. ",
            },
        ],
        temperature=0,
        max_tokens=1500,
    )
    response_text = response["choices"][0]['message']['content']
    st.subheader('以下為解釋表格： \n', response_text)

    return response_text
