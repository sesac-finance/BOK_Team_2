from urllib.request import urlopen
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import olefile
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd


# 한글파일(hwp)로부터 텍스트 추출
def extract_text_from_hwp(file_path: str) -> str:
    return olefile.OleFileIO(file_path).openstream('PrvText').read().decode('utf-16')
    # return olefile.OleFileIO(file_path).openstream('PrvText').read().decode('utf-16').split("\r\n")


# BOK 의사록 다운로드(1~27페이지)
def download_BOK_minutes():
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
    page_index = 1

    # BOK minutes download from 2010 to 2022
    while page_index < 27:
        base_url = 'https://www.bok.or.kr'
        url = f'https://www.bok.or.kr/portal/bbs/B0000245/list.do?menuNo=200761&pageIndex={page_index}'

        response = requests.get(url, headers={"User-Agent": agent})
        if response.status_code == 200:
            board_source = BeautifulSoup(response.text, 'html.parser')
            results = board_source.find('div', class_='bdLine type2').find_all("li")

            for index, txt in enumerate(results):
                try:
                    sub_url = base_url + txt.find('a')['href']
                    title = txt.find('a').text
                    if 'pdf' not in title or 'hwp' not in title:
                        file_header = title
                    if "FILE" not in sub_url:
                        result = requests.get(sub_url, headers={"User-Agent": agent})
                        source = BeautifulSoup(result.text, 'html.parser')
                        data = source.find('div', class_='addfile').find_all("li")

                        for idx, file_info in enumerate(data):
                            file_name = file_info.find("a").text
                            if 'pdf' in file_name:
                                link_name = file_info.find('a')['href']
                                file_download_from_web(base_url + link_name, file_header.strip(), 'pdf')

                except Exception as e:
                    pass
        else:
            print(response.status_code)

        page_index += 1


# 웹사이트에 업로드되어 있는 파일 다운로드
def file_download_from_web(url: str, file_name: str, file_extension: str):
    download = urlopen(url).read()
    file = '../Data/Original/KOB Minutes/' + file_name + '.' + file_extension
    with open(file, mode='wb') as f:
        f.write(download)
        print(f' {file} Save Complete')


# PDF 파일로부터 텍스트 추출
def extract_text_from_pdf(file_path: str, codec='utf-8', password='', maxpages=0, caching=True) -> str:
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
        text = retstr.getvalue().strip()

    fp.close()
    device.close()
    retstr.close()
    return text


# 추출된 텍스트를 csv 파일로 저장
def text_to_csv(csv_file_name):
    base_directory = '../Data/Original/KOB Minutes/'
    save_directory = '../Data/Merged/'
    KOB_Minutes = []
    for files_name in os.listdir(base_directory):
        file_list = []
        if '.pdf' in files_name:
            text_set = extract_text_from_pdf(base_directory + files_name)
            text_list = text_set[text_set.index('회의경과') + 4:].split()
            file_list.append(files_name)
            file_list.append(' '.join(text_list))
            print(files_name)
        KOB_Minutes.append(file_list)
    KOB_Minutes_List = pd.DataFrame(KOB_Minutes)
    KOB_Minutes_List.to_csv(save_directory + csv_file_name)
    print(f'{csv_file_name} save Done!')
    # test = pd.read_csv('KOB_Minutes.csv')
    # print(test)

# download_BOK_minutes()
# text_to_csv('KOB_Minutes.csv')
