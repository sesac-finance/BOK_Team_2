#### 텍스트 추출 함수
from urllib.request import urlopen
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def extract_text_from_pdf(file_path: str, codec='utf-8', password='', maxpages=0, caching=True):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    
    fp = open(file_path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
        text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text



### 데이터 파일 분리하기 (500 * 500 * 500 * 500 * 159개)
import shutil
import os

# 폴더 안 파일 리스트 만들기
# 데이터가 있는 폴더 경로
path_dir= './data/'   


# 이동할 폴더의 경로
# 숫자 하나씩 변경
move_path_dir= './data[1-73p](1)/' 

# 폴더 안의 파일 리스트를 가져온다.
file_list= os.listdir(path_dir)
div_files= file_list[0:500]
#print(div_files)


# 리스트에서 조건에 맞는 파일을 찾으면서 목표 폴더로 분류
for item in div_files:
    shutil.move(path_dir+item, move_path_dir+item)



### 폴더별로 pdf to text 변환
# data 폴터 내 파일 목록 불러오기

import os 
import pandas as pd

PATH = './data[1-73p](1)/'  #괄호 속 숫자 바꿔가면서!

file_list = []

for path, dir, files in os.walk(PATH):
    for file in files:
        current = os.path.join(path, file)

        file_list.append(current)


# 각 파일 텍스트 추출
text = []
  
for file in file_list:
    try:
        content = extract_text_from_pdf(file).strip().split()
        join_content = ' '.join(content)
        text.append(join_content)
        
    except Exception as e:
        print(file,e)
        pass


### text를 csv 파일로 저장
import pandas as pd
text_from_pdf= pd.DataFrame(text)
text_from_pdf.to_csv('채권[1-73]_totext(1).csv')  # 괄호 속 숫자 바꿔가면서!



### csv파일 마무리 작업  
#> 자동인덱스, 파일제목, 변환된 텍스트
import pandas as pd
import os


get_filename= os.listdir('./data[1-73p](1)/')
get_filename_df= pd.DataFrame(get_filename)

file_org= pd.read_csv('채권[1-73]_totext(1).csv')
file_org['1']=file_org['0']
file_org['0']=0
file_org['0']=get_filename_df

file_org.to_csv('./채권[1-73]_fin(1).csv', index=False)
file_org