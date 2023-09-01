import openai
import streamlit as st
from CountTokens import num_tokens_from_messages, count_tokens
from doubleSpace import diff_tokens, get_a_line, replaceBlank

functions_file_path = "./rhetorical_functions.txt"
with open(functions_file_path , 'r') as functions_file:
    rhetorical_functions = functions_file.read()

def process_article(article_content):

    CONTENT_1 = f"""I want you to act as if you are a linguist who are familiar with functional language which is meta discourse and not the content itself. Phrases in functional language typically appear at the beginning of a sentence, are high in frequency with common and general words. 

Here are 12 types of rhetorical functions and their examples.

{rhetorical_functions}

Do the following steps:
Let's do it step by step.

Step1. Read the following article and identify the word or phrases realizing rhetorical functions for each sentence.
Notice:
    1. Phrases should use less than 5 words.
    2. A sentence may have no phrase using rhetorical function.
    3. A sentence may have two or more phrases using rhetorical functions.

Step2. Mark each identified phrase with square brackets (i.e., "[-", "-]"), and then insert the corresponding rhetorical function with curly brackets  (i.e., "{{+", "+}}") right before each phrase.
For example:
Input: After the election, we asked whether the parties should change their leaders, their policies, or both. In addition, we asked about voting preferences.
Output: After the election, we asked whether the parties should change their leaders, their policies, or both. {{+A. Adding Information+}} [-In addition,-] we asked about voting preferences."""

    RESPONSE_1 = "OK. I will do it step by step and strictly follow the specified format above. Please give me more articles."

    CONTENT_2 = "The most obvious implication of the single market is, in my view, the abolition of trade and customs barriers."

    RESPONSE_2 = "The most obvious implication of the single market is {+E. Expressing Personal Opinions+} [-, in my view,-] the abolition of trade and customs barriers."

    CONTENT_3 = "I believe that we can observe two things: first, what an animal does, and second, its previous environmental history"

    RESPONSE_3 = "{+E. Expressing Personal Opinions+} [-I believe that-] we can observe two things: {+I. Listing Items+} [-first,-] what an animal does, and {+I. Listing Items+} [-second,-] its previous environmental history"
    
    CONTENT_4 = "As Davidson (1981) maintains, interpreters should be highly educated and fluent, because of the highly complex activity."
    
    RESPONSE_4 = "{+K. Citing Others+} [-As Davidson (1981) maintains,-] interpreters should be highly educated and fluent, {+D. Expressing Cause/Effect+} [-because of-] the highly complex activity."
	
    CONTENT_5 = f"""{article_content}"""
    
    model="gpt-4"
    #model="gpt-3.5-turbo"
    
    messages_1= [
        {'role': 'user', 'content': CONTENT_1},
        {'role': 'assistant', 'content': RESPONSE_1},
        {'role': 'user', 'content': CONTENT_2},
        {'role': 'assistant', 'content': RESPONSE_2},
        {'role': 'user', 'content': CONTENT_3},
        {'role': 'assistant', 'content': RESPONSE_3},
        {'role': 'user', 'content': CONTENT_4},
        {'role': 'assistant', 'content': RESPONSE_4},
        {'role': 'user', 'content': CONTENT_5}
    ]
    
    submit_prompt = st.button('送出')
    if submit_prompt:
	# Get ChatGPT answer
        response_1 = openai.ChatCompletion.create(
            model=model,
            messages=messages_1,
            temperature=0.7,
            #max_tokens=1000
        )
        fixed_sentence = response_1['choices'][0]['message']['content']	
    	
        count_tokens(messages_1, response_1, model)
    	
        # Display double space format
        with st.container():
            sent_tokens = diff_tokens(fixed_sentence)
            while sent_tokens != [0]:
                lines, sent_tokens = get_a_line(sent_tokens)
                #print(lines[0])
                #print(lines[1])
                line1 = replaceBlank(lines[0])
                line2 = replaceBlank(lines[1])
                st.write(line1)
                st.write(line2)

        getTable(fixed_sentence)
        # Original fixed sentence
        with st.expander('Original Fixed Sentence'):
            st.write(fixed_sentence)
        # All content of reponse
        with st.expander('Whole Response'):
            st.write(response_1)
   	
