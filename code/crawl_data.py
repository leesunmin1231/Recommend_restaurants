from sre_constants import SUCCESS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #selenium에서 사용할 모듈 import

import time
import requests
from bs4 import BeautifulSoup
import re
import csv



def crawl_store(input_data):
    driver = webdriver.Chrome("./code/chromedriver") #selenium 사용에 필요한 chromedriver.exe 파일 경로 지정



    driver.get("https://map.naver.com/v5/") #네이버 신 지도 
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "input_search"))
        ) #입력창이 뜰 때까지 대기
    finally:
        pass

    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "input_search")))
    search_box.send_keys(input_data)
    search_box.send_keys(Keys.ENTER) #검색창에 장소 입력

    frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#searchIframe")))

    driver.switch_to.frame(frame)

    # 여기까지 iframe 전환

    scroll_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[2]/div[1]")))
    #검색 결과로 나타나는 scroll-bar 포함한 div 잡고
    driver.execute_script("arguments[0].scrollBy(0,2000)", scroll_div)
    time.sleep(1)
    driver.execute_script("arguments[0].scrollBy(0,2000);", scroll_div)
    time.sleep(1)
    driver.execute_script("arguments[0].scrollBy(0,2000);", scroll_div)
    time.sleep(1)
    driver.execute_script("arguments[0].scrollBy(0,2000);", scroll_div)
    time.sleep(1)
    driver.execute_script("arguments[0].scrollBy(0,2000);", scroll_div)
    time.sleep(1)
    #여기까지 scroll
    #맨 아래까지 내려서 해당 페이지의 내용이 다 표시되게 함

    final_result = []
    # # 반복 시작
    count_store = 0 # 가져올 상점 개수 

    i = 2
    while i<=5: #몇 페이지까지 크롤링할 것인지 지정
        stores_box = driver.find_element(by=By.XPATH, value='//*[@id="_pcmap_list_scroll_container"]')
        stores = driver.find_elements(by=By.CSS_SELECTOR, value="li._1EKsQ._12tNp")
        #해당 페이지에서 표시된 모든 가게 정보
    
        for store in stores: #한 페이지 내에서의 반복문. 순차적으로 가게 정보에 접근
            if count_store >=50:
                break
            name = store.find_element_by_css_selector("span.OXiLu").text #가게 이름
            try:
                rating = store.find_element_by_css_selector("span._2FqTn._1mRAM em").text
            except:
                rating = "0"
            try:
                state = store.find_element_by_css_selector("span._2FqTn._4DbfT").text
            except:
                state = ''
            
            # print ("success, store: {}".format(count_store))
            click_name = store.find_element_by_css_selector("span.OXiLu")
            click_name.click() 
        # 가게 주소, 홈페이지 링크를 확인하려면 가게 이름을 클릭해 세부 정보를 띄워야 함.

            time.sleep(1)
            driver.switch_to.default_content()      
        ##오래 헤맸던 부분!! switch_to.default_content()로 전환해야 frame_in iframe을 제대로 잡을 수 있다. 
        
            frame_in = driver.find_element_by_xpath("/html/body/app/layout/div[3]/div[2]/shrinkable-layout/div/app-base/search-layout/div[2]/entry-layout/entry-place-bridge/div/nm-external-frame-bridge/nm-iframe/iframe")

            driver.switch_to.frame(frame_in) 
            # 가게 이름을 클릭하면 나오는 세부 정보 iframe으로 이동 
            try:
                address = driver.find_element_by_css_selector("div.place_section.no_margin._18vYz li._1M_Iz._1aj6- div._1h3B_ span._2yqUQ").text
            except:
                address = ''
            try:
                menu = driver.find_element_by_css_selector("div.place_section.GCwOh div._3uUKd._2z4r0 div._1_hm2 span._3ocDE").text
            except:
                menu=''
            #주소 정보 확인
            store_info = {
                'placetitle':name,
                'menu':menu,
                'rate':float(rating),
                'sales_state':state,
                'address':address
            }
            #크롤링한 정보들을 store_info에 담고
            # print(name,menu,rating,state,address)
            # print("*" * 50)
            final_result.append(store_info)
            count_store+=1
            # 출력해서 확인 후 final_result에 저장

            driver.switch_to.default_content()
            driver.switch_to.frame(frame)
            time.sleep(2)
            # 한 페이지 크롤링 끝
            
            # '2'페이지로 이동하는 버튼 클릭 후 i 1증가 
        try:
            next_button = driver.find_element(by=By.LINK_TEXT, value=str(i))
            next_button.click()
        except:
            break
        i = i+1
        time.sleep(3)
    check_list = []
    copy_result = []
    for item in final_result:
        copy_result.append(item)
    for item in copy_result:
        if item['placetitle'] in check_list:
            final_result.remove(item)
        else:
            check_list.append(item['placetitle'])
    final_result.sort(key = lambda x :x['rate'], reverse=True)
    #print(final_result)
    # csv 파일 생성
    file = open('./data/crawl_data/'+input_data+'.csv', mode='w', newline='')
    writer = csv.writer(file)
    writer.writerow(["가게 이름","메뉴", "평점", "영업 상태", "주소"])
    for data in final_result:
        writer.writerow(data.values())

    file.close()
    #최종 결과 확인
