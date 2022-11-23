import os
import pandas as pd
from ekonlpy.sentiment import MPCK

# to see all data
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.width', 100)
pd.set_option('display.colheader_justify', 'left')


# 다양한 소스로부터 수집된 csv 파일들로부터 데이타 불러오기
def text_from_csv():
    mergerd_directory = './Data/Merged/'
    total_text = []
    columns = ['date', 'contents']
    for files_name in os.listdir(mergerd_directory):
        text_list = []

        # if 'Minutes' not in files_name:
        print(f'(text_from_csv)processing file = {files_name}')

        with open(mergerd_directory + files_name, 'r', encoding='utf8') as f:
            for text in f.readlines():
                text_list.append(text.split(',')[1:])
        total_text.extend(text_list)
    df_text_list = pd.DataFrame(total_text, columns=columns)
    return df_text_list


# 데이타 수집된 전체 파일들을 하나의 csv 파일로 생성(각 줄 형식 : 날짜, 감성분석점수)
def create_total_dataset_csv(total_dataset: pd.DataFrame, save_path='./Data/MDLs/sentiment_results.csv', purpose=False):
    sentiment_list = []
    cnt = 0
    all_contents = total_dataset['contents']

    for index in range(len(all_contents)):
        content = total_dataset['contents'].iloc[index]
        date = total_dataset['date'].iloc[index]

        # preprocessing function
        score = preprocessing(content)
        sentiment_list.append([date, score])
        print("create total dataset process check by date : ", date)

        # True for test, False for real
        if purpose:
            cnt += 1
            if cnt > 100:
                break

    df_sentiment_result = pd.DataFrame(sentiment_list)
    df_sentiment_result.to_csv(save_path)


# 전처리과정
def preprocessing(content: str):
    mpck = MPCK()
    tokens = mpck.tokenize(content)
    ngrams = mpck.ngramize(tokens)
    score = mpck.classify(tokens + ngrams, intensity_cutoff=1.5)

    return score


df_all_data = text_from_csv().sort_values(by='date', ascending=True)

# purpose : True(테스트 목적) / False(전체 데이타셋으로 csv파일 생성), default value = False
create_total_dataset_csv(df_all_data, purpose=True)
