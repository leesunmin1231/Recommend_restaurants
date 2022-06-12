import pandas as pd
import numpy as np
import csv
import os
import shutil
from crawl_data import *

FILE_DIRECTORY = "./data/"

# 1. 데이터 저장 클래스
# 2. 데이터 업데이트 클래스
# 3. 멤버 관리 클래스

class DataStorage:
  def __init__(self):
    self.place_list = self.get_filelist()
    self.menulist = ["와인", "맥주", "닭발", "분식", "국수", "족발", "보쌈", "삼계탕", "감자탕", "소고기", "삼겹살", "곱창", "막창", "치킨", "닭강정",
    "떡볶이","커피","디저트","베트남 음식", "인도 음식", "회", "초밥", "중식", "마라탕", "파스타", "피자", "브런치"]
  def get_filelist(self):
    file_list = os.listdir(FILE_DIRECTORY + 'crawl_data')
    file_name = []
    for file in file_list:
        if file.count(".") == 1: 
            name = file.split('.')[0]
            file_name.append(name)
        else:
            for k in range(len(file)-1,0,-1):
                if file[k]=='.':
                    file_name.append(file[:k])
                    break
    return file_name
  def get_menulist(self):
    return self.menulist
  def get_userlist(self):
    file_list = os.listdir(FILE_DIRECTORY + 'client_data')
    return file_list
 # 데이터 저장 클래스. 맛집 파일 목록, 메뉴 리스트를 가져와서 저장해둔다.