def getTable(fixed_sentence):

    CONTENT_6 = """Convert the article with square brackets and curly brackets into a table which containing the sentence number, sentence, phrase, and rhetorical Function, sentence by sentence.
Notice:
    1. The table should have 4 columns: Sentence Number, Sentence, Phrase, Rhetorical Function. 
    2. The rhetorical Function content should be written as "<Alphabet>. <Big Title of Function>".
    3. Each sentence must have its own row.
    4. If a sentence have no phrase using rhetorical function, leave the Phrase and Rhetorical Function blank.
    5. If a sentence have two or more phrases using rhetorical functions, separate the Phrases and Rhetorical Functions with "<br/>".
    6. Output only the table. Do not output any other message.

For example:
Input: The most obvious implication of the single market is {+E. Expressing Personal Opinions+} [-, in my view,-] the abolition of trade and customs barriers.
Output: 
Sentence Number | Sentence | Phrase | Rhetorical Function
--- | --- | --- | ---
1 | The most obvious implication of the single market is, in my view, the abolition of trade and customs barriers. | , in my view, | E. Expressing Personal Opinions
"""

    RESPONSE_6 = "OK. I will do it step by step and strictly follow the specified format above. Please give me more articles."

    CONTENT_7 = "{+E. Expressing Personal Opinions+} [-I believe that-] we can observe two things: {+I. Listing Items+} [-first,-] what an animal does, and {+I. Listing Items+} [-second,-] its previous environmental history. {+K. Citing Others+} [-As Davidson (1981) maintains,-] interpreters should be highly educated and fluent, {+D. Expressing Cause/Effect+} [-because of-] the highly complex activity."

    RESPONSE_7 = """Sentence Number | Sentence | Phrase | Rhetorical Function
--- | --- | --- | ---
1 | I believe that we can observe two things: first, what an animal does, and second, its previous environmental history | I believe that<br/>first,<br/>second, | E. Expressing Personal Opinions<br/>I. Listing Items<br/>I. Listing Items
2 | As Davidson (1981) maintains, interpreters should be highly educated and fluent, because of the highly complex activity. | As Davidson (1981) maintains,<br/>because of | K. Citing Others<br/>D. Expressing Cause/Effect
"""

    CONTENT_8 = "Sky is blue."

    RESPONSE_8 = """Sentence Number | Sentence | Phrase | Rhetorical Function
--- | --- | --- | ---
1 | Sky is blue. | |
"""

    CONTENT_9 = "A judicial investigation ordered the arrest of a police officer. {+G. Introducing a Concession+} [-However,-] a military court revoked the arrest order."

    RESPONSE_9 = """Sentence Number | Sentence | Phrase | Rhetorical Function
--- | --- | --- | ---
1 | A judicial investigation ordered the arrest of a police officer. | |
2 | However, a military court revoked the arrest order. | However, | G. Introducing a Concession
"""

    CONTENT_10 = "{+E. Expressing Personal Opinions+} [-I certainly agree that-] travelling in a group with a tour guide is the best option. Travelling outside of the place where you live is one of the most exiting things."
    
    RESPONSE_10 = """Sentence Number | Sentence | Phrase | Rhetorical Function
--- | --- | --- | ---
1 | I certainly agree that travelling in a group with a tour guide is the best option. | I certainly agree that | E. Expressing Personal Opinions
2 | Travelling outside of the place where you live is one of the most exiting things. | |
"""

    model="gpt-4"
    #model="gpt-3.5-turbo"

    messages_2= [
        {'role': 'user', 'content': CONTENT_6},
        {'role': 'assistant', 'content': RESPONSE_6},
        {'role': 'user', 'content': CONTENT_7},
        {'role': 'assistant', 'content': RESPONSE_7},
        {'role': 'user', 'content': CONTENT_8},
        {'role': 'assistant', 'content': RESPONSE_8},
        {'role': 'user', 'content': CONTENT_9},
        {'role': 'assistant', 'content': RESPONSE_9},
        {'role': 'user', 'content': CONTENT_10},
        {'role': 'assistant', 'content': RESPONSE_10},
        {'role': 'user', 'content': fixed_sentence}
    ]

    response_2 = openai.ChatCompletion.create(
        model=model,
        messages=messages_2,
        temperature=0.7,
        #max_tokens=1000
    )
    response_table = response_2['choices'][0]['message']['content']

    count_tokens(messages_2, response_2, model)

    st.write('以下為表格： \n', response_table)
    
