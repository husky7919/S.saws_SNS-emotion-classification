def insta_searching(word):
    url = "https://www.instagram.com/" + word
    return url


from bs4 import BeautifulSoup
from  selenium import webdriver
import time
import pandas as pd
import re
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

driver.get("https://www.instagram.com/accounts/login/")
time.sleep(1) 

email = input("아이디입력: ")   
input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
input_id.clear()
input_id.send_keys(email)

##password 입력
password = input("비밀번호입력: ")
input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
input_pw.clear()
input_pw.send_keys(password)
input_pw.submit()
time.sleep(3)

word = email
url = insta_searching(word)
driver.get(url)
time.sleep(2)

insta_dict = {'date': [],'text': []}
first_post = driver.find_element_by_class_name('eLAPa')
first_post.click()
num = 0
seq = 0
start = time.time()
 
while num < 11  :
    try:
        if driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow'):
            if seq % 20 == 0:
                print('{}번째 수집 중'.format(seq), time.time() - start, sep = '\t')
 
 
            ## 시간정보 수집 
            time_raw = driver.find_element_by_css_selector('time.FH9sR.Nzb55')
            time_info = pd.to_datetime(time_raw.get_attribute('datetime')).normalize()
            insta_dict['date'].append(time_info)
 
            ##text 정보수집
            raw_info = driver.find_element_by_css_selector('div.C4VMK').text.split()
            text = []
            for i in range(len(raw_info)):
                ## 첫번째 text는 아이디니까 제외 
                if i == 0:
                    pass
                ## 두번째부터 시작 
                else:
                    if '#' in raw_info[i]:
                        pass
                    else:
                        text.append(raw_info[i])
            clean_text = ' '.join(text)
            insta_dict['text'].append(clean_text)
 
            seq += 1
 
            if seq == 100:
                break
 
            driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow').click()
            time.sleep(1.5)
            
 
        else:
            break
            
    except NoSuchElementException:
        driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow').click()
        time.sleep(2)
    num += 1

#데이터프레임 만들고 엑셀로 저장하기
results_df = pd.DataFrame(insta_dict)
results_df.to_csv(r'D:\S.saws.project\repository\insta_crawler\insta_crawler.csv', index=False) 