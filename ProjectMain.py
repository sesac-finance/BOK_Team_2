import os
import pandas as pd
from ekonlpy.sentiment import MPCK

# to see all data
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
pd.set_option('display.colheader_justify', 'left')

stop_words = ['NR', 'VV', 'VA', 'VX', 'VCP', 'VCN', 'MM', 'MAJ', 'IC', 'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV',
                  'JKQ', 'JX', 'JC', 'EP', 'EF', 'EC', 'ETN', 'ETM', 'XPN', 'XSN', 'XSV', 'XSA', 'XR', 'SF', 'SE',
                  'SSO', 'SSC', 'SC', 'SY', 'SL', 'SH', 'SN']

# 다양한 소스로부터 수집된 csv 파일들로부터 데이타 불러오기
def text_from_csv():
    mergerd_directory = './Data/Merged/'
    total_text = []
    columns = ['date', 'contents']
    for files_name in os.listdir(mergerd_directory):
        text_list = []

        # if 'Minutes' not in files_name:
        # print(f'(text_from_csv)processing file = {files_name}')

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


def creation_ngram_dict(total_dataset: pd.DataFrame):
    cnt = 0
    word_list = []


    for index in range(len(total_dataset)):
        content = total_dataset['contents'].iloc[index]
        date = total_dataset['date'].iloc[index]

        mpck = MPCK()
        tokens = mpck.tokenize(content)

        add_word_list = []
        for word in tokens:
            if word not in stop_words:
                add_word_list.append(word)

        word_list.extend(mpck.ngramize(add_word_list))

        print("creation_ngram_dict process check by date : ", date)
        # print(word_list)

        cnt += 1
        if cnt > 2000:
            break

    df_dict_words = pd.DataFrame(set(word_list))
    df_dict_words.to_csv('./Data/MDLs/dict_ngram.csv')


# 통합된 데이타파일에 up/down/ngram된 내용 추가
def merge_polarity(total_dataset: pd.DataFrame):
    call_rate_columns = ['origin_date', 'origin_rate', 'comp_date', 'comp_rate', 'polarity']
    df_call_rate = pd.read_csv('./Data/MDLs/call_rate.csv', header=None, names=call_rate_columns)
    df_polarity_dataset_total = pd.merge(total_dataset, df_call_rate, how='left', left_on='date',
                                         right_on='origin_date')

    df_polarity_dataset_total['contents_ngrams'] = 'NAN'

    cnt = 0
    for index in range(len(df_polarity_dataset_total)):
        date = df_polarity_dataset_total['date'].iloc[index]
        content = df_polarity_dataset_total['contents'].iloc[index]

        mpck = MPCK()
        tokens = mpck.tokenize(content)
        add_word_list = []
        for word in tokens:
            if word not in stop_words:
                add_word_list.append(word)
        ngrams = mpck.ngramize(add_word_list)
        df_polarity_dataset_total['contents_ngrams'].iloc[index] = ngrams

        cnt += 1
        if cnt > 100:
            break

    return df_polarity_dataset_total

# df_all_data = text_from_csv().sort_values(by='date', ascending=True)

# purpose : True(테스트 목적) / False(전체 데이타셋으로 csv파일 생성), default value = False
# create_total_dataset_csv(df_all_data, purpose=False)
# df_total_data = pd.read_csv('./Data/MDLs/sentiment_results.csv')



# 통합된 csv 파일로부터 데이터프레임 추출
df_all_data = text_from_csv().sort_values(by='date', ascending=True)

# ngram 사전(up/down 추가 전)
# creation_ngram_dict(df_all_data)

# up/down/ngram된 내용 추가
merged_df_all_date = merge_polarity(df_all_data)
print(merged_df_all_date.to_csv('./Data/MDLs/test.csv'))


