### pdf 링크 및 보고서 정보 크롤링
import requests
from bs4 import BeautifulSoup

# pdf파일 링크 크롤링
BASE_URL = 'https://finance.naver.com/research/debenture_list.naver?&'

link_list=[]

for page in range(1, 73):
    parameters = 'page=' + str(page)
    URL = BASE_URL + parameters
    
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')

    url_results = soup.find_all(class_='file')
   
    
    for result in url_results:
        try:
            a_tag = result.select('a')[0].attrs['href']
            
            link_list.append(a_tag)
        except:
            pass
                    
#print(link_list)


# 채권분석 보고서 날짜, 제목 정보 크롤링

file_info = []

for i in range(1, 73) :
    URL = 'https://finance.naver.com/research/debenture_list.naver?&page='+str((i))
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')

    information = soup.select('table.type_1')

    for info in information:

            for a in range(2, 47):
                try:
                    
                    title = info.select('tr')[a].select('td')[0].text.strip()
                    specialChars = '\/:*?"<>|'
                    for specialChar in specialChars:  
                        title = title.replace(specialChar, '')
                    
                    name = info.select('tr')[a].select('td')[1].text.strip()
                    date = info.select('tr')[a].select('td')[3].text.strip()
                        
                    temp = [date, name, title]
                    file_info.append(temp)
        
                except:
                    if temp in file_info:
                        pass



# pdf 파일이 존재하지 않는 보고서 정보의 인덱스 확인
file_info.index(['22.07.20', '미래에셋증권', '미국 금리 역전 심화와 국내 장기금리 추가 하락 기대'])

# 보고서 정보와 pdf가 불일치함을 확인
file_info[206], link_list[206]

# 해당 보고서정보 인덱스를 삭제
file_info.pop(206)



### csv 변환
# 보고서정보 데이터 csv 변환
import pandas as pd

link_list_df= pd.DataFrame(file_info)
save_link= link_list_df.to_csv('./채권[1-73]_file info.csv', index=False)

# 링크 데이터 csv 변환
link_list_df= pd.DataFrame(link_list)
save_link= link_list_df.to_csv('./채권[1-73]_pdf_link.csv', index=False)

# 두 개a의 csv 병합
info_df= pd.read_csv('./채권[1-73]_file info.csv')
link_df= pd.read_csv('./채권[1-73]_pdf_link.csv', sep='\t')
info_df['3']=link_df['0']
info_df.to_csv('./채권[1-73]_데이터병합.csv', index=False)



### pdf 다운로드 코드

from urllib.request import urlopen
import pandas as pd
import os

def pdf_file_download(report_name:str):
    report_data= pd.read_csv(report_name) #레포트 데이터 파일 불러오기
    
    for i in range(0, len(report_data)):
        report_info= report_data.loc[i] #행으로 추출해 낸 것
        
        rpt_date= report_info['0']
        stf= report_info['1'] #stock firm
        rpt_nm= report_info['2'] #report name
        rpt_lk= report_info['3'] #report link


        download = urlopen(rpt_lk).read()

        file = './data/'+ rpt_date + '_' + rpt_nm +'.pdf'
        try: 
            with open(file, mode='wb') as f: 
                f.write(download)
                #print(f' {file} Save Complete')
        except:
            if FileNotFoundError:
                print(f' {file} is not found')
            elif AttributeError:
                pass
        
        
# 갯수 일치하는지 확인
import os
list_check= os.listdir('./data/')
len(list_check)