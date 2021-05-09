import datetime
import time
import re

############################# 함수 #############################

def insta_searching(word): # word라는 매개변수를 받는 insta_searching 함수 생성
        url = 'https://www.instagram.com/explore/tags/'+word
        return url

def select_first(driver):
        first = driver.find_element_by_css_selector('div._9AhH0')
        #find_element_by_css_selector 함수를 사용해 요소 찾기
        first.click()
        time.sleep(3) #로딩을 위해 3초 대기


# 본문 내용, 작성 일시, 위치 정보 및 해시태그 추출
def get_content(driver):
        # 1. 현재 페이지의 HTML 정보 가져오기
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        # 2. 본문 내용 가져오기
        try: # 어려 태그 중 첫번째([0]) 태그를 선택
                content = soup.select('div.C4VMK > span')[0].text
                # 태그명이 div, class명이 C4VMK인 태그 아래에 있는 span태그를 모두 선택
        except:
                content = ' '
        # 3. 본문 내용에서 해시태그 가져오기(정규표현식 활용)
        tags = re.findall(r'#[^\s#,\\]+', content)
        '''
        content 변수의 본문 내용 중 #으로 시작하며, # 뒤에 연속된 문자 (공백,#,\기호가 아닌경우)를
        모두 찾아 tags 변수에 저장
        '''
        # 4. 작성 일자 가져오기
        try:
                date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]
        except:
                date = ''
        # 5. 좋아요 수 가져오기
        try:
                like = soup.select('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > section.EDfFK.ygqzn > div > div > a')[0].text[4:-1]
        except:
                like = 0
        # 6. 위치 정보 가져오기
        try:
                place = soup.select('react-root > section > main > div > div.ltEKP > article > header > div.o-MQd.z8cbW > div.M30cS > div.JF9hh > a')[0].text
        except:
                place = ''

        # 7. 포스트 아이디 정보 가져오기
        try:
                post_id = soup.select_one('body > div._2dDPU.CkGkG > div.zZYga > div > article > header > div.o-MQd.z8cbW > div.PQo_0.RqtMr > div.e1e1d > span > a').string
        except:
                post_id = ''
        
        # 7. 수집한 정보 저장
        data = [post_id, content, date, like, place, tags]
        return data

# 다음 게시물로 이동
def move_next(driver):
        right = driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow')
        right.click()
        time.sleep(3)

############################# 본문 #############################
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
import openpyxl

# 1. 드라이버 실행
driver = webdriver.Chrome('./chromedriver.exe')
word = '' # 키워드 입력
target =  # 크롤링할 게시물 수
fileName = '.xlsx' # 저장할 파일 명
url = insta_searching(word)
driver.get(url)
time.sleep(5)

# 2. 로그인 하기
## 로그인 버튼 클릭 (가끔 안나올때가 있음, 안뜨면 주석처리)

driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button').click()
time.sleep(4)

email = '' # 아이디 입력
input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
input_id.clear()
input_id.send_keys(email)


password = '' # 비밀번호 입력
input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
input_pw.clear()
input_pw.send_keys(password)
input_pw.submit()

time.sleep(5)

# 로그인 정보 넘어가기
## 로그인 정보 저장 안 나올 수도...
try:
    log_info_button = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/section/div/button')
    log_info_button.click()
except:
    pass
   
time.sleep(5)

# 알람 설정 넘어가기
## 알람 설정이 나오지 않을 경우가 있음..
try:
    alarm_remove_button = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[1]')
    alarm_remove_button.click()
except:
    pass
   
time.sleep(5)

# 3. 검색페이지 접속
driver.get(url)
time.sleep(4)
# 4. 첫번째 게시글 열기
select_first(driver)
# 5. 비어있는 변수(results) 만들기
results = []

# 여러 게시물 크롤링하기
for i in range(target):
        data = get_content(driver)
        results.append(data)
        print(str(i+1)+'/'+str(target))
        try:
                move_next(driver)
                
        except:
                break
        
df = pd.DataFrame(results, columns = ["post_id", "content", "date", "like", "place", "tags"])
df.to_excel(fileName)


## 종료
driver.close()
                

# 결과: id/본문내용/날짜/좋아요수/장소/해시태그
