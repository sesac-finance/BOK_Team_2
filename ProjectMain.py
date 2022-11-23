import os
import pandas as pd
from ekonlpy.sentiment import MPCK

# to see all data
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.width', 100)
pd.set_option('display.colheader_justify', 'left')


# csv 파일로부터 데이타 불러오기
def text_from_csv():
    mergerd_directory = './Data/Merged/'
    total_text = []
    columns = ['date', 'contents']
    for files_name in os.listdir(mergerd_directory):
        text_list = []
        if 'Minutes' not in files_name:
            with open(mergerd_directory + files_name, 'r', encoding='utf8') as f:
                for text in f.readlines():
                    text_list.append(text.split(',')[1:])
            total_text.extend(text_list)
    df_text_list = pd.DataFrame(total_text, columns=columns)
    return df_text_list


df_all_data = text_from_csv().sort_values(by='date', ascending=True)
all_contents = df_all_data['contents']

sentiment_list = []
cnt = 0
for index in range(len(all_contents)):
    content = df_all_data['contents'].iloc[index]
    date = df_all_data['date'].iloc[index]
    mpck = MPCK()
    tokens = mpck.tokenize(content)
    ngrams = mpck.ngramize(tokens)
    score = mpck.classify(tokens + ngrams, intensity_cutoff=1.5)
    # print("tokens", tokens)
    print("ngrams", ngrams)
    # print("score", score)
    sentiment_list.append([date, score])
    cnt += 1
    if cnt > 50:
        break

# print(sentiment_list)
