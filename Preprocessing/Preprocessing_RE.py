import sys
import csv
import re


# 2022 새싹 2팀에서 뉴스기사 크롤링 csv 포맷은 num, data, text 이렇게 3 컬럼으로 정한다.
# num은 일련번호, data 포맷은 1999.01.01, text 는 한글/영어/숫자/기호가 섞여있는 뉴스기사 본문임

maxInt = sys.maxsize


while True:
    try:
        # 용량이 큰 뉴스기사를 파싱할 때 에러 방지를 위해서 시스템이 허용하는 최대값을 넣어준다.
        csv.field_size_limit(maxInt)

        with open("D:\\git\\newstudy\\code\\csv\\naver_news_scrapy_total_prep_2.csv", 'rt', encoding='UTF-8', newline='') as csvfile:
        
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            with open("D:\\git\\newstudy\\code\\csv\\Team2_naver_news_scrapy_total_prep_2.csv", 'w', newline='', encoding='UTF8') as f:
                # create a csv writer
                writer = csv.writer(f)

                csv_text = ""
                list_string = []
                new_string = ""

                for i, row in enumerate(csvreader):      

                    list_string = re.findall(r"""[ㄱ-ㅣ가-힣]|[ |\,|\.]""",  row[2])
                    
                    # 제목을 원본 CSV와 동일하게 넣어주기 위해서 첫 줄은 처리없이 그대로 써준다.
                    if i == 0 :
                        writer.writerow(row)

                    else :
                        t = ''
                        for x in list_string:
                            if x =='' :
                                t += ' '
                            else :
                                t += x

                        t = t.strip()
                        new_string = re.sub(r"""[\,|\.]""", " ", t)
                        new_string = re.sub(r"""[ ]{2,}""", " ", new_string)
                        new_string = re.sub(r"""[ ]([ㄱ-ㅣ가-힣][ ]).[ ]""", " ", new_string)
                        new_string = re.sub(r"""[ ][ㄱ-ㅣ가-힣][ ]""", " ",new_string)
                        new_string = re.sub(r"""[ ][ㄱ-ㅣ가-힣][ ]""", " ", new_string)
                        new_string = re.sub("\n", "", new_string)
                        

                        row[2] = new_string
                        writer.writerow(row)
        break

    except OverflowError:
        # python3에서 간혹 허용 최대값 적용시 에러가 발생하는데 이를 방지하기 위한 부분 
        maxInt = int(maxInt/10)
            

      
    
        