class UpdateData:
  def __init__(self):
    self.upcsv = DataStorage()
    self.menu_list = self.upcsv.get_menulist()
    self.place_list = self.upcsv.get_filelist()
    self.arr_size = 20 * len(self.place_list)
  def get_menulist(self):
    return self.upcsv.get_menulist()
  def get_placelist(self):
    return self.place_list
  def get_arrsize(self):
    return self.arr_size 
  def new_user_data(self, user_name, my_favor):
    file = open(FILE_DIRECTORY + 'client_data/'+user_name+'/'+user_name+'.csv', mode='w', newline='')
    writer = csv.writer(file)
    writer.writerow(["대학","가게 이름","메뉴","주소","메뉴 평점","인터넷 평점", "내 평점", "총 내 평점"])
    my_result = []
    for i in range(len(self.place_list)):
      final_data = []
      # 가게 이름,메뉴,평점,영업 상태,주소
      crawl_file = pd.read_csv(FILE_DIRECTORY + 'crawl_data/'+self.place_list[i]+'.csv')
      for ik,row in crawl_file.iterrows():
        num = float(row["평점"])
        favor_rate = -1
        for j,data in enumerate(self.menu_list):
          if data in str(row["메뉴"]):
            num = (float(row["평점"]) + my_favor[j])/2
            favor_rate = my_favor[j]
            break
        user_data = {
          "university": self.place_list[i],
          "store" : row["가게 이름"],
          "menu" : row["메뉴"],
          "address" : row["주소"],
          "favor" : favor_rate,
          "rate" : float(row["평점"]),
          "my_rate" : 0,
          "total_rate" : num
        }
        final_data.append(user_data)
      final_data.sort(key = lambda x :x['total_rate'], reverse=True)
      my_result.append(final_data)
    for lst in my_result:
      index = 0
      for data in lst:
        if (index >= 20):
          break
        writer.writerow(data.values())
        index+=1
    file.close()

  def update_myrate(self,user_name, my_favor, my_store_rate):
    file = open(FILE_DIRECTORY + 'client_data/'+user_name+'/'+user_name+'.csv', mode='w', newline='')
    writer = csv.writer(file)
    writer.writerow(["대학","가게 이름","메뉴","주소","메뉴 평점","인터넷 평점", "내 평점", "총 내 평점"])
    my_result = []
    for i in range(len(self.place_list)):
      final_data = []
      # 가게 이름,메뉴,평점,영업 상태,주소
      crawl_file = pd.read_csv(FILE_DIRECTORY + 'crawl_data/'+self.place_list[i]+'.csv')
      for ik,row in crawl_file.iterrows():
        num = float(row["평점"])
        favor_rate = -1
        for j,data in enumerate(self.menu_list):
          if data in str(row["메뉴"]):
            num = (float(row["평점"]) + my_favor[j])/2
            favor_rate = my_favor[j]
            break
        user_data = {
          "university": self.place_list[i],
          "store" : row["가게 이름"],
          "menu" : row["메뉴"],
          "address" : row["주소"],
          "favor" : favor_rate,
          "rate" : float(row["평점"]),
          "my_rate" : 0,
          "total_rate" : num
        }
        final_data.append(user_data)
      #final_data.sort(key = lambda x :x['total_rate'], reverse=True)
      my_result.append(final_data)

    for lst in my_result:
      for data in lst:
        # if (index >= 20):
        #   break
        for item in my_store_rate:
          if data['university'] == item[0] and data['store'] == item[1]: 
            data['my_rate'] = item[2]
        if data['my_rate'] != 0:
          if data["favor"] != -1:
            data['total_rate'] = (data['my_rate'] + data['rate'] + data["favor"]) / 3
          else:
            data['total_rate'] = (data['my_rate'] + data['rate']) / 2
      lst.sort(key = lambda x :x['total_rate'], reverse=True)
    for lst in my_result:
      index = 0
      for data in lst:
        if (index >= 20):
          break
        writer.writerow(data.values())
        index+=1
    file.close()

  def input_menu(self,user_name):
    menu_list = self.upcsv.get_menulist();
    file = open(FILE_DIRECTORY + 'client_data/'+user_name+'/'+user_name+'.txt', mode='w')
    my_favor = []
    i = 0
    while (i < len(menu_list)):
      print("{} ".format(menu_list[i]),end='')
      try:
        num = float(input('선호도를 입력하세요.(0~5): '))
        if num >=0 and num <= 5:
          my_favor.append(num)
        else:
          print("잘 못 입력하였습니다. 다시 입력하십시오. (0 ~ 5)")
          continue
      except:
        print("잘 못 입력하였습니다. 다시 입력하십시오. (0 ~ 5)")
        continue
      line_data = "{}:{}\n".format(menu_list[i],my_favor[i])
      file.write(line_data)
      i+=1
    file.close()
    return my_favor
  
  def update_crawlData(self):
    while True:
      ans = input("9개 대학 맛집 정보를 업데이트 하시겠습니까? (약 20분 정도 소요) Y/n ")
      if ans == "Y":
        for place in self.place_list:
          crawl_store(place)
          print("{} 정보 업데이트 완료".format(place))
        break
      elif ans == 'n':
        print("업데이트 하지 않습니다.")
        break
      else:
        print("입력 형식에 맞지 않습니다. 다시 입력하세요.")
        continue
