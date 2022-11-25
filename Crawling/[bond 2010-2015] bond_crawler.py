# 네이버 채권 73~128 page
# 2010년도 자료까지 다운로드





# 링크 크롤링

import requests
from bs4 import BeautifulSoup


link_list = []


for i in range(73, 128) :
    URL = 'https://finance.naver.com/research/debenture_list.naver?&page='+str((i))
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')

    results = soup.find_all(class_='file')   

    for result in results:

        a_tag = result.find('a')    
        href = a_tag.attrs['href']

        link_list.append(href)

for i in range(-10, 0):
    link_list.pop(i)

link_list





# link_list csv 파일로 만들기

import pandas as pd

df = pd.DataFrame(link_list, columns = ['link'])

df.to_csv("link_list_73~127.csv", index = False)





# 파일명 크롤링
# 오직 파일 저장명을 위한.....

file_name = []
date_list=[] # csv로 저장할 때 넣을 날짜 미리 뽑아버림

for i in range(73, 128) :
    URL = 'https://finance.naver.com/research/debenture_list.naver?&page='+str((i))
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')

    information = soup.select('table.type_1')

    for info in information:

        if i <= 126:
            for a in range(2, 47):
                try:

                    title = info.select('tr')[a].select('td')[0].text.strip()
                    specialChars = '\/:*?"<>|' # 파일명에 특수문자 들어가 있는 경우 제거
                    for specialChar in specialChars:  
                        title = title.replace(specialChar, '')
                    
                    name = info.select('tr')[a].select('td')[1].text.strip()
                    date = info.select('tr')[a].select('td')[3].text.strip()
                        
                    temp = [date, name, title]
                    file_name.append(temp)
                    date_list.append(date)
        
                except:
                    if temp in file_name:
                        pass

        else:
            for a in range(2, 31): # 127page -> 2010년도 자료까지만 가져옴
                try:  
                    title = info.select('tr')[a].select('td')[0].text.strip()
                    specialChars = '\/:*?"<>|'
                    for specialChar in specialChars:  
                        title = title.replace(specialChar, '')

                    name = info.select('tr')[a].select('td')[1].text.strip()
                    date = info.select('tr')[a].select('td')[3].text.strip()
                        
                    temp = [date, name, title]
                    file_name.append(temp)
                    date_list.append(date)

                except:
                    if temp in file_name:
                        pass

# file_name # file_name 확인





# 파일명 csv 파일로 만들기

import pandas as pd

df = pd.DataFrame(file_name, columns = ['date', 'name', 'title'])

df.to_csv("file_name_73~127.csv", index = False, encoding='utf-8')





# 링크, 파일명 csv 파일 병합
import pandas as pd
import numpy as np
import os

df1 = pd.read_csv('./file_name_73~127.csv')
df2 = pd.read_csv('./link_list_73~127.csv')

df1['link']=df2['link']

df1.to_csv('./merge_73~127.csv', index=False)





# 파일 다운로드 함수

from urllib.request import urlopen
import pandas as pd
import os

def file_download(report_name:str):
    report_data = pd.read_csv(report_name)
    
    for i in range(0, len(report_data)):
        report_info = report_data.loc[i]
        
        rpt_date = report_info['date']
        rpt_name = report_info['name'] # stock firm name
        rpt_title = report_info['title'] # report title
        rpt_link = report_info['link'] # report link


        download = urlopen(rpt_link).read()

        file = './data/' + rpt_date + ', ' + rpt_name + ', ' + rpt_title +'.pdf'
        try: 
            with open(file, mode='wb') as f: 
                f.write(download)

        except:
            if FileNotFoundError:
                print(f' {file} have not found')
            else:
                pass





print(file_download('./merge.csv'))