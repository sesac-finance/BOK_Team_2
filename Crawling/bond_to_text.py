# 텍스트 추출 함수

from urllib.request import urlopen
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import olefile

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





# data 폴더 내 파일 목록 불러오기

import os 
import pandas as pd
import csv

# PATH = 작업 폴더 내 data 폴더
PATH = './data'

file_list = []
max_depth = 0
for path, dir, files in os.walk(PATH):
    for file in files:
        current = os.path.join(path, file).replace('\\', '/')
        file_list.append(current)
        
        if len(current.split('/')) > max_depth: 
            max_depth = len(current.split('/'))

file_list





# 리스트에서 각 파일명 추출

for i in file_list:
    print(i)





# 각 파일 텍스트 추출
try:
    text = []
    for file in file_list:
        content = extract_text_from_pdf(file).strip().split()
        join_content = ' '.join(content)
        text.append(join_content)
except:
    pass

text





# 텍스트 추출 후 csv 파일로 만들기

import pandas as pd

df = pd.DataFrame(text, columns=['text'])
df.index.name = 'title'
df.to_csv("text_73~127.csv", index = True)