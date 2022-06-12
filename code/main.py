from my_data import *

FILE_DIRECTORY = "./data/"
while True:
    print("-----------대학별 맛집 추천-----------")
    print("1. 기존 회원")
    print("2. 신규 회원")
    print("3. 회원 탈퇴")
    print("0. 프로그램 종료")
    print("--------------------------------------")
    index = input("Enter the key: ")

    if index=='1':
        while True:
            member_id = input("ID를 입력하세요: ")
            if member_id == "0":
                flag = 0
                break
            try:
                member = MemberManage(member_id)
                member.check_menulist()
                member.check_missing_rate()
                flag = member.original_member()
                break
            except:
                print("아이디가 존재하지 않습니다. 다시 입력해주세요.")
                continue
        if (flag == -1):
            continue
        if (flag != 0):
            file = open(FILE_DIRECTORY + 'client_data/'+member_id+'/'+'dummy.txt', mode='w')
            file.write(flag)
            file.close()
    elif index == '2':
        member_id = input("ID를 입력하세요: ")
        member = MemberManage(member_id)
        member.new_member()
    elif index == '3':
        while True:
            member_id = input("ID를 입력하세요: ")
            ans = input("정말 탈퇴하시겠습니까? (Y/n) ")
            if (ans == 'Y'):
                if os.path.exists(FILE_DIRECTORY + 'client_data/'+member_id):
                    shutil.rmtree(FILE_DIRECTORY + 'client_data/'+member_id)
                    print("탈퇴 완료 되었습니다.")
                    break
                else:
                    print("회원 정보가 없습니다. 아이디를 다시 입력하세요.")
                    continue
            elif (ans == 'n'):
                break
            else:
                print("입력 형식이 맞지 않습니다.")
                continue
    elif index == '0':
        break
    else:
        print("입력 형식이 잘못 되었습니다. 0,1,2 중 하나로 다시 입력하세요.")
    
        

