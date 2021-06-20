from selenium import webdriver
import time
import re
import time

def insta_searching(word):
    url = "https://www.instagram.com/explore/tags/"+str(word)
    return url

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

driver.get('https://www.instagram.com')
email = input("아이디입력: ")
input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
input_id.clear()
input_id.send_keys(email)

password = input("비밀번호입력: ")
input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
input_pw.clear()
input_pw.send_keys(password)
input_pw.submit()
time.sleep(1)

word = input("검색어 입력: ")
word = str(word)
url = insta_searching(word)

driver.get(url)
time.sleep(5)

insta_dict = {'text': []}

#첫번쨰 게시물의 위치를 class값을 이용해 찾음

first_post = driver.find_element_by_class_name('eLAPa')
#첫번쨰 게시물 클릭
first_post.click()
time.sleep(30)
num = 0
seq = 0
#정보를 가져오는 속도를 측정하기위한 코드
start = time.time()

# 크롤링할 게시물의 개수를 정함

while num < 2001  :

    try:

        if driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow'):
            
            if seq % 20 == 0:
                print('{}번째 수집 중'.format(seq), time.time() - start, sep = '\t')
 
            raw_info = driver.find_element_by_css_selector('div.C4VMK').text.split()

            text = []

            for i in range(len(raw_info)):

                if i == 0:
                    pass 
                else:

                    if '#' in raw_info[i]:
                        pass

                    else:
                        text.append(raw_info[i])

            clean_text = ' '.join(text)

            insta_dict['text'].append(clean_text)

            seq += 1

            if seq == 2000:
                break
     
            driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow').click()
            time.sleep(3)
            

        else:
            break

    except:
        driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow').click()
        time.sleep(3)
    num += 1

import pandas as pd

results_df = pd.DataFrame(insta_dict)
results_df.columns = ['content']
results_df.to_csv(r'D:\S.saws.project\repository\수집데이터_iloveyou2.csv')