# 사용자의 정보 업데이트 하는 메소드 들을 모아 놓은 클래스.
# 1. 전체 크롤링 데이터 업데이트하는 함수.
# 2. 음식 선호도 입력받는 함수.
# 3. 내 평점 업데이트 하는 함수. 등이 있다.
class MemberManage:
  def __init__(self,username):
    self.up = UpdateData()
    self.username = username

  def check_missing_rate(self):
    if os.path.exists(FILE_DIRECTORY + 'client_data/'+self.username+'/'+'dummy.txt'):
      file = open(FILE_DIRECTORY + 'client_data/'+self.username+'/'+'dummy.txt', mode='r')
      store_name = file.readline()
      file.close()
      print("이전에 갔던 {}의 별점을 입력하지 않았습니다.".format(store_name))
      while True:
          ans = input("별점을 입력하시겠습니까? (Y/n) ")
          if ans == 'Y':
              client_file = pd.read_csv(FILE_DIRECTORY + 'client_data/'+self.username+'/'+self.username+'.csv')
              self.input_store_rate(client_file, store_name)
              break
          elif ans == 'n':
              print("별점을 입력하지 않습니다.")
              break
          else:
              print("다시 입력해주세요")
              continue
      os.remove(FILE_DIRECTORY + 'client_data/'+self.username+'/'+'dummy.txt')

  def check_menulist(self):
    file = open(FILE_DIRECTORY + 'client_data/'+self.username+'/'+self.username+'.txt', mode='r')
    my_list = []
    lst = file.readlines()
    for lst_item in lst:
      my_list.append(lst_item.split(":")[0])
    for i in range(len(self.up.menu_list)):
      if self.up.menu_list[i] != my_list[i]:
        print("맛집 데이터가 업데이트 되었습니다.")
        print("음식 선호도를 변경합니다.")
        my_favor = self.up.input_menu(self.username)
        my_store_rate = []
        f = pd.read_csv(FILE_DIRECTORY + 'client_data/'+self.username+'/'+self.username+'.csv')
        for il,row in f.iterrows():
          lst = []
          lst.append(row["대학"])
          lst.append(row["가게 이름"])
          lst.append(float(row["내 평점"]))
          my_store_rate.append(lst)
        self.up.update_myrate(self.username, my_favor, my_store_rate)
        print("변경 완료 되었습니다.")
        break

  def input_store_rate(self, client_file, store_name):
    while True:
      try:
        store_rate = float(input("가게 별점을 입력하세요 (1~5): "))
        if (store_rate >= 1 and store_rate <= 5):
          break
        else:
          print("잘못 입력되었습니다. 1점에서 5점 사이로 입력하세요.")
          continue
      except:
        print("잘못 입력되었습니다. 1점에서 5점 사이로 입력하세요.")
        continue
    my_store_rate = []
    for il,row in client_file.iterrows():
      lst = []
      lst.append(row["대학"])
      lst.append(row["가게 이름"])
      if str(row['가게 이름'])==store_name:
        lst.append(float(store_rate))
      else:
        lst.append(float(row["내 평점"]))
      my_store_rate.append(lst)
    file = open(FILE_DIRECTORY + 'client_data/'+self.username+'/'+self.username+'.txt', mode='r')
    my_favor = []
    lst = file.readlines()
    for lst_item in lst:
      my_favor.append(float(lst_item.split(":")[-1]))
    self.up.update_myrate(self.username, my_favor, my_store_rate)

  def recommend_store(self):
    while True:
      place = input("검색할 대학가 맛집을 입력하세요 (ex: 중앙대 맛집): ")
      if os.path.exists(FILE_DIRECTORY + 'crawl_data/'+place+'.csv'):
        break
      else:
        print("입력 형식이 맞지 않습니다. 다시 입력하세요.")
        continue
    # 대학,가게 이름,메뉴,주소,인터넷 평점,내 평점,총 내 평점 
    try:
      client_file = pd.read_csv(FILE_DIRECTORY + 'client_data/'+self.username+'/'+self.username+'.csv')
      to_find= client_file[client_file['대학']==place]
      prob = to_find["총 내 평점"]/sum(to_find["총 내 평점"])
      top5 = np.random.choice(to_find['가게 이름'],5,p=prob,replace=False)
    except:
      file = open(FILE_DIRECTORY + 'client_data/'+self.username+'/'+self.username+'.txt', mode='r')
      my_favor = []
      lst = file.readlines()
      for lst_item in lst:
        my_favor.append(float(lst_item.split(":")[-1]))
      self.up.new_user_data(self.username, my_favor)
      client_file = pd.read_csv(FILE_DIRECTORY + 'client_data/'+self.username+'/'+self.username+'.csv')
      
      to_find= client_file[client_file['대학']==place]
      prob = to_find["총 내 평점"]/sum(to_find["총 내 평점"])
      top5 = np.random.choice(to_find['가게 이름'],5,p=prob,replace=False)
    for i in range(5):
      print("{}. {}".format(i+1, top5[i]), end ="")
      for ik,row in to_find.iterrows():
        if (row["가게 이름"] == top5[i]):
          print(" 메뉴: {}, 최종 평점: {}, 주소: {}".format(row["메뉴"], row["총 내 평점"], row["주소"]))
    while True:
      print("갈 곳을 입력하시오. (1~5)")
      print("뒤로가기: 0")
      index_store = int(input("Enter the key: "))
      if (index_store > 5 or index_store < 0):
        print("다시 입력하세요 (1~5)")
        continue
      elif index_store == 0:
        return(-1)
      else:
        break
    while (True):
      rate_index = input("가게 별점을 지금 입력하시겠습니까? Y/n ")
      if (rate_index == 'n'): # 선택 후 입력 안함.
        return (top5[index_store-1])
      elif (rate_index == 'Y'):
        self.input_store_rate(client_file, top5[index_store-1])
        return(0)
      else:
        print("다시 입력하세요. (Y/n)")

  def original_member(self):
    if not os.path.exists(FILE_DIRECTORY + 'client_data/'+self.username):
      print("ID를 잘 못 입력하였습니다.")
      return (-1)
    while True:
      print("-----------대학별 맛집 추천-----------")
      print("1. 음식별 선호도 수정하기")
      print("2. 맛집 검색하기")
      print("3. 내 별점 업데이트 하기")
      print("4. 인터넷 별점 정보 업데이트 하기")
      print("0. 뒤로가기")
      print("--------------------------------------")
      index = input("Enter the key: ")
      my_store_rate = []
      f = pd.read_csv(FILE_DIRECTORY + 'client_data/'+self.username+'/'+self.username+'.csv')
      for il,row in f.iterrows():
        lst = []
        lst.append(row["대학"])
        lst.append(row["가게 이름"])
        lst.append(float(row["내 평점"]))
        my_store_rate.append(lst)
      if index == '1':
        my_favor = self.up.input_menu(self.username)
        self.up.update_myrate(self.username, my_favor, my_store_rate)
        print("회원 정보가 변경 되었습니다.")
        continue
      elif index == '2':
        return_data = self.recommend_store()
        if return_data != -1:
          return return_data
        else:
          continue
      elif index == '3': # 네이버 지도에서 크롤링한 데이터가 변경된 경우, 내 총 평점 업데이트.
        file = open(FILE_DIRECTORY + 'client_data/'+self.username+'/'+self.username+'.txt', mode='r')
        my_favor = []
        lst = file.readlines()
        for lst_item in lst:
          my_favor.append(float(lst_item.split(":")[-1]))
        self.up.update_myrate(self.username, my_favor, my_store_rate)
        print("회원 정보가 변경 되었습니다.")
      elif index == '4':
        self.up.update_crawlData()
        file = open(FILE_DIRECTORY + 'client_data/'+self.username+'/'+self.username+'.txt', mode='r')
        my_favor = []
        lst = file.readlines()
        for lst_item in lst:
          my_favor.append(float(lst_item.split(":")[-1]))
        self.up.update_myrate(self.username, my_favor, my_store_rate)
      elif index == '0':
        return 0
      else:
        print("다시 입력해 주세요.")
        continue

  def new_member(self):
    try:
      if not os.path.exists(FILE_DIRECTORY + 'client_data/'+self.username):
        os.makedirs(FILE_DIRECTORY + 'client_data/'+self.username)
      else:
        print("이미 존재하는 ID입니다.")
        return
    except OSError:
      print ('Error: Creating directory. ' + FILE_DIRECTORY + 'client_data/'+self.username)
      return
    my_favor = self.up.input_menu(self.username)
    self.up.new_user_data(self.username, my_favor)
    print("회원 정보가 등록되었습니다.")
# 사용자들을 관리하는 클래스 (가장 핵심적인 역할이다.)
# 기존 회원 정보를 관리하는 메소드와 신규 회원 데이터를 저장하는 메소드가 있다.