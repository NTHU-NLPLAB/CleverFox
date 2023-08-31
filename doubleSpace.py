import re


def combine_tokens(fixed_list):
    '''
    將[0, '']: no errors, [1, '']:  correction word, [-1, '']: wrong word
    改成word, {+word+}, [-word-]形式
    '''
    result = []
    current_text = ""

    i = 0
    while i < len(fixed_list):
        tag, text = fixed_list[i]

        if tag == 0:  # no errors
            current_text += text + ' '

        elif tag == 1 and re.match('\n', fixed_list[i + 1][1]):  # \n+word
            i += 1
            current_text += fixed_list[i][1] + ' '

        elif tag == 1:  # correction word
            combined_text = text
            temp_text = ''
            while i + 1 < len(fixed_list) and fixed_list[i + 1][0] == 1:
                # 若文章未到結尾&連續出現錯字
                i += 1
                temp_text += ' ' + fixed_list[i][1]

            if (
                fixed_list[i + 1][0] == -1 and re.search('\n', fixed_list[i + 1][1]) != None
            ):  # 處理[word0]: \n\n[word1]被分成[word0], [:], [word1]
                i += 1
                current_text += fixed_list[i][1] + ' '
            else:
                combined_text += temp_text
                current_text += '{+' + combined_text + '+} '  # 把正確的字加到原有文章

        elif tag == -1:  # wrong word
            combined_text = text
            while i + 1 < len(fixed_list) and fixed_list[i + 1][0] == -1:
                i += 1
                combined_text += ' ' + fixed_list[i][1]
            current_text += '[-' + combined_text + '-] '

        i += 1

    # 移除最後一個空格
    combined_text = current_text.strip()
    result.append(combined_text)
    fixed_sentence = ' '.join(combine_tokens(result))

    return fixed_sentence


def diff_tokens(fixed_sentence):
    '''
    切字，包含以下六種形式
    {+any char} [-any char]
    [-any char]
    {+any char}
    word\d\s
    :
    \d
    \w
    '''
    return re.findall(
        r'\{\+[^}]+?\}\s\[\-[^]]+?\]|\[\-[^]]+?\]|\{\+[^}]+?\}|[^a-zA-Z\d\s:]|:|\d+|\w+|\n',
        fixed_sentence,
    )


# Generate double-spaced sentences with edits
def get_a_line(tokens, limit=60):
    '''
    產生以60個字為一行的文章with double-space sentences
    '''
    # colors
    # error_html_start = ':blue[$\\tt{\\underline{'  # color=blue & underline
    # error_html_end = '}}$]'
    error_html_start = ':blue['  # color=blue
    error_html_end = ']'
    edit_html_start = ':red['  # color=red
    edit_html_end = ']'

    # 追蹤當前行的長度與兩行的文本
    skip, acc_length, line1, line2 = False, 0, '', ''

    for i, token in enumerate(tokens):
        if skip:
            skip = False
            continue
        # 若標記單位是 "{+edit+} [-error-]" 形式
        if token.startswith('{+') and token.endswith('-]'):
            edit, error = token[2:-2].split('+} [-')  # 取出word
            maxlen = max(len(error), len(edit))
            line1 += error_html_start + error + error_html_end + (' ' * (maxlen - len(error) + 1))
            line2 += edit_html_start + edit + edit_html_end + (' ' * (maxlen - len(edit) + 1))
            acc_length += maxlen + 1

        # 若只有 "[-error-]" 形式
        elif token.startswith('[-'):
            error = token[2:-2]
            line1 += error_html_start + error + ' ' + error_html_end
            line2 += ' ' * (len(error) + 1)
            acc_length += len(error) + 1

        # 若只有 "{+edit+}" 形式
        elif token.startswith('{+'):
            edit = token[2:-2]
            try:
                next = tokens[i + 1]
            except:
                next = edit
            maxlen = max(len(next), len(edit))
            line1 += (' ' * (maxlen - len(next) + 2)) + next + ' '
            line2 += (
                edit_html_start + '^ ' + edit + edit_html_end + (' ' * (maxlen - len(edit) + 1))
            )
            acc_length += len(edit) + 1
            skip = True

        # 普通單詞
        elif token.isalpha():
            line1 += token + (' ')
            line2 += ' ' * (len(token) + 1)
            acc_length += len(token) + 1

        # 標點符號
        else:
            line1 = line1.rstrip()
            line1 += token + (' ')
            line2 += ' ' * (len(token) + 1)
            acc_length += len(token) + 1
        print('line1:', len(line1), 'line2:', len(line2))
        print(line1)
        print(line2)

        # 檢查 acc_length 是否超過指定的行長限制
        if token == '\n' or (acc_length) > limit or i == len(tokens) - 1:
            maxlen = max(limit, acc_length)
            line1 += (
                ' ' * (limit - acc_length - 1)
                if limit - acc_length > 0
                else ' ' * (acc_length - limit - 1)
            )
            line2 += (
                ' ' * (limit - acc_length - 1)
                if limit - acc_length > 0
                else ' ' * (acc_length - limit - 1)
            )

            tokens = [t for t in tokens[i + 1 :]]
            if tokens != []:
                print('tokens: ', tokens)
                return [line1, line2], tokens
            else:
                return [line1, line2], [0]


def replaceBlank(text):
    '''
    let blank fit the format of streamlit
    '''
    replaced = ''
    i = 0
    while i < len(text):
        replaced += '&nbsp;' if text[i] == ' ' else text[i]
        i += 1
        # begin = text[i : i + 6]
        # end = text[i : i + 4]
        # while begin != ':blue[' and i < len(text):
        #     replaced += '&nbsp;' if text[i] == ' ' else text[i]
        #     i += 1
        #     begin = text[i : i + 6]
        #     continue
        # while end != '}}$]' and i < len(text):
        #     replaced += '~' if text[i] == ' ' else text[i]
        #     i += 1
        #     end = text[i : i + 4]
        #     continue
    return replaced
