# BOK 기준금리 예측 프로젝트

 * 파일 구조
   * ├── Crawling 
   * ├── Preprocessing
   * ├── MDLing
   * ├── Data
   * │ ├── Original
   * │ 	├── KOB Minutes 
   * │ 	├── News
   * │ 	├── Bond_Analysis
   * │ ├── Merged
   * │ ├── MDLs
   * └── 


   * Crawling : 크롤링 소스코드(2010년~2022년의 회의록, 뉴스, 채권애널리스트 분석)  
   * Preprocessing : 자연어 전처리 소스코드
   * MDLing : 모델링 소스코드 
   * Data : 데이터 모음
   * Data/Original/KOB Minutes : 한국은행 의사록
   * Data/Original/News : 웹으로부터 수집된 뉴스 데이터
   * Data/Original/Bond_Analysis : 채권보고서
   * Data/Merged : 각 사이트로부터 수집된 데이터 모음
   * Data/MDLs : 모델링된 파